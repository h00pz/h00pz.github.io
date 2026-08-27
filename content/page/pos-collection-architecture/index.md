---
title: "Subsystem Architecture: pos-collection"
slug: pos-collection-architecture
description: "A complete, real PortfolioOS subsystem architecture document, reproduced as the worked example for The Architecture Method."
---

This is a complete, real subsystem architecture document from PortfolioOS, reproduced exactly as it's written in the repository. It's the worked example for the post [The Architecture Method: Argue First, Write Second](/p/the-architecture-method/), which describes the process that produces documents shaped like this one. Cross-references to other pOS documents are left as plain filenames, because those documents aren't published here.

---

**Standing architecture document.** The lane that gathers. It measures and preserves what the system has
said it depends on, and it says loudly when it cannot. Seam contracts live in
`seam-collection.md`. This document is everything inside them.

**Living document.** Architecture changes are argued between the operator and the main session before
they are made.

> **This document describes the DESIRED END STATE, never the current one.**

> **This lane is autonomous.** It never escalates to the operator. Only the two loops do.

**Supersedes `pos-market-intel` and `pos-evidence`**, which were one lane split by where their output
landed.

**What it must serve** is stated in three registers, one per customer, plus the inventory that organises
all of them by how each thing is obtained:

| document | derives the requirement from |
|---|---|
| `collections-position-register.md` | **the capital** — winds, both directions, per position |
| `collections-brain-register.md` | **the Brain** — regime proxies, cycle inputs, the frame, bellwethers, artifacts |
| `collections-huntpack-register.md` | **the packs** — what each screen or agent runs on |
| `collection-inventory.md` | **how it is gathered** — the five kinds, and what that costs |

Original derivation: `collections-initial-demand-set.md`.

---

## 1. What collection is for

> **Collection gathers what the system has said it depends on, and says loudly when it cannot.**

One job, and a second half that is not optional: **gather it, and check that it is gathering it.**
Collection health is a first-class output of this lane, not telemetry bolted to its side.

**Everything it produces is one of two things:** a **value** — with a unit, a timestamp and a source — or
an **artifact**, preserved immutably and chunked so that anything downstream can cite *this span* rather
than *that article somewhere*.

### Why it is one lane

Market-intel produced series; Evidence produced documents. That is a difference of **record shape**, and
`platform-persistence.md` §1 already rules shape out as a lane boundary — *a
single lane routinely spans three engines*. The home office keeps a versioned plan, a committee argument
and a household close, and nobody proposes splitting it into three.

Everything else about them was the same job: both fetch from outside, both are blind by design, both are
demand-served by the same customers with the same record, both declare a freshness contract per thing
collected, both cross one governed egress boundary.

**And two catalogues cannot answer the question that matters.** *Collected and unread* is the leading
indicator of the expensive failure — a series exists that nothing touches, so the cost is already being
paid while a dashboard of healthy collectors says everything is fine. With two registers, each can report
itself healthy while the gap sits between them. **One catalogue makes the question answerable across
everything the system gathers.**

---

## 2. The boundary — gather versus assess

This is the axis the whole architecture runs on. Hunt finds, the Committee argues. Collection gathers,
the Brain interprets. Portfolio records, the Portfolio Loop judges. **No lane grades its own homework.**

The test is **not** *is it computed*. Plenty of what collection produces is computed.

> **The lane that owns the assumptions owns the output — even when the arithmetic between them is
> mechanical.**

And there is a checkable proxy for it:

> **Does producing it require a chosen threshold, a chosen weight, or a chosen taxonomy?**

`crack.diesel = (heating_oil × 42) − wti` has none — forty-two is gallons in a barrel. A z-score, a
percentile against history, `GDX ÷ gold`, market cap ÷ GDP, the inside-versus-outside-the-wall spread:
all arithmetic over gathered inputs, however many steps deep. **All collection's.**

The regime matrix is the worked counterexample. Twelve buckets, thirty-seven proxies, momentum blended
across three windows, voting into four quadrants — fully deterministic, and its config states
`regimeSensitivity: {reflation: positive}`, which is a **stated belief about how the world works**,
alongside chosen weights, a chosen vote threshold and a chosen taxonomy. **So regime is the Brain's, and
collection serves the thirty-seven proxies.**

