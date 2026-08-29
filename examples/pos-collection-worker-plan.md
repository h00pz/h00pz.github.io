# Collection Worker Implementation Plan

This is the *plan* half of the same pair: it turns the collection-worker spec (examples/pos-collection-worker-spec.md) into an ordered sequence of implementable, test-first slices with their dependencies made explicit, before any code is written. Reproduced as the worked example for the post [Spec to Plan to Code](https://h00pz.github.io/p/spec-plan-code/); cross-references to other pOS documents are left as plain identifiers.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the first real lane worker — a deterministic `feed` collection worker that claims a collection demand, fetches the measure from a non-ibeam source (FRED), records the run, and completes with the value through the FML-1210 result slot.

**Architecture:** A standing process on the FML-1302 `WorkerLoop` (`createWorkerLoopFromEnv`), holding no store connection and no model. It claims over the ClaimStore demand seam, resolves the demand to a `feed` collector, fetches via a NEW injected `FeedFetch` port (mirroring `IbeamGateway`/`ModelTransport` — real client at the composition root, fake in tests), writes a `CollectorRunRecord`, and returns the value as the `WorkOutcome.complete.result`. A prerequisite path-override on the shared `PosApiClient` lets the generic client reach any seam's real mount path — fixing the same wall every future lane worker hits.

**Tech Stack:** TypeScript, Node 20 (global `fetch`), npm workspaces + turbo, jest/ts-jest, express (seam router), UBI9 container, k8s Deployment (restricted-v2 SCC).

## Global Constraints

- **No build without an FML** — Task 0 bakes the FML; every code task lands under it. One lifecycle transition per PR.
- **A worker holds NO database connection, ever** (FML-1302) — the worker imports no `@pos/persistence` driver; its only state-plane dependency is `POS_API_URL`. An acceptance test asserts `require.cache` holds no db driver.
- **Honest degradation** (seam-pattern §7) — a feed that errors/empties/stales is a recorded `gap` + honest completion, never a fabricated value.
- **Never fabricate; every read carries asOf + source** (FML-1205) — a fetched value carries its `asOf`.
- **Dockerfile.api/worker needs a COPY line per new package** — a container build fails where `npm run build` passed if a new package is not copied.
- **Board flipped to `built` BEFORE the reconcile gate**, then invariant check (`python3 scripts/generate-route-manifest.py`, 0 NEW).
- **Deterministic, position-blind** — this worker calls no model and never sees a position.
- **Package name convention:** `@pos/worker`, `@pos/platform-api`, `@pos/collection`, `@pos/persistence`.

---

## File Structure

- `docs/fml/sections/s13_platform_runtime.py` (or s01) — Task 0: the new worker FML item + edge.
- `packages/pos-worker/src/pos-api-client.ts` — Task 1: add `seamPath?` override.
- `packages/pos-collection/src/feed-fetch.ts` (new) — Task 2: the `FeedFetch` port + `SeriesFetchResult` type.
- `packages/pos-collection/src/fred-feed.ts` (new) — Task 3: the real FRED-backed `FeedFetch` impl + injected http transport.
- `packages/pos-collection/src/collection-work.ts` (new) — Task 4: the pure `work` fn (demand → fetch → run record → outcome), no worker/loop.
- `packages/pos-collection/src/collection-worker.ts` (new) — Task 5: `createCollectionWorker()` + `start()` (the entry, mirrors demo-worker.ts).
- `apps/api/src/index.ts` — Task 4/6: wire the FeedFetch client + (if needed) the demand collector store at the composition root.
- `docker/Dockerfile.collection-worker` (new) + `k8s/base/collection-worker.yaml` (new) — Task 6.
- `docs/fml/sections/...` — Task 7: flip the FML to `built`.

---

### Task 0: Author + bake the collection-worker FML

**Files:**
- Modify: `docs/fml/sections/s13_platform_runtime.py` (add the item + its feature slug to the FML-13 spine + an edge)
- Regenerate: `docs/fml/*` via `python3 docs/fml/generate_fml.py`

**Interfaces:**
- Produces: a baked FML id (e.g. `FML-1310`, slug `collection-worker`) that every later task lands under. Confirm the next free seq in §13 at authoring time.

- [ ] **Step 1: Add the item** to `s13_platform_runtime.py` ITEMS (a `required_now`/`planned_compatible` `feature`, `life="woven"`, `deployed` unset). Need/why quote the design doc: the framework is live as definitions + demand seam + lease substrate, but nothing runs it; this is the execution half and the cleanest first lane worker. `endpoints=[]` (it declares no surface — it CALLS the demand seam). Add its slug to the FML-13 spine `features=[...]`.
- [ ] **Step 2: Add the edge** — the new item `requires` FML-1302 (the worker loop) and FML-102 (the demand seam), both `confirmed`.
- [ ] **Step 3: Regenerate + verify**

Run: `cd docs/fml && python3 generate_fml.py && grep "collection-worker" ledger.md`
Expected: the new row appears, `woven`/⬜ pending, no assembler assert failure.

- [ ] **Step 4: Commit the bake (its own PR)**

```bash
git checkout -b h00pz/fml-collection-worker-bake
git add docs/fml/
git commit -m "bake(platform-runtime): the collection worker — the execution half the framework was built without"
git push origin HEAD:refs/for/main -o topic=fml-collection-worker-bake -o title="bake: the collection worker"
```
Main session merges via Gitea API, then syncs main before Task 1.

---

### Task 1: PosApiClient seam-path override (unblocks every worker)

**Files:**
- Modify: `packages/pos-worker/src/pos-api-client.ts` (the `PosApiClientConfig` + the path builders)
- Test: `packages/pos-worker/src/pos-api-client.test.ts`

**Interfaces:**
- Consumes: existing `PosApiClientConfig = { baseUrl; workerId; lane; basePath?; fetch? }` (pos-api-client.ts).
- Produces: `PosApiClientConfig` gains `readonly seamPath?: string`. When set, every seam path is built as `${basePath}${seamPath}/...` instead of `${basePath}/${lane}/${recordType}/...`. Default (unset) = today's behavior exactly. This lets the client reach a seam mounted at a custom `basePath` (the demand seam's real path is `/collection/demands`, not `/pos-collection/demand`).

