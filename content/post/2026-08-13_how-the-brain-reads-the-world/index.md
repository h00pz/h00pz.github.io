---
title: "How the Brain Reads the World"
slug: how-the-brain-reads-the-world
date: 2026-08-13
draft: true
description: "The job I most wanted off my plate was reading the news into my thesis. It's also the one where a model most wants to invent, so it runs inside a cage."
tags:
  - ai
  - architecture
  - systems
  - pos
categories:
  - AI Systems Engineering
image: how-the-brain-reads-the-world.png
---

The part of writing my old market letter that actually broke me was never the writing. It was the reading. Every week I'd wade through news, substacks, and podcasts looking for the handful of things that bore on what I already believed, and then do the harder thing, which was deciding what each one meant for the thesis: did it support the view, weaken it, or actually threaten it, and at what horizon. That judgment, made a hundred times a week across a dozen half-formed beliefs, is the cognitive load that ended the letter. So when I built [the thesis graph](/p/the-living-thesis-graph/), the very next thing I needed was something to do that reading for me. This post is about that something, and about why it's the single scariest thing in the Brain to hand to a model.

## The Job, and Why It's Dangerous

The setup is bleak on its own. Evidence flows into the system, gets stored, and stops. A candidate piece of news lands in custody and nothing does anything with it, because the thing that's supposed to look at it and say "this bears on the credit thesis, it weakens the near-term branch" is the exact judgment I was trying to offload. Without that mapper, the thesis graph is a snapshot that ages. With it, the graph is a belief the world continuously argues with. The whole difference between those two is one job: read a new document, and decide what it means for what I already believe.

That job is dangerous to give a model for a specific reason. It's the place in the entire system where the model most wants to invent. Hand a model a news article and a list of your beliefs and ask "does this fit," and its instinct, unless you stop it, is to be helpful: to find a connection that isn't quite there, to decide a passing mention is a whole new thesis, to attach a claim to a branch it doesn't actually bear on because the words rhyme. Every one of those is the model quietly authoring your worldview instead of reading against it, and a worldview a model edits on its own initiative is worthless, because you can no longer tell your beliefs from its confabulations. So the mapper is built, from the ground up, to let the model read and forbid it from inventing.

## Two Rules I Paid for in v2

The design is shaped by two guardrails I did not arrive at cleanly. I learned both the hard way in v2, and they're the load-bearing constraints of the whole mapper.

The first is the granularity rule. The judgment about whether something is a *new* thesis is made on the whole document, never on a sentence. In v2 I let the system evaluate claims in isolation, and it went wrong the same way every time: a sentence ripped out of its article looks novel, because it's been stripped of exactly the context that would have placed it on an existing branch. Evaluate spans alone and you manufacture new thesis nodes endlessly, each one a fragment that already belonged somewhere. So the rule is absolute: the new-thesis judgment reads the entire document, and a span is structurally incapable of proposing a branch. A claim can attach to a belief. Only a whole document can suggest a new one.

The second is the write rule. Ninety-eight times out of a hundred, a new document doesn't imply a new tier-1 thesis, it just bears on beliefs you already hold. Occasionally, it genuinely does, and that's a moment that needs me. So the mapper routes on its own verdict: a confident attachment to existing beliefs lands live, autonomously, no human in the loop, because that's the common case and bottlenecking it on my attention would defeat the entire point. A no-fit, the rare document that doesn't map onto anything, surfaces to me as a signal that I might need to author a new node. The operator's judgment is spent in exactly one place: the genuinely new belief. Everywhere else, the Brain produces the output, not me.

## Pass One: Does This Fit at All

Those two rules give the mapper its shape, which is two passes. The first is a single whole-document call that makes one judgment, and its result type is the whole design in miniature:

```typescript
type FitGateResult =
  | { ok: true; fits: true;  branchIds: readonly string[] }              // fits these existing branches
  | { ok: true; fits: false; aboutSummary: string; whyNoneFit: string } // no-fit -> maybe a new thesis
  | { ok: false; reason: string };                                      // gate failed; NOT a fabricated fit
```

The anti-invention discipline is in the details of that type. When the model returns `fits: true` and names branches, every named branch is filtered against the set of branches that actually exist, and any invented one is dropped. If, after filtering, the model named no surviving branch, the whole result is downgraded to `fits: false`. A confident-sounding fit to a branch that isn't real doesn't become a fabricated attachment, it becomes an honest no-fit that asks me whether the belief is missing. And the gate never throws: a model that's down or an answer that won't parse produces `{ ok: false }`, which surfaces as "the mapper is unavailable, re-run it," never as a silent nothing and never as a guessed fit. The gate can fail. It cannot lie.