| collection | the Brain |
|---|---|
| prices, series, spreads, ratios, z-scores | **regime · cycle stage** |
| the article, preserved and citable | **what the article means** |
| a third party's published call, attributed and dated | whether to believe it |
| positioning series | *"this trade is crowded"* |
| bellwether results | **what they say about the economy** |
| collection health | risk composites, horizon reads, the brief |

**Composition is not interpretation.** *"190% means expensive"* is not collection's. *190%* is.

### Blind twice over

Market-intel was position-blind; Evidence was thesis-blind. **One lane is both**, and it is stronger
stated once:

> **The collector never learns why anyone wants this.**

A demand names an instrument and a transform, never a position. An artifact source is fetched because it
is on the register, not because of what it might say. **A lane that knows which answer is wanted will
find it** — not through dishonesty, but through the ordinary gravity of relevance.

The line is finer than it looks and has to be defended precisely: reading an article and noticing *"the
CTO left"* is **not** collection. It is reading, and reading is analysis. Collection keeps the article;
the Brain notices what is in it.

---

## 3. Three sources of demand

| source | how it arrives |
|---|---|
| **implicit — holding** | **holding something is the demand.** Every instrument in the book must be marked. Portfolio never asks — it holds positions, and holding generates the requirement |
| **implicit — watching** | **watching something is the demand.** Every subject the Hunt Loop tracks is priced and its news followed. The loop never asks either |
| **demanded** | a customer states a need |
| **designated** | **the Brain names a subject worth reading** — the bellwether set (§7) |

**Two suppliers, one rule: the state of a lane generates the requirement.** Portfolio's being implicit is
what keeps the ledger honest — no judgment leaks into a lane whose job is recording, and the most
important gathering set in the system needs nobody to remember to request it. The Hunt Loop's is the
same shape one step earlier.

> **A subject watched for eight months already has eight months of price history and news when the
> Committee finally says yes.**

Nothing starts blind on the day it matters most, and a subject becoming a position changes nothing about
collection's behaviour — the ticker moves from one implicit supplier to the other.

**The reading is asymmetric and deliberately so.** Both sets are classified cheaply; **the Brain's heavy
read of an article is reserved for held positions.** Before capital, arithmetic is enough.

### The customers

| customer | demands |
|---|---|
| **the Portfolio Loop** | declared winds and their transmission chains |
| **the Hunt Loop** | conditions written against a metric |
| **Hunt** | **what its packs need gathered** — market structure, the filings corpus, flow rotation. A pack that declares what qualifies also knows what it must read to decide, so **stating the requirement is Hunt's job, not collection's guess** |
| **the Brain** | what a thesis branch rests on, **the frame** — curve, spreads, breadth, liquidity — and **the bellwether designation** |
| **the Committee** | one-shot research for a starving seat (§8) |
| **AEP** | **bars — intraday, and deep.** One timeframe for running a live strategy, a long history for backtesting. **The only customer whose profile is sub-daily** |

> **Working out what needs gathering is not collection's job.** A wind names what would have to be
> measured; a pack knows what it screens on. **Hunt turns both into a stated requirement**, and that
> requirement arrives here as a demand like any other — with collection never learning which pack asked
> or why. `hidden-compounders` needs no special case: it states its universe rule and its inputs,
> collection publishes the metrics, and **the pack keeps the threshold.**

**Collection's job is set by its customers.** There is no privileged tier it maintains on its own
initiative — **the Brain is the customer whose job is looking at the whole**, which is what stops a
demand-driven service being blind to everything the book does not already own.

**Precollection is excluded from standing collection.** A metric gathered for a specific seat belongs to
that job, and lands in that requester's registry (§8).

---

## 4. The catalogue

The register of everything that can be gathered, and the artifact that makes gaps visible.

| field | |
|---|---|
| id, name, unit *(a value)* or modality *(an artifact)* | |
| **kind** | `feed` · `scrape` · `computed` · `agentic` · `artifact` |
| **source** | where it comes from, or **none** for a computed instrument |
| **freshness contract** | its expected cadence — **declared per thing, never one global number** |
| **horizons** | which horizons it carries information at (§6) |
| **demanded by** | **`demandedBy[]`** — every customer that asked, not one. Four lanes wanting the same series produce one entry carrying four refs |
| **state** | below |