- [ ] **Step 1: Write the failing test**

```ts
// pos-api-client.test.ts — new describe
it('targets the seamPath when provided, not lane/recordType', async () => {
  const calls: string[] = [];
  const fakeFetch = (async (url: string) => {
    calls.push(url);
    return new Response(null, { status: 204 }); // empty claim
  }) as unknown as FetchFn;
  const client = new PosApiClient({
    baseUrl: 'http://x', basePath: '/api', seamPath: '/collection/demands',
    workerId: 'w', lane: 'pos-collection', fetch: fakeFetch,
  });
  await client.claim({ recordType: 'demand', filterKey: 'demand' });
  expect(calls[0]).toBe('http://x/api/collection/demands/claim');
});
it('falls back to lane/recordType when seamPath is unset (back-compat)', async () => {
  const calls: string[] = [];
  const fakeFetch = (async (url: string) => { calls.push(url); return new Response(null, { status: 204 }); }) as unknown as FetchFn;
  const client = new PosApiClient({ baseUrl: 'http://x', basePath: '/api', workerId: 'w', lane: 'pos-collection', fetch: fakeFetch });
  await client.claim({ recordType: 'demand', filterKey: 'demand' });
  expect(calls[0]).toBe('http://x/api/pos-collection/demand/claim');
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd packages/pos-worker && npx jest pos-api-client -t seamPath`
Expected: FAIL (seamPath ignored; first test hits `/api/pos-collection/demand/claim`).

