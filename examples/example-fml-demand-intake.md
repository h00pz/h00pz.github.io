# Example FML: The demand seam (FML-102)


This is a complete, real FML entry from PortfolioOS, reproduced exactly as it's written in the repository. It's the worked example for the post [The Failure Manifest Log](https://h00pz.github.io/p/the-failure-manifest-log/). Notice the shape the whole post is about: the entry opens with the operator need it answers, the deployed axis is kept honest, and the decision history at the bottom records the exact moment it went from built to proven-live against the running cluster. Cross-references to other ledger entries are left as plain identifiers, because those pages aren't published here.

---

**Canonical FML ID:** `demand-intake`  ·  **Sequence (metadata):** FML-102  
**Classification:** `planned_compatible`  ·  **Lifecycle status:** `woven`  ·  **Dependency health:** `clear`  
**Altitude:** `feature`  
**Target architecture:** 3.0  ·  **Target product:** 3.0  ·  **Owner:** operator  
**Architecture version:** 3.0  

> **Canonical rule (HASF §AG.5.1):** this detail page owns item truth. The FML index and any dependency graph are derived projections of this page.

## Intent
- **Operator need:** Eight of a hundred and thirty-one position winds are instrumented, and almost every instrumented one is a tailwind. Nobody ever asked collection for the rest, because there was no way to ask - so the gaps were invisible rather than declined.
- **Governing question:** How does a lane say what it needs measured, and how does it find out whether it can have it?
- **Capability summary:** One Demand record - spec, transform, horizons, freshness contract, demandRef and why - emitted by the Brain, either loop, Hunt or the home office. Collection answers per instrument: SERVED, PROXIED or GAP, with the cause. That is the whole of its answer.
- **Why it matters:** Collection's job is set by its customers, which is why this intake is the one endpoint deliberately open to every lane. And it never says whether the wind is a good one - the lane that owns the assumptions owns that.

## Impact
- **Operator workflow:** not_applicable
- **Canonical:** demands, and their per-instrument coverage state
- **Authority:** an instrument and a transform, never a position. A demand naming a holding is a 422
- **Lifecycle:** not_applicable
- **Information:** the coverage answer is a fact about collection, not an opinion about the demand
- **Surface:** not_applicable
- **AI:** not_applicable
- **Platform:** not_applicable
- **Security:** not_applicable
- **Migration:** not_applicable

## Architecture weaving & delivery
- **Weaving state:** baked 2026-07-31 as wave 13 — the collection lane made askable: the demand intake its four customers call, the one catalogue over everything gathered, declared proxies, and cite-or-reject retrieval. Deps built, opened for build.
- **Acceptance evidence:** A demand from each of the four customers returns served, proxied or gap per instrument, with a cause on every gap.
- **Next required action:** 

## Typed outgoing dependencies
| edge | type | target | hard? | state | rationale | satisfaction |
|---|---|---|---|---|---|---|
| edge-08 | `requires` | FML-101 | **hard** | confirmed | A demand is answered served, proxied or gap against declared collectors. |  |

## Typed incoming dependents (derived)
| type | source | hard? | state |
|---|---|---|---|
| `requires` | FML-105 | **hard** | confirmed |
| `requires` | FML-125 | **hard** | confirmed |
| `requires` | FML-126 | **hard** | confirmed |
| `requires` | FML-217 | **hard** | confirmed |
| `requires` | FML-306 | **hard** | confirmed |
| `requires` | FML-411 | **hard** | confirmed |
| `requires` | FML-714 | **hard** | confirmed |
| `requires` | FML-919 | **hard** | confirmed |
| `requires` | FML-1310 | **hard** | confirmed |

## Disposition
- **Revisit trigger:** not_applicable
- **Linked decisions:** spec:architecture/subsystem-collection, spec:architecture/seam-collection, collection-inventory

## Decision & classification history
- 2026-07-31 — baked (wave 13): the askable half of collection opened for build — demand intake, catalogue, proxies, retrieval. Wave 10 built the spine as a LIBRARY; the 2026-07-31 deploy proved apps/api mounts no collection route, so wave 13 items ship their api-shell mount as part of the build, not as later wiring.
- 2026-07-31 — built (wave 13, PR #171): POST /collection/demands — the FIRST real lane seam through FML-1202's createSeamRouter, and the first use of FML-1204's declared idempotency rule (spec x transform x horizonSet, order-insensitive via the function form), so four customers wanting the same series collapse to ONE demand carrying four demandRefs. demandRef is opaque: no path parses, splits or resolves it (structural test over both the pure module and the router). Position-blind 422 on a DEEP walk (objects and arrays, any depth), with the other side tested too — an instrument named as a thing to gather is accepted, only holding-shaped FIELDS are rejected. COVERAGE IS ANSWERED PER ASK (main-session ruling): freshnessContract lives on the ask, never on the identity, so the Portfolio Loop asking at 86400s and Hunt asking at 60s read served and gap in the SAME response — collapsing to the tightest was rejected because it would force 60s collection on a customer happy with a day, a policy collection was never given. Every gap carries a cause and a causeless gap does not type-check. No verdict field anywhere. VERIFIER CAUGHT THREE BLOCKERS, all confirmed by the main session driving real HTTP against the built shell and all fixed: (1) the factory's internal base path /pos-collection/demand was a live route that bypassed the register write and then permanently 409'd the legitimate customer — now sealed with the lane's own 404; (2) a caller-supplied filterKey parked a demand in a slice the intake worker never claims while the next emit collapsed onto it and returned 200 OK — 'invisible rather than declined', the exact failure this item exists to kill — the lane now owns the slice unconditionally; (3) a later asker's freshnessContract was silently discarded. Also fixed: torn state on queue-down (the register now commits only on a 2xx), coverage accepts either id space, and a horizon mismatch reports source_configured_item_not_pulled rather than collected_for_wrong_universe (which §9 defines as symbol-list drift; NO path emits it now, because nothing tracks universes yet and a wrong reason sends someone to fix the wrong thing). Mounted in apps/api. deployed=built.
- 2026-08-01 — deployed=live. Rolled out at gitSha b450362 and VERIFIED ON THE CLUSTER: every endpoint this item declares appears in GET /api/routes on the running pos-api (91 mounted, UNDECLARED 0, UNMOUNTED 0), over real stores — /health/stores reports backing {documents: mongo, ledger: postgres, claims: postgres, graph: neo4j}. It was `built` only because the code had not been rolled out; the rollout closed that.