| state | meaning |
|---|---|
| **served** | gathered, fresh, within contract |
| **stale** | a contract is being missed |
| **proxied** | served indirectly, declared, with a validation record (§5a) |
| **manual** | **in the registry by hand, no collector yet** — a graduation candidate (§8) |
| **unserved** | asked for, not available, **with its cause** |
| **available, undemanded** | known to exist, nothing has asked. Zero cost |

### One catalogue, many views

**There is one catalogue, and it is filtered — never one per lane.** The temptation is real: the packs,
the Brain and the book each derive their requirement differently, so a register each looks natural.

> **It recreates exactly the split this lane was formed by removing.**

*Gathered and unread* is the question that justifies the catalogue, and it is **only answerable across
everything at once.** With a register per lane, each reports itself healthy while the gap sits between
them — a series the Brain stopped reading looks fine to the Brain's register and invisible to everyone
else's.

**Filtering costs nothing because the provenance is already there.** `demandedBy[]` names every customer,
so *what does the Brain depend on* and *what would break if the packs stopped running* are **views over
one register**, not separate stores:

| view | asks |
|---|---|
| `?demandedBy=brain` | what the Brain's reading rests on |
| `?demandedBy=portfolio-loop` | what the book's winds are measured by |
| `?demandedBy=hunt` | what the packs run on |
| `?state=unread` | **what nothing anywhere consumes** — and this one must not be filterable by lane, because a lane cannot see its own absence of readers |

**The three derivation documents are a different artifact.**
`collections-position-register.md`,
`collections-brain-register.md` and
`collections-huntpack-register.md` are **arguments** — how each
customer's requirement was derived, and why each line exists. The catalogue is **live state**. Once it
runs, the registers stop being maintained against it and become the record of how the demand set was
arrived at. **Two things that must never be kept in sync, because only one of them is true.**

> **An hourly bound is right for a liquid equity and meaningless for something that prints once a day.**
> A collector that silently stopped becomes a **broken contract** rather than a series that merely looks
> quiet — which is how *stale crons* stops being a failure class.

**A bar request returns a reproducibility snapshot.** A backtest asking *what did we know when this ran*
is the same question a revised GDP series asks, and the bi-temporal store already answers it. **A result
whose data cannot be re-served is not evidence** — which is why the digest is part of the response rather
than something the caller reconstructs.

**Instrument identity is versioned.** A redefined series is a different series: change a crack spread's
formula or a proxy's inputs and every comparison across the change is silently wrong.

---

## 5. The five kinds

**Adding something to gather is a definition, not a pull request.** Directly modelled on Hunt's pack
framework, for the same reason: the lane's value is in how easily its coverage grows.

| kind | what it does | output | model |
|---|---|---|---|
| **`feed`** | pull a structured source — prices, FX, FRED, EIA, exchange data | a value | none |
| **`scrape`** | pull a structured page — a calendar, a customs table | a value | none |
| **`computed`** | **an expression over other instruments.** No source at all | a value | **none — structurally** |
| **`agentic`** | an agent reads an unstructured source and **extracts a stated value** | a value | yes |
| **`artifact`** | fetch and preserve a document, chunked and addressable | **a registry item** | none |

### The kind enforces the boundary

**`computed` has no model field.** It can reference other instruments and arithmetic, and nothing else.
So *composition is not interpretation* stops being a rule somebody has to remember and becomes a schema
constraint: **if producing it needs a model to form a view, it is not a collector.**

**`agentic` extracts; it never concludes.** Its output has the same shape as a feed's — a value, a unit,
a timestamp, a source — and the source is **the span it was read from**, so the number stays checkable
rather than trusted. That is cite-or-reject applied to a number instead of to text. **An agent that
returns prose is not a collector.**

**`artifact` is the only kind whose output is not a value.** It preserves a document so a claim can be
traced to a sentence, and it never says what the document means.

### Authoring a collector is a conversation

**Adding something to gather is a definition, not a pull request — and the definition is written by
talking.** The operator says what he wants measured; **Samantha shapes it into the format collection
needs**: which kind it is, the source or the expression, the unit, the cadence and freshness contract,
and which horizons it actually carries information at.

> **`cockpit → Samantha → cockpit → API`. Collection receives a valid definition and never learns a
> conversation happened.**