- [ ] **Step 3: Implement the override.** Add `readonly seamPath?: string` to `PosApiClientConfig`. Introduce a private `seamBase(recordType)` returning `this.seamPath ?? `/${this.lane}/${recordType}``, and use it in `claim`/`heartbeat`/`complete`/`release`/`emit`/`get`/`list` in place of the inlined `/${this.lane}/${recordType}`. Keep `{id}` suffixes identical. The `/api` prefix logic (basePath) is unchanged.

- [ ] **Step 4: Run to verify pass**

Run: `cd packages/pos-worker && npx jest pos-api-client` — Expected: PASS, full suite green (back-compat test proves default unchanged).

- [ ] **Step 5: Commit**

```bash
git add packages/pos-worker/src/pos-api-client.ts packages/pos-worker/src/pos-api-client.test.ts
git commit -m "feat(worker): PosApiClient seamPath override so the generic client reaches any seam mount"
```

---

### Task 2: The FeedFetch port

**Files:**
- Create: `packages/pos-collection/src/feed-fetch.ts`
- Test: `packages/pos-collection/src/feed-fetch.test.ts`
- Modify: `packages/pos-collection/src/index.ts` (export the port + types)

**Interfaces:**
- Produces:
```ts
export interface SeriesFetchOk { readonly ok: true; readonly value: number; readonly asOf: string; readonly unit: string; }
export interface SeriesFetchGap { readonly ok: false; readonly reason: 'unreachable' | 'no_observation' | 'malformed'; }
export type SeriesFetchResult = SeriesFetchOk | SeriesFetchGap;
export type FeedFetch = (source: string, spec: string) => Promise<SeriesFetchResult>;
```
Mirrors `IbeamGateway`'s result-union discipline (marks.ts) — never throws on a source failure, returns a typed gap. `source` = the `FeedCollectorDefinition.source`; `spec` = the demand's `spec` (the series id).

- [ ] **Step 1: Write the failing test** — a fake FeedFetch returns ok + a gap, asserting the union shape is usable.

```ts
import type { FeedFetch, SeriesFetchResult } from './feed-fetch';
it('a FeedFetch resolves ok and gap without throwing', async () => {
  const fetchOk: FeedFetch = async () => ({ ok: true, value: 2.1, asOf: '2026-08-02T00:00:00Z', unit: 'percent' });
  const fetchGap: FeedFetch = async () => ({ ok: false, reason: 'no_observation' });
  expect(await fetchOk('FRED', 'DFII10')).toEqual({ ok: true, value: 2.1, asOf: '2026-08-02T00:00:00Z', unit: 'percent' });
  expect(await fetchGap('FRED', 'DFII10')).toEqual({ ok: false, reason: 'no_observation' });
});
```

- [ ] **Step 2: Run — Expected FAIL** (module not found). `cd packages/pos-collection && npx jest feed-fetch`
- [ ] **Step 3: Implement** — write `feed-fetch.ts` with the interfaces above (types only, no impl). Export from `index.ts`.
- [ ] **Step 4: Run — Expected PASS.**
- [ ] **Step 5: Commit** — `feat(collection): the FeedFetch port — a typed, non-throwing series fetch seam`.

---

### Task 3: The FRED-backed FeedFetch implementation

**Files:**
- Create: `packages/pos-collection/src/fred-feed.ts`
- Test: `packages/pos-collection/src/fred-feed.test.ts`
- Modify: `packages/pos-collection/src/index.ts`

**Interfaces:**
- Consumes: `FeedFetch`, `SeriesFetchResult` (Task 2); `FetchFn = typeof globalThis.fetch`.
- Produces: `export function createFredFeed(cfg: { apiKey: string; baseUrl?: string; fetch?: FetchFn }): FeedFetch`. Calls FRED `fred/series/observations?series_id=<spec>&api_key=<key>&file_type=json&sort_order=desc&limit=1`; maps the latest observation → `{ok:true, value, asOf, unit}`; a network error → `{ok:false,'unreachable'}`, empty observations → `{ok:false,'no_observation'}`, unparseable → `{ok:false,'malformed'}`. Never throws. `fetch` injected (default global) so tests are network-free.

