---
title: "Event-Driven AI Beats Continuous AI"
slug: event-driven-ai
date: 2026-08-29
draft: false
description: "I set my portfolio review to run every hour and it starved the one GPU re-judging things that hadn't moved. Why the fix wasn't a smaller interval."
tags:
  - systems
  - workers
  - bounded-inference
  - deterministic
  - agentic
categories:
  - AI Systems Engineering
image: event-driven-ai.png
---

There's a feeling I get when I automate something that I've come to distrust, and it's the feeling that more often means more on top of it. When I first wired up the position review, the thing that re-reads each holding and asks whether my thesis still holds, I set it to run every hour, and the reason was pure gut: an hour felt attentive. A system that looks at my whole book every sixty minutes sounds like a system that's paying attention. What it actually was, was a system that spent a scarce, expensive resource re-judging a pile of positions that hadn't moved a cent since the last time it judged them, and it took a self-inflicted outage to teach me that "attentive" and "continuous" are not the same word.

This post is about the difference between an AI system that runs on a clock and one that runs on events, and why, when the intelligence is expensive, that difference is the whole ballgame. I've spent this series on the [26B model at the center of pOS](/p/the-weekend-brief/) and the [single GPU slot it runs on](/p/the-router-translates-nothing/). Continuous AI is what starves that slot. Event-driven AI is what feeds it only when there's something worth feeding it.

## The Timer Was the Bug

Here is the anti-pattern in its purest form, and I built it on purpose thinking it was the responsible thing to do. A worker woke up on an interval and, every time it woke, ran the expensive model over every position in the book. Not the positions that had changed. All of them. The header comment I eventually wrote on the module that killed this design says it plainly, and I'm going to quote it because it's the thesis of the entire post:

```typescript
/**
 * loop-triggers -- retire the timer, wake the review on a REAL EVENT.
 *
 * WHY THIS MODULE EXISTS. The review ran every sweep interval over the WHOLE
 * book -- a HIGH-GPU 26B agentic pass re-judging positions that did not move.
 * That is a GPU bill with almost no signal. The fix is NOT a smaller interval:
 * it is a CHEAP arithmetic gate in front of the expensive tier, so the GPU is
 * spent once per REAL move.
 */
```

What the timer produced, at load, was a flood. Every held position escalated to the full thinking-on 26B review on every sweep, and that model serves a [single inference slot](/p/the-router-translates-nothing/), `LLAMA_CPP_N_PARALLEL=1`, so the slot got pinned by a queue of long, rambling reviews, one of them decoding tens of thousands of tokens in a single turn. And while it was pinned, every other thing that needed the model, the research pass, the sleeve designer, the weekend brief, sat behind the flood and eventually gave up:

```
transport error calling nuance: This operation was aborted
```

That string is what the failure actually looks like from the outside. It comes from an `AbortController` firing on a five-minute transport timeout, and once the one slot is backed up past five minutes, everything downstream of it starts throwing that line. One badly-shaped timer, re-judging things that hadn't moved, and the entire model tier browns out. Every individual review in that flood was a correct thing to compute. Run continuously over an unchanged book on one slot, the correct calls compose into a starved tier that can't answer anything. Locally sensible, globally an outage, in the relations between the parts.

## The Fix Everyone Reaches For Doesn't Work Here

The instinct when a worker can't keep up is to add workers. Scale out. That's the reflex a decade of stateless web services trained into me, and it's exactly wrong when the bottleneck is one GPU, because the pods aren't the scarce thing. The slot is. I wrote the scaler to refuse the reflex on my behalf:

```typescript
if (policy.resourceClass === 'gpu-bound') {
  // depth is NOT a scaling signal ... throughput is arbitrated by the shared
  // model-serving queue (model-side, not pod-count). So the desired count is the
  // declared concurrency floor -- max(minReplicas, 1): depth NEVER pushes past it.
  return Math.max(policy.minReplicas, 1);
}
```

For a GPU-bound worker, queue depth does not scale the pod count. It can't, because ten pods all talking to one slot don't finish faster than one pod does. They just deepen the same queue and make the aborts worse. So the only lever that actually relieves a flooded model tier isn't more capacity. It's less work. And the only honest way to do less work without doing a worse job is to stop doing the work that didn't need doing, which means stop running the model on a clock and start running it on events.