Samantha is in that loop because the definition has to be right **in this lane's terms**, and those are
the terms most likely to be got wrong from outside. Is this a `feed` or an `agentic` read? What unit —
and does the source publish it in that unit? Which horizons does this measure genuinely speak at?
**A collector authored with the wrong horizon runs perfectly and lies**, because the read layer will
serve it to callers it has nothing to say to.

**The same authoring loop as a Hunt pack**, deliberately. Both extend a pluggable framework without a
code change, both end in schema-forced JSON, and in both cases the receiving lane sees only the artifact.
Hand-writing one is identical.

### Adding diesel takes minutes

```yaml
- id: crack.diesel
  kind: computed
  expr: (heating_oil * 42) - wti
  unit: usd_per_bbl
  horizons: [now, short]
  demandedBy: energy-complex
```

**No code, no deploy, no source.** That is the test the architecture has to pass, because the reason to
measure something usually arrives after the system was built.

### Agentic is where the conviction is

Some of the highest-value things in the inventory cannot be bought: **signed-but-not-commenced leases**
(footnote 14, $388bn → $662bn in three months, on no balance sheet) · days payable and useful-life
assumptions · **interconnection queue lengths** · AISC per miner · **take-or-pay contracted share**.

> **The only class the system must *read* rather than fetch — and where the highest-conviction signals
> live, because a disclosure a company had to make is worth more than a number a vendor chose to sell.**

**It is also where the cost side lives.** Feeds and computed expressions mostly serve revenue and price —
what goes up when a position is working. Reading filings serves cost, leverage and execution — what
breaks one. **A book instrumented only by feeds can be confirmed and never falsified.**

### An absence is an observation

*"Nvidia does not offer customer financing, as of this 10-Q"* is a **finding**, with a citation and a
date. If only values are stored, *checked and it is not there* and *never checked* are
indistinguishable — and the cleanest binary in the book becomes unfalsifiable.

### A headline is not a document

Per-subject news yields **headlines**, and you cannot cite a span in a headline. So it produces a count
and a headline stream — **an observation** — while article sources produce artifacts. Two kinds, one
word.

## 5a. Proxies

Some things cannot be measured directly, or only at a price not worth paying. **The answer is a proxy,
declared as one.** `GDX ÷ gold` stands in for gold-miner AISC: free, daily, two series already held.

**The operator declares the proxy, with Samantha's help, and hands it to collection to gather.** The
belief is authored outside this lane; collection executes it and never forms one. Same shape as a pack
definition.

| rule | |
|---|---|
| **it names what it proxies** | the wind still says *AISC*; the instrument says *proxy for AISC* |
| **it carries an assumed regime** | `GDX ÷ gold` tracks cost pressure normally and moves for other reasons in a financing-driven mining selloff. **A proxy can decouple exactly when it matters** |
| **it does not turn a wind green** | *proxied* is its own coverage state |
| **it is validated** | cheap direct measurement at low frequency validates a free proxy at high frequency — read four miners' actual AISC quarterly and confirm the proxy still tracks |

> **A proxy that is never validated is a belief**, and this architecture already has a word for those.

---

## 6. Horizons are declared per measure

**Not a uniform grid.** A measure declares which horizons it carries information at, and **a consumer
asking outside that range gets nothing rather than a number.**

| measure | horizons |
|---|---|
| ETF and fund flows · VIX and its term structure | now · short |
| credit spreads | short · medium |
| curve, real yields, net liquidity | medium · long |
| **Buffett indicator, CAPE** | **long · long+** |

The Buffett indicator is why this matters: **almost no short-horizon information and real long-horizon
information.** Without a declared horizon it gets read as a reason to act this week.

**Silence beats a number that does not mean what the reader thinks.**

---

## 7. Bellwethers — a subject, not an instrument

A company tracked because its results say something about the **economy** — freight volume, dealer
inventories, delinquency rates, temp placements.

**It inverts the rule the rest of the lane runs on.** Everything else is gathered because the household
owns something or the thesis claims something. A bellwether is gathered because it **reads on the
world**, and the book may hold none of them.

> **The Brain declares the bellwether set. Collection gathers it.**

Which companies read on the economy, and which number inside each carries the signal, is a stated belief
about how the world works — so it belongs to the lane that owns the assumptions. Identical shape to Hunt
declaring a pack threshold while collection publishes the metric, and to the operator declaring a proxy.