- [ ] **Step 1: Write the failing tests** (fake fetch returns a canned FRED body; assert ok mapping, and each gap path).

```ts
import { createFredFeed } from './fred-feed';
const body = JSON.stringify({ observations: [{ date: '2026-08-01', value: '2.13' }] });
it('maps the latest FRED observation to ok', async () => {
  const fetchFn = (async () => new Response(body, { status: 200 })) as unknown as FetchFn;
  const feed = createFredFeed({ apiKey: 'k', fetch: fetchFn });
  expect(await feed('FRED', 'DFII10')).toEqual({ ok: true, value: 2.13, asOf: '2026-08-01', unit: 'percent' });
});
it('returns no_observation on empty', async () => {
  const fetchFn = (async () => new Response(JSON.stringify({ observations: [] }), { status: 200 })) as unknown as FetchFn;
  expect(await createFredFeed({ apiKey: 'k', fetch: fetchFn })('FRED', 'DFII10')).toEqual({ ok: false, reason: 'no_observation' });
});
it('returns unreachable when fetch rejects', async () => {
  const fetchFn = (async () => { throw new Error('down'); }) as unknown as FetchFn;
  expect(await createFredFeed({ apiKey: 'k', fetch: fetchFn })('FRED', 'DFII10')).toEqual({ ok: false, reason: 'unreachable' });
});
```
(Note: FRED returns no unit; default `'percent'` for the real-yield/rate series in scope, or carry unit on the collector definition and pass it in — pick one and be consistent. This plan defaults `'percent'`.)

- [ ] **Step 2: Run — Expected FAIL.** `cd packages/pos-collection && npx jest fred-feed`
- [ ] **Step 3: Implement `createFredFeed`** per the interface; guard every access (untrusted body); catch fetch rejection → `unreachable`; `Number.parseFloat` NaN → `malformed`.
- [ ] **Step 4: Run — Expected PASS.**
- [ ] **Step 5: Commit** — `feat(collection): FRED-backed FeedFetch, honest gaps, injected fetch`.

---

### Task 4: The pure work function

**Files:**
- Create: `packages/pos-collection/src/collection-work.ts`
- Test: `packages/pos-collection/src/collection-work.test.ts`
- Modify: `packages/pos-collection/src/index.ts`

**Interfaces:**
- Consumes: `QueuedDemand` (demand-intake.ts: `{ demandId; spec; transform; horizons; freshnessContract; demandRef; why }`), `FeedFetch` (Task 2), `WorkOutcome` (`@pos/worker`), `recordRun` + `CollectorRunRecord` + `CollectorRunInput` (collector-framework.ts), `Repository<CollectorRunRecord>` (@pos/persistence), `recordSeriesValue` + `SeriesValueInput` (series-releases.ts), `BiTemporalStore<SeriesValue>`.
- Produces:
```ts
export function createCollectionWork(deps: {
  readonly feed: FeedFetch;
  readonly runs: Repository<CollectorRunRecord>;
  readonly series: BiTemporalStore<SeriesValue>;
  readonly source: string;          // e.g. 'FRED' — the feed source for this worker
  readonly now: () => string;
}): (payload: unknown) => Promise<WorkOutcome>;
```
> **AS-BUILT SUPERSEDES this Task-4 sketch.** Per [[feedback_workers_never_touch_db]], the work fn
> does NOT take `runs`/`series` store ports and does NOT call recordSeriesValue/recordRun — a worker
> never touches the DB. It takes an injected `post: (path, body) => Promise<void>` and POSTs the
> finished records to the persist-only endpoints; pos-api writes them. See Task 5c (the shipped
> behavior). The description below is the original store-writing sketch, retained for history only.