## Pass Two: Where, Exactly, and How

Only when pass one fits does pass two run, and this is where the reading becomes structured. Each individual claim in the document gets attached to a specific branch, with the same vocabulary the graph is built on: a relation of `supports`, `refutes`, or `weakens`, at a horizon, anchored to a span of the source. The model decides the interpretation, which claim bears on which branch, in which direction, over what time frame.

What it cannot decide is the structure, and that's enforced by code, not by asking nicely. This pass runs through what the Brain calls the cage, and the cage's rule is exactly the one from the [deterministic sandwich](/p/the-deterministic-sandwich/) and the [agentic worker](/p/the-agentic-worker/): the model chooses only *where inside its given anchor* a claim lands. It cannot invent a branch, it cannot merge or reorganize the taxonomy, and it cannot attach a claim to a branch it wasn't handed. A candidate that names a node outside its anchor is rejected by the cage before anything is written. The model authors the interpretation. The cage owns the structure. Instructing the model to behave is not a control, and the mapper doesn't rely on it as one.

When a document genuinely fits nothing, the no-fit path produces a small record of what the model read the document to be arguing, and hands it to me:

```typescript
interface NewThesisSignal {
  aboutSummary: string;   // what the model read the document to argue
  whyNoneFit: string;     // why it maps onto no existing branch
  // ...
}
```

That's the one door left open to human judgment, and it opens exactly where judgment belongs. I don't get pinged when the world confirms something I already believe. I get pinged when the world says something my worldview has no place for yet, which is precisely the moment I should be the one deciding whether to grow the graph.

## Seven Claims From One Article

The mapper was working and I still managed to get one thing badly wrong, and it's worth telling because the fix reshaped a chunk of the system. The problem was granularity of a different kind: not which branch a claim attached to, but how a claim got carved out of a document in the first place. My extractor was pulling out the load-bearing sentences of an article, and one week I looked at a weekend brief and found seven separate claims attributed to a single article, where the honest number was one, maybe two. It was highlighting sentences, not extracting facts.

Seven thin claims from one article doesn't sound like a disaster until you follow it downstream. A claim that's a lone sentence carries a "what" with no subject, no magnitude, no significance, and no reasoning, and the thing that eventually writes the brief has to string those disconnected fragments into prose. So it did what a model does when handed a gap: it filled it. That over-extraction is the direct cause of the worst thing my system has ever done in public, which was write a weekend brief containing a Munger quote the man never said, and a confident sentence claiming two numbers "came out of the same report" when they came from different ones entirely. The compose model didn't hallucinate out of nowhere. It fabricated the connective tissue my thin claims forced it to invent.

The fix was to change what a claim even is. A claim is no longer a load-bearing sentence, it's one complete fact told completely: a five-part unit that carries who and what, by how much, how it works and why it matters, when it was true, and when it gets tested, with verbatim spans anchoring every piece of it back to the source. One real fact, told in full, instead of seven fragments of one. It gives the model downstream a thread to follow instead of a hole to fill, and the fabrication problem it was papering over went away because the paper was gone.

And one of those five parts, the *when it gets tested*, quietly demanded infrastructure of its own. A claim that says "this reverses if the next inflation print comes in soft" is only worth anything if the system actually knows when the next print lands. So the humble test-date field on a claim is what forced me to build a forward calendar: a harvested, continuously updated view of the upcoming releases, central-bank dates, and events, so that every claim's test date resolves to a real thing on a real timeline instead of a vague "later." A structured claim needs a structured future to be tested against, and I didn't have one until a fake quote made me build it.

## What the Reading Can't Do

The mapper closes the loop I most wanted closed: the graph now reads the world into itself, autonomously on the common case, and asks for me only on a genuinely new belief. But I want to be exact about the seam it doesn't cover, because it's a big one. The mapper decides where a claim fits and how it relates. It does not decide whether the claim is *true*. A confidently written, completely false statement attaches just as cleanly as a true one, lands as `supports`, and strengthens a branch it had no business touching, and nothing in the fit-gate will catch it, because the fit-gate guards the structure of my beliefs, not the truth of the evidence. Keeping the world from lying to the graph is a different machine entirely, the one that verifies the evidence before it's trusted, and that machine is a later post. What this one guarantees is narrower and still worth everything: the model can read my worldview, and it cannot invent it.