**Three kinds serve one bellwether:** price is a `feed`, published operating statistics are a `scrape`,
and the number that matters is usually **`agentic`** — mix, ticket versus traffic, cancellation rates and
dealer inventories live in the release and on the call, not in tagged data.

**A bellwether is not a Hunt candidate.** Hunt finds what is worth owning; a bellwether is read and need
never be owned. **And a held position can also be a bellwether**, with two separate readings — GOOG's
winds are cloud growth and capex intensity, while as a bellwether the signal is what its ad revenue says
about discretionary corporate spend. **Shared subject, separate interpretation.**

---

## 8. Where output lands

| destination | what lands there | who reads it |
|---|---|---|
| **observations** | every `feed`, `scrape`, `computed` and **`agentic`** output | everyone, as facts |
| **the world-of-money registry** | standing `artifact` collectors on macro sources, **and everything the operator ingests by hand** | **the Brain claims and interprets** |
| **the equity registry** | one-shot research for a named Committee seat | the Committee and Hunt. **The Brain never reads it** |

**The registry split is not about who gathered.** Custody is shared beneath both — one immutable copy,
addressable, *shared source ≠ shared interpretation*. What differs is where the **record** lands and who
interprets it.

> **Originating incident: Committee research was filed into the world registry and it wrecked the
> thesis.** Everything in that registry is interpreted by the Brain against the thesis, so one company's
> owner-earnings pressured a thesis about the world of money. **A macro thesis must not move because of
> one company's quarter.**

**Which is why an `agentic` output is an observation and not a registry item.** Reading footnote 14 to
extract a lease figure produces a number; the 10-K is custodied and referenced but never becomes
something the Brain interprets against the thesis. The boundary is structural rather than remembered.

### Manual ingestion is an on-ramp, and it is meant to empty

**Not everything in the world-of-money registry is gathered.** The operator comes across an article, a
research paper, a report that belongs in the thesis, and puts it in by hand — as a URL, pasted text or an
uploaded file. That path is **first-class and permanent**, and it is the only way material with no
collector reaches the Brain.

> **The goal for any given source is to graduate it out of manual and into one of the five kinds.**

**An ingest carries one routing flag, and its default is off.** Most material is thesis material and goes
to the world registry for the Brain to read. **Toggled on, the document is also read for the trades it
names**, and those become candidates into Hunt.

> **The operator is the router.** He knows a report names trades; he says so. No classifier guesses, and
> nothing in this lane decides what a document is for.

Which makes the stream itself a signal: **a source the operator keeps feeding by hand is a missing
collector stating its own need.** Manual items therefore carry their source rather than arriving
anonymously.

It is the one class with **no cadence** — it arrives rather than being fetched, so it can never be stale
or unserved. And for a pasted document or an upload, **custody is the only copy**: not a convenience, the
artifact itself.

### Retrieval — cite or reject

Artifacts are served by **cite-or-reject** retrieval: an answer arrives with its citations or it does not
arrive. There is no *here is what I found, roughly*, because an ungrounded answer that looks grounded is
worse than silence — it is silence you cannot detect.

This is the lane's read surface for artifacts, exactly as the series reads are its surface for values.
**One lane, two shapes, one contract.**

---

## 9. Demands, and what an unserved one costs

An unserved demand **carries its reason**, because the reason decides the fix:

| cause | fix |
|---|---|
| **wrong series under a right-looking name** | **a correction, and it goes first** — a present series read as the missing one is worse than an absent one |
| **collected but unwired** | **a wire.** Cheapest and most embarrassing |
| **source configured, item not pulled** | configuration. Nearly free |
| **collected for the wrong universe** | re-scope — a symbol list that drifted from the book |
| **manual, wants a collector** | graduate it into a kind |
| **never built** | genuine new capability |
| **broken** | an operational alert. Nothing new is needed |
| **never asked** | a question for a person |
| **costs money** | a price and a proxy alternative, decided visibly |

### What is not an unserved demand

Some winds have **no possible instrument** — a strait staying open, a succession, a jurisdiction turning
hostile. Recording those as *never built* implies a capability someone could deliver.

> **They are not collection's. They route to the Brain as thesis branches**, where a branch with no
> evidence either way is already classified **blind-spot**.