The work fn (AS-BUILT): cast payload → `QueuedDemand`; `feed(source, demand.spec)`; on ok → `post('/collection/series', {seriesId, asOf, value, unit, source})` + `post('/collection/runs', {status:'ok', ...})` → `{kind:'complete'}` (bare — the writes landed via the POSTs); on gap → `post('/collection/runs', {status:'failed', error: reason})` → `{kind:'complete'}` (a gap is a TERMINAL honest completion, not a release); on a POST failure → `{kind:'release', reason}` so the demand requeues and the gathered value is never dropped; malformed payload → `{kind:'failure', detail}` before any post.

- [ ] **Step 1: Write the failing tests** — fake feed (ok + gap), in-memory `Repository`/`BiTemporalStore` fakes; assert (a) ok path writes a series value + an `ok` run record + returns complete-with-value, (b) gap path writes a `failed` run record + returns complete-with-gap (NOT release), (c) a malformed payload → `{kind:'failure', detail}`.

```ts
import { createCollectionWork } from './collection-work';
it('ok: records series value + ok run, completes with value', async () => {
  const runs = fakeRepo<CollectorRunRecord>(); const series = fakeBiTemporal<SeriesValue>();
  const feed: FeedFetch = async () => ({ ok: true, value: 2.13, asOf: '2026-08-01', unit: 'percent' });
  const work = createCollectionWork({ feed, runs, series, source: 'FRED', now: () => '2026-08-02T00:00:00Z' });
  const out = await work({ demandId: 'd1', spec: 'DFII10', transform: 'level', horizons: ['short'], freshnessContract: { maxAgeSeconds: 86400 }, demandRef: 'r', why: 'w' });
  expect(out).toEqual({ kind: 'complete', result: { seriesId: 'DFII10', value: 2.13, asOf: '2026-08-01' } });
  expect((await runs.list()).some(r => r.status === 'ok')).toBe(true);
  expect((await series.list()).length).toBe(1);
});
it('gap: records failed run, completes with gap (not release)', async () => {
  const runs = fakeRepo<CollectorRunRecord>(); const series = fakeBiTemporal<SeriesValue>();
  const feed: FeedFetch = async () => ({ ok: false, reason: 'no_observation' });
  const work = createCollectionWork({ feed, runs, series, source: 'FRED', now: () => 'now' });
  const out = await work({ demandId: 'd1', spec: 'DFII10', transform: 'level', horizons: ['short'], freshnessContract: { maxAgeSeconds: 86400 }, demandRef: 'r', why: 'w' });
  expect(out).toEqual({ kind: 'complete', result: { seriesId: 'DFII10', gap: 'no_observation' } });
  expect((await runs.list()).some(r => r.status === 'failed')).toBe(true);
});
```
(Use the existing in-memory fakes from `@pos/persistence` test utils if present; else a minimal `{ put/list }` fake. Confirm `SeriesValue`/`BiTemporalStore` method names against series-releases.ts before writing the fake.)

- [ ] **Step 2: Run — Expected FAIL.**
- [ ] **Step 3: Implement `createCollectionWork`** per the interface. Validate the payload shape (missing `spec`/`demandId` → `{kind:'failure', detail}`). Keep it PURE — no fetch, no worker, deps injected.
- [ ] **Step 4: Run — Expected PASS.**
- [ ] **Step 5: Commit** — `feat(collection): the collection work fn — demand to series value + run record, honest gaps`.

---

### Task 5: The collection worker entry

**Files:**
- Create: `packages/pos-collection/src/collection-worker.ts`
- Test: `packages/pos-collection/src/collection-worker.test.ts` (in-process, real seam router + InMemoryClaimStore, the first-worker.test.ts pattern)
- Modify: `packages/pos-collection/src/index.ts`

