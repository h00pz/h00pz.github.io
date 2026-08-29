# The Collection Worker — design (the true first worker)

This is a real PortfolioOS specification, reproduced as the worked example for the post [Spec to Plan to Code](https://h00pz.github.io/p/spec-plan-code/). It is the *spec* half of a spec-then-plan pair: it argues what the collection worker is, what it owns, and where its boundaries sit, before any implementation exists. Cross-references to other pOS documents are left as plain identifiers, because those documents are not published here.

**Status:** design, for operator review. Not yet FMLs, not yet built.
**Date:** 2026-08-02
**Companion:** `seam-collection.md`,
`collections-position-register.md` (the winds whose
measures this fills), `2026-08-02-portfolio-loop-worker-design.md`
(Track A, which this feeds).

> Reordered AHEAD of the PLW on 2026-08-02: the collector framework is live as DEFINITIONS + a demand
> seam + a lease substrate, but NOTHING runs it (subsystem self-reports `degraded`: "per-kind workers
> are later FMLs"). The instrumentation track cannot flow without a collection worker, and that worker
> is the CLEANEST first worker in the system — deterministic, no model, no position-awareness. It proves
> the worker pattern end-to-end on the FML-1302 loop + FML-1210 result slot, then the PLW (model-bound,
> position-aware) rides the proven pattern. See [[project_worker_tier_horse_cart]],
> [[feedback_workers_designed_not_sprinted]].

---

## 1. What the collection worker is

A standing process that **serves a collection demand**: it claims a demand for a measure, fetches the
value from a structured source, and records the run. It is the execution half the framework was built
without — `defineCollector`/`recordRun` and the demand seam are live; nothing fetches.

**It is the cleanest possible worker:** deterministic, holds no store connection (FML-1302), calls no
model, knows nothing about positions. Its only job is claim → fetch → record → complete. This is why it
is the first worker — it proves the pattern with none of the PLW's model/position complexity.

## 2. First scope — deliberately narrow

Two scoping decisions, operator-confirmed 2026-08-02:

- **`feed` kind only.** Of the five collector kinds (`feed`/`scrape`/`computed`/`agentic`/`artifact`),
  the first worker serves `feed` — a structured source returning a series value. `computed` (pure expr
  over other instruments) and `scrape` follow once the pattern is live; `agentic` waits on FML-113
  (captured, governed egress undesigned); `artifact` is a different output shape.
- **Non-ibeam sources first.** ibeam (the one price/FX gateway, FML-106) is an injected PORT with no
  client wired in v3 — wiring it is a separate infra task (operator's, like model-serving was). The
  first worker's feeds are the ones that DON'T need ibeam: **FRED** (real yields — already covered — and
  peers), **NOAA** (heating-degree-days), **EIA** (gas storage). ibeam-backed measures (copper,
  producer-FX) wait for the client and are served by the same worker once ibeam is up — a config
  addition, not a new worker.

The smallest honest keystone: **a `feed` collection worker, claiming one demand, fetching one series
from a non-ibeam source, writing one run record, completing with the value.**

## 3. The loop

```
collection worker (createWorkerLoopFromEnv, holds no store, holds no model):
  claim a demand over the ClaimStore seam (POST /collection/demands/claim)
    → payload: the demand (spec × transform × horizonSet — the measure to collect)
  fetch: call the feed source (FRED/NOAA/EIA) for the current value + asOf
  POST the finished SeriesValue to POST /collection/series (pos-api persists it as-is)
  POST the finished CollectorRunRecord to POST /collection/runs (pos-api persists it as-is)
  complete the lease (bare) — the writes already landed via the POSTs above
    → the demand's coverage read (GET /collection/demands/{id}/coverage) flips gap → served
```

> **AS-BUILT SUPERSEDES the original §3.** The design first had the worker `complete` WITH the
> result on the FML-1210 slot and pos-api derive the writes. The operator ruled otherwise
> ([[feedback_workers_never_touch_db]]): **the worker builds the finished records and POSTs them to
> persist-only endpoints; pos-api validates shape and writes AS-IS, never computes.** So the shipped
> worker POSTs the SeriesValue + run record, then completes the lease BARE (no result on the slot) —
> the coverage read flips on actually-persisted data, not a lease-result field. A failed POST
> RELEASES so the demand requeues; a gathered value is never dropped.

**Honest degradation (the framework's contract):** a feed that returns nothing, errors, or is stale is
a recorded `gap` on the run record and an honest completion — never a fabricated value. Same rule the
model client follows: absent data is a stated absence.

## 4. What is live vs what this builds

**Live (definitions + substrate):**
- FML-101 collector framework — the five kinds, `defineCollector`, `recordRun`, catalogue
- FML-102 demand seam — `POST /collection/demands` + the lease ops (`/claim`, `/{id}/{heartbeat,complete,release}`)
- `GET /collection/demands/{id}/coverage` — served · proxied · gap per instrument
- FML-106/107 gather SHAPES — `gatherPriceMark`, `recordSeriesValue` (functions a worker calls)
- FML-1302 worker loop + FML-1210 result slot — the substrate the worker runs on

**This builds:**
1. **The feed source client(s)** — a deterministic fetcher for FRED (and NOAA/EIA), an injected
   transport like the model client's (pure of the network in tests). Non-ibeam.
2. **The collection worker entry** — `createWorkerLoopFromEnv` claiming `collection/demands`, with a
   `work` fn that resolves the demand → picks the feed collector → fetches → builds a `CollectorRunRecord`
   → returns the value as the WorkOutcome result.
3. **Feed collector definitions** for the first measures (the FRED/NOAA/EIA series the register names).
4. **Dockerfile + k8s Deployment** — cloned from `worker-demo.yaml`, env `POS_API_URL` + the feed base
   URLs, NO store credential.

## 5. Why this is the right first worker

- **Deterministic** — no model, so no capability question, no budget, no honest-degradation-of-inference.
- **Position-blind** — collection never sees a holding; no position wall to get wrong.
- **Proves the whole substrate** — claim → work → complete-with-result → coverage flips. If this runs on
  the cluster, the FML-1302/1210 pattern is proven and the PLW (harder) copies it.
- **Feeds Track A** — every measure it lands flips a PLW wind uncovered → covered. It is the quality ramp
  the PLW rides, so building it first makes the PLW sharper the day it ships.

## 6. Build order (for the plan step)

1. **The feed source client** (FRED first — real-yield peers; the simplest structured JSON source).
2. **The collection worker** — the loop entry + work fn + one feed collector definition, proven in-process
   against a real seam router over an in-memory ClaimStore (the demo-worker test pattern).
3. **Deploy + drive** — image + manifest, run on-cluster, claim a real demand, observe coverage flip.
   This is the FML-1209-style gate for the first LANE worker.
4. **Widen** — more feed definitions (NOAA HDD, EIA gas storage), then `computed`, then `scrape`. ibeam
   client + its measures (copper, producer-FX) are a parallel infra task.

## 7. Open questions for the operator

1. **Which FML(s)** — the framework items (101/106/107) are built; the WORKER is new. Likely a new
   platform-runtime or pos-collection worker FML (mirrors how the PLW needs a new worker FML, not a
   re-bake of the shapes). To be settled at the FML-authoring step.
2. **FRED API key** — FRED needs a key. Operator-supplied secret (like `POS_INBOUND_ACK_SECRET`), or a
   keyless source for the very first proof.
3. **ibeam wiring** — the parallel infra task: stand up the ibeam client + deploy so the same worker can
   serve copper/producer-FX. Operator's, deferred, not blocking.
4. **Cadence** — how often the worker sweeps for claimable demands (the framework is pull, not push; the
   worker polls the claim). TIMELY vs PATIENT per the ingestion-cadence design.