The wind stays declared on the position and is measured by a thesis state instead of a series. **Nobody
keeps trying to source it.**

---

## 10. Checking that it is gathering

**The second half of the one job.** Two queries over the catalogue, both cheap:

| query | finds |
|---|---|
| **demanded and unserved** | somebody asked, we cannot gather it |
| **gathered and unread** | **something exists that no signal, no consumer and no reader touches** |

The second is the leading indicator of the failure the loops later find the expensive way, and it is
**why the two lanes had to merge** — with separate registers, a substack fetched weekly and read by
nobody is invisible to the series catalogue, and vice versa.

Two live instances: **oil is gathered as `USO` and nothing reads it**, and **`moveIndex` is gathered
while the regime read reports `volatility:MOVE` missing** — for which an entire freshness-quorum design
was written to *tolerate* an absence that is not one. **The wire was cheaper than the workaround.**

### What this lane structurally cannot know

**A demand-driven service cannot know what nobody asked for.** Collection will never notice that credit
is unwatched. That belongs to the customers' coverage reads — both loops and the Brain have one.

What makes those reads possible is the **available-and-undemanded** register: a customer can only notice
credit is unwatched if it can see what credit instruments exist. **Registered, never gathered**, at zero
cost until something asks.

---

## 11. What collection owns

| record | |
|---|---|
| **the catalogue** | what can be gathered, its kind, source, contract, horizons and provenance |
| **collector definitions** | the pluggable configuration |
| **observations** | every gathered value, with **timestamp, source and `knownAt`** |
| **releases and revisions** | **what was known when it was known** |
| **the calendar** | what prints, when, consensus, prior — forward-looking, and itself a signal. Collection owns the STORE + the scraped feed; the calendar is now a first-class shared subsystem read by thesis/regime/brief and fed a second, harvested feed — see `subsystem-forward-calendar.md` + `seam-forward-calendar.md` |
| **signals** | deterministic transforms and compositions |
| **proxy declarations** | what stands in for what, its assumed regime, its validation record |
| **custody** | the immutable, chunked, content-addressed copy of every artifact |
| **the world-of-money registry** | canonical records of collected and hand-ingested material, with provenance |
| **the retrieval index** | what makes cite-or-reject possible |
| **collection health** | fresh, stale, failed, against contract |
| **demands** | raised, served, proxied, unserved with cause |

**Not collection's:** regime · cycle stage · risk composites · horizon reads · the brief · what any
artifact means · the bellwether *designation* · anything position-aware · the equity registry's contents.

---

## 12. Worker design

| worker | wakes on | claim filter | model |
|---|---|---|---|
| **feed collector** | a thing's cadence | `kind=feed` | **none** |
| **scrape collector** | a calendar entry, or cadence | `kind=scrape` | **none** |
| **compute** | an input instrument updating | `kind=computed` | **none — structurally** |
| **agentic collector** | cadence, or a filing landing | `kind=agentic` | yes |
| **artifact collector** | freshness — a source is due | `kind=artifact` | **none** |
| **research** | a one-shot request from a seat | `research` | light |
| **classify** | headlines arriving for a tracked subject | `classify` | FinBERT — **a trigger, never a judgment** |
| **intake** | a demand arriving | `demands` | **none** |
| **health** | continuously | `health` | **none** |

**The worker is trivial because the lane has one job.** Claim, fetch or compute, timestamp, store, report
whether it worked. No thresholds, no interpretation, no position awareness — all of it was moved to lanes
allowed to hold a view.

**Two economics, one implementation.** Deterministic collectors are CPU-cheap and idle-schedulable;
agentic collectors read documents. If filings gathering backs up while feeds idle, **only that class
scales** — which is the whole reason the claim filter is `kind`.

**Artifact collectors are I/O-bound and scale by adding pods.** Content addressing makes duplicate
gathering harmless: two workers fetching the same article produce one record.

Every worker claims a lease through the central API and holds no database connection. Model calls go
direct to model-serving.

---

## 13. Doctrines