**Interfaces:**
- Consumes: `createWorkerLoopFromEnv` (`@pos/worker`, `WorkerFromEnvConfig` incl `seamPath` is NOT on it — see note), `createCollectionWork` (Task 4), the demand seam constants (`DEMAND_LANE='pos-collection'`, `DEMAND_RECORD_TYPE='demand'`, `DEMAND_FILTER_KEY='demand'`).
- Produces: `export function createCollectionWorker(deps): WorkerLoop` and `export function start(): void` (mirrors demo-worker.ts). Reads env: `POS_API_URL` (via the factory), `FEED_SOURCE` (default `'FRED'`), `FRED_API_KEY`, `FRED_BASE_URL?`.

- NOTE: `createWorkerLoopFromEnv` (Task-1-updated `PosApiClient` is what it builds internally) must pass `seamPath: '/collection/demands'` through to the client. `WorkerFromEnvConfig` does NOT expose `seamPath` today. **Add `readonly seamPath?: string` to `WorkerFromEnvConfig` and thread it into the `PosApiClient` it constructs** (factory.ts). This is a small addition folded into THIS task (its deliverable — a worker that reaches the demand seam — needs it), tested by the in-process harness below.

- [ ] **Step 1: Write the failing integration test** (the first-worker.test.ts harness): real express on port 0, `createSeamRouter` for the demand descriptor over `InMemoryClaimStore`, `createPlatformQueuesRouter`; emit one demand; build the worker with a fake FeedFetch returning ok; `loop.runOnce()`; assert the demand completed (queue depth 0, and the completed record's `result` carries the value via `GET /platform/queues` + a GET on the record).

```ts
// harness mirrors packages/pos-worker/src/first-worker.test.ts
// emit a demand: POST /api/collection/demands with {filterKey:'demand', payload:{...QueuedDemand}}
// worker: createWorkerLoopFromEnv({ lane:'pos-collection', recordType:'demand', filterKey:'demand',
//   seamPath:'/collection/demands', work: createCollectionWork({feed: fakeOkFeed, runs, series, source:'FRED', now}) , now })
// assert: runOnce() → queue depth 0; the completed claim record.result === { seriesId, value, asOf }
```

- [ ] **Step 2: Run — Expected FAIL** (module missing; then, once written, FAIL if seamPath not threaded → claim 404s → depth stays 1).
- [ ] **Step 3: Implement** `collection-worker.ts` (`createCollectionWorker` + `start`) AND thread `seamPath` through `WorkerFromEnvConfig` → `PosApiClient` in factory.ts.
- [ ] **Step 4: Run — Expected PASS** (the demand is claimed, worked, completed-with-result; depth → 0).
- [ ] **Step 5: Commit** — `feat(collection): the collection worker entry + seamPath threading; in-process proof against the real seam`.

---

### Task 6: Container + k8s manifest

**Files:**
- Create: `docker/Dockerfile.collection-worker` (copy `docker/Dockerfile.worker`, change CMD to the collection-worker dist entry; COPY `platform-core`, `pos-worker`, `pos-collection`, `pos-persistence`? — NO: the worker holds no persistence driver; COPY only what the entry imports at runtime — verify with the require.cache test)
- Create: `k8s/base/collection-worker.yaml` (copy `k8s/base/worker-demo.yaml`; env `POS_API_URL`, `FEED_SOURCE=FRED`, `FRED_API_KEY` from a secret, `FRED_BASE_URL` optional; NO store credential; restricted-v2 SCC)

**Interfaces:** none (deploy artifacts).

- [ ] **Step 1: Write the Dockerfile** — multi-stage UBI9, mirror Dockerfile.worker, CMD `node packages/pos-collection/dist/collection-worker.js` (confirm the compiled entry path). Add the COPY lines for each runtime package.
- [ ] **Step 2: Verify the no-db-driver acceptance** — a test asserting `require.cache` after importing `collection-worker` holds no `mongodb`/`neo4j-driver`/`pg`. (If the collection package pulls a driver transitively, the worker entry must import only the pure work path — fix imports until clean.)
- [ ] **Step 3: Write the k8s manifest** — Deployment `pos-collection-worker`, replicas 1, the env above, `FRED_API_KEY` from `secretKeyRef` (operator supplies the secret; document the secret name). No `MONGODB_URI`/`NEO4J_*`/`POSTGRES_URI`.
- [ ] **Step 4: Build check** — `npm run build` green; `docker build -f docker/Dockerfile.collection-worker .` succeeds locally if the daemon is available (else note main-session/CI runs it).
- [ ] **Step 5: Commit** — `feat(collection): Dockerfile + k8s Deployment for the collection worker (no store credential)`.

---

### Task 7: Flip the board to built + PR

**Files:**
- Modify: the FML section source (add `deployed="built"` + a build-history line to the Task-0 item)
- Regenerate: `docs/fml/*`

- [ ] **Step 1: Set `deployed="built"`** on the collection-worker FML with a history line summarizing what shipped (seamPath override, FeedFetch port, FRED feed, work fn, worker entry, container/manifest; test counts).
- [ ] **Step 2: Regenerate + invariant check**

Run: `cd docs/fml && python3 generate_fml.py` then from repo root `python3 scripts/generate-route-manifest.py`
Expected: the FML shows 🔷 built; invariants `0 NEW` (the worker declares no endpoints, so board⊆seam is unaffected).

- [ ] **Step 3: Full workspace verify** — `npm run build` (all tasks), `npx turbo run test` (all packages green, no regressions).
- [ ] **Step 4: Commit + PR** — one build PR (code + board flip together). Main session reviews the real diff, re-runs suites, merges, then deploys + drives on-cluster (the FML-1209-style gate for the first lane worker) and flips `live` with evidence.

---

## Self-Review

**Spec coverage** (vs `2026-08-02-collection-worker-design.md`):
- §2 feed-only, non-ibeam → Tasks 2/3 (FeedFetch + FRED), no ibeam touched. ✓
- §3 the loop (claim → resolve → fetch → run record → complete-with-result) → Task 4 work fn + Task 5 entry. ✓
- §4 "this builds": feed client (T3), worker entry (T5), feed collector definitions (see gap below), Dockerfile+k8s (T6). ✓ except collector definitions.
- §5 deterministic/position-blind/no-db → Global Constraints + Task 6 require.cache assertion. ✓
- §6 build order (feed client → worker → deploy → widen) → Tasks 3→5→6. ✓
- §7.1 which FML → Task 0. §7.2 FRED key → Task 6 secret. §7.3 ibeam deferred → out of scope, stated. §7.4 cadence → the worker `run()` loop + backoff (factory default); exact cadence is a deploy tuning, noted. ✓

**Gap found + fixed:** the design's "feed collector definitions" (a `defineCollector` FeedCollectorDefinition per FRED series) is not its own task. It is small and belongs with the demand that needs it. **Add to Task 5 Step 3:** call `defineCollector({kind:'feed', id, name, source:'FRED', unit:'percent', cadence, horizons, freshness}, store, now)` for the first real-yield series, and assert the worker resolves the claimed demand's `spec` to it. (If demand→collector resolution is by `spec` match, the work fn in Task 4 already keys on `demand.spec` directly and the definition is metadata/catalogue — confirm at build time whether the work path needs the definition or only the demand; if only the demand, collector definitions become a catalogue-population step, not a work dependency, and stay a documented follow-on.)

**Placeholder scan:** no TBD/TODO; every code step carries real signatures from the current source. ✓

**Type consistency:** `FeedFetch`, `SeriesFetchResult`, `QueuedDemand`, `WorkOutcome`, `CollectorRunRecord`, `seamPath` used identically across Tasks 1–5. ✓

---

## Open items carried to execution
- **FRED unit:** defaulted `'percent'` for the real-yield/rate first series; if a later series needs a different unit, carry `unit` on the demand or the collector definition (noted in Task 3).
- **Demand→collector resolution:** confirm at build time whether the work path requires a `defineCollector` record or keys on `demand.spec` alone (Task 5 self-review note).
- **FRED_API_KEY secret:** operator supplies; Task 6 documents the secret name.