## An Event Is a Reason

So the review got a gate in front of it, and the gate is deliberately, aggressively dumb. Before any position reaches the 26B, a piece of pure arithmetic asks one question: did anything actually happen to this position? Not "has an hour passed." Did the price move enough to matter, or did real news land on it? A move of a couple percent intraday, a larger move close-over-close across days, or a fresh piece of high-sentiment news. If none of those is true, the expensive tier never runs, and the position is skipped, cheaply, in microseconds, by code that holds no model at all. The pass reports what it did in three numbers, `evaluated`, `fired`, and `skipped`, and on a quiet day almost everything is skipped.

That gate is the same [deterministic-bread instinct](/p/the-deterministic-sandwich/) from earlier in the series, pointed at cost instead of correctness: cheap, boring, checkable code standing in front of the expensive probabilistic thing, deciding whether it even gets to run. The model is the most expensive component I own. The right amount of it to run is the least I can get away with, and "an hour elapsed" is not a reason to run it. "This position moved" is.

And the deepest version of the event isn't even a price. It's a change in what I believe. The review worker's real trigger is a claim off a queue, and the queue is fed by [the Brain](/p/the-living-thesis-graph/) whenever a thesis changes:

```typescript
const LOOP_RECORD_TYPE = 'thesis-change';
```

When a belief about the world updates, that's an event, and it lands as a claimable record that wakes exactly the positions that belief touches. That's the whole shape I want. Something real happens, a price breaks or a thesis shifts, and the expensive machinery wakes for that specific thing and nothing else. The rest of the time it's asleep, and the GPU is free for the caller that has an actual reason to want it.

## Underneath, the Worker Was Always Event-Shaped

The nice part is that the worker runtime never wanted a timer in the first place. The [bounded worker](/p/is-this-even-an-agent/) at the bottom of every lane in pOS is a claim loop, not a poll loop. It asks the queue for a unit of work, and the only time it sleeps is when the queue is empty:

```typescript
const lease = await this.cfg.client.claim(this.cfg.filter, leaseSeconds);
if (lease === null) {
  return { kind: 'empty', at: this.cfg.now() };   // nothing claimable -> back off
}
// ... and in the loop:
if (result.kind === 'empty') {
  await this.sleep(delayMs, shouldStop);
  delayMs = Math.min(backoff.maxMs, Math.round(delayMs * factor));  // back off when idle
} else {
  delayMs = backoff.initialMs;   // had work -> claim the next immediately
}
```

An idle worker backs off exponentially, up to thirty seconds between checks, so an empty system costs almost nothing. A busy one claims the next unit the instant it finishes the last, with no delay at all. The cadence is driven by the arrival of work, not by a clock I picked out of a hat. Even the infrastructure agrees: the pods scale to zero on an empty queue and a scaler wakes one the moment a record arrives, so a lane with nothing to do isn't running at all. The timer I bolted onto the review was fighting the grain of a system that was event-driven from the queue up. I'd taken an event-shaped runtime and put a clock on top of it, which is the worst of both.

## Where This Stops

I want to be straight about the two places this doesn't save me, because it would be easy to read all this as solved.

The first is that event-driven only moves the hard problem, it doesn't erase it. A system that runs on events is exactly as good as its triggers, and a trigger is a judgment call wearing arithmetic's clothes. Set the move threshold too high and a position slides into real trouble without ever crossing the line that wakes the review, and I find out late. Set it too low and I'm back to a flood, just a slightly more expensive one. The gate turned "how often should this run" into "what counts as something happening," which is a better question, but it's still a question I have to answer with judgment, and I can get it wrong in a way no amount of architecture will catch for me.

The second is smaller and more embarrassing: some of my cheap sweeps still fire on a plain interval with no guard against overlapping themselves, so the exact "a slow pass laps itself and piles onto the one behind it" failure I've been describing is still structurally possible in the corners I haven't converted. What saved the position review wasn't a lock that made overlap impossible. It was making each pass cheap enough that overlap stopped mattering. That's a real fix and I stand by it, but it's mitigation, not a proof, and the honest state of the system is that the event-driven discipline is fully paid off in one place and still owed in a few others. I bought the GPU back by spending it only on things that actually happened. I have not yet made it impossible to waste it again.