| doctrine | why |
|---|---|
| **Collection gathers; it never assesses** | a lane that analyses its own material gathers what its conclusions want |
| **The lane that owns the assumptions owns the output** | even when the arithmetic between them is mechanical |
| **The collector never learns why anyone wants this** | position-blind and thesis-blind, stated once |
| **Composition is not interpretation** | a spread, a ratio and a z-score are arithmetic |
| **Holding is the demand** | portfolio asks for nothing and generates the most important requirement |
| **A demand names an instrument, never a position** | blindness survives a book-driven priority |
| **Adding something to gather is configuration** | the reason to measure arrives after the system was built |
| **A collector is authored by conversation** | the definition has to be right in this lane's terms, and a wrong horizon runs perfectly and lies |
| **Working out what needs gathering belongs to the asker** | a pack that knows what qualifies knows what it must read |
| **An agent that returns prose is not a collector** | the output is a value, a unit, a timestamp and a source |
| **An extracted value carries the span it came from** | cite-or-reject, applied to a number |
| **An absence is an observation** | otherwise *checked* and *never checked* are the same record |
| **A headline is not a document** | you cannot cite a span in one |
| **A proxy is declared, and never reads as the thing it stands for** | an unvalidated proxy is a belief |
| **Horizon is declared per measure** | silence beats a number that does not mean what the reader thinks |
| **Freshness is a contract per thing gathered** | a stopped collector is a broken contract, not a quiet series |
| **Store what was known when it was known** | revisions make a naive backtest lie |
| **Preserve before interpreting** | a conclusion whose source has changed cannot be examined |
| **Collection owns the only egress** | one hardened boundary is worth more than two, and material nobody custodied cannot be re-examined |
| **Shared source, separate interpretation** | one custodied copy, two registries, two readings |
| **Cite or reject** | an ungrounded answer that looks grounded is worse than none |
| **Manual ingestion is an on-ramp that is meant to empty** | a source fed by hand is a missing collector stating its need |
| **One catalogue, filtered — never one per lane** | *gathered and unread* is only answerable across everything at once |
| **Gathering and checking that it gathers are one job** | not telemetry bolted to the side |

---

## 14. Degradation

| absent | collection behaviour |
|---|---|
| a source | that thing goes **stale against its contract** and says so. **No substitute is silently used** |
| the ibeam gateway | price and FX gathering stops. **There is no second price source** |
| the egress gateway or SearXNG | **agentic and artifact collectors stall visibly.** Feed, scrape and computed are unaffected. **No other lane has a second path out**, so this absence is total — and total is honest |
| model-serving | agentic gathering and classification **queue**. Everything deterministic is unaffected |
| an input to a computed instrument | the computation **does not run.** It never substitutes a stale input for a fresh one |
| a demanded thing that cannot be obtained | recorded **unserved, with its cause**, and a proxy is offered where one exists |
| the Brain | the registry keeps filling, un-interpreted. **Collection does not guess at meaning in its place** |
| portfolio | the held set cannot refresh; **new holdings go unmarked and are reported missing.** The book is never guessed |
| a requester | the layer is produced and lands in their registry; nothing is lost |
| a customer | nothing changes — collection does not stop because nobody read it today. **`unread` will say so** |

**Nothing here estimates.** The rule is uniform and it comes from one failure: **a missing record
announces itself and a stale one does not.** A price from Friday returned on Tuesday with no timestamp is
indistinguishable from a correct one, and everything computed on top of it is confidently wrong.

---

## 15. Open design questions

1. **Does the catalogue enumerate at universe scale?** ~125 book-and-thesis instruments enumerate with a
   source, contract, horizons and provenance each. Four thousand companies × seven compounding metrics do
   not, on the same model. Either the catalogue registers **classes** at that scale, or universe-scale
   computation is registered once rather than per instrument.
2. **The compounding metric definitions** — ROIC how, invested capital how, trend over what window.
   Hunt's `hidden-compounders` hangs off them and nothing can be versioned until they exist.
3. **Is per-subject news bound to held positions only, or also to the Hunt Loop's tracked set?** Thirty
   versus thousands — a different collector either way.
4. **How are proxy validations stored** — as observations on the proxy instrument, or as their own
   record? They are evidence *about* an instrument rather than a measurement of the world.
5. **How deep does audio handling go?** A transcript must exist before anything else can happen, and a
   produced transcript is not the same artifact as a published one.
6. **Which paid sources**, and the commercial question behind them.
7. **Does the calendar own regulatory and corporate dates**, or only economic releases? A statute with a
   date behaves identically to a print, and *"the floor arrives before the substitution"* is only
   expressible if both clocks are in one place.
