---
title: "The Deterministic Sandwich"
slug: the-deterministic-sandwich
date: 2026-07-28
draft: false
description: "How I turn a would-be agent into a Kubernetes worker: a bounded model call as the filling, deterministic input and output as the bread, the prompt as config."
tags:
  - agentic
  - workers
  - deterministic
  - prompts
  - structured-outputs
categories:
  - AI Systems Engineering
image: the-deterministic-sandwich.png
---

There is a thing in PortfolioOS I call an agent, out loud, in conversation, because it's convenient. Her name is Samantha, which is the name I use across pOS for the operator-facing voice, picked on purpose after the Sex and the City character who never once softened a verdict to make anyone feel better, because bedside manner is the last thing I want from the thing reviewing my money. Her job is to design a sleeve, the pack structure and target weights that a slice of the portfolio should aim for. She reads the mandate, reads the market and economy regimes, argues two investing philosophies against each other, and proposes a design. It looks, from the outside, exactly like an agent.

She is not an agent. She's a Kubernetes worker with a language model bolted into the middle of her, bounded on both sides by code that does not trust her. The [previous post](/p/is-this-even-an-agent/) was about how I classify work into bounded workers and genuine agents, and it left a question hanging: once you've decided a thing should be a bounded worker, how do you actually build it around a model that would very much like to be an agent? The answer is a shape I've been drawing for months and only recently got precise about. I call it the deterministic sandwich, and this post is the real one, with the actual code and the actual config.

## The Shape

The [deterministic sandwich](/p/your-ai-agent-probably-shouldnt-be-an-agent/) is three layers. The bottom slice is deterministic code that assembles the model's input. The filling is exactly one bounded model call. The top slice is deterministic code that validates the output before anything downstream is allowed to believe it. The model does the one thing it's genuinely good at, which is fuzzy reasoning over messy input, and it does it strictly between two slices of code that decide what goes in and refuse to trust what comes out.

The defining property, the thing that makes this a worker and not an agent, is that the control flow is fixed. The model does not choose the next step. The sequence is decided before the run starts: assemble, call, validate. The model reasons inside the filling, and that's the only place it gets to. Everything around it is ordinary, deterministic, testable software, and that's not a limitation I'm apologizing for. That's the point.

## The Bottom Slice Is Config, Not Code

Here's the part people skip. The model's input is not just data assembled at runtime, it's also the prompt, and the prompt is the most important piece of deterministic infrastructure in the whole sandwich. So I refuse to bake it into the code.

Samantha's entire design doctrine lives in a Kubernetes ConfigMap, mounted into the pod at runtime, and the [whole thing is reproduced here](https://github.com/h00pz/h00pz.github.io/blob/main/examples/pc-agent-prompt-config.yaml). The prompt is data, versioned in git, and editable without a rebuild:

```yaml
# change the doctrine, `oc apply -f` this file, then
# `oc rollout restart deploy/pos-api`. No rebuild.
apiVersion: v1
kind: ConfigMap
metadata:
  name: pc-agent-prompt
  namespace: pos
data:
  sleeve-agent-prompt.txt: |
    You are Samantha, the research director of Portfolio Construction...
    You design the sleeve's INDEX — the pack structure and target
    weights — and NEVER its individual positions.
```

Treating the prompt as config rather than code isn't a convenience. It's the same instinct as keeping [state out of the model](/p/persistent-state-beats-agent-memory/), applied to the model's instructions: the behavior that governs a probabilistic component has to live somewhere I can see it, diff it, and change it without shipping a binary. The inline constant it replaced is now only a dev fallback, used when the ConfigMap isn't mounted.

And look at what the doctrine actually encodes, because it's most of the sandwich's bottom slice written in English. It tells her to read both the market regime and the economy regime, and then this:

> If EITHER regime read is stale or absent, REFUSE TO DESIGN. Say so plainly to the operator and defer. An honest refusal beats a design built on a number you do not have.

That's a guardrail against fabrication, written into the input rather than bolted on after. She's told to be holdings-blind, to design pack shapes and never name a ticker, so an entire category of dangerous output is ruled out before she generates a token. And the honesty rule that matters most is right there in the prompt: *cite only figures a tool actually returned.* Hold onto that one, because the top slice is going to enforce it in code.

## The Filling Is One Bounded Call

The model call itself is unremarkable, which is exactly right. She's given a fixed set of tools to read what she needs, she reasons, and the only way a design leaves her is a single tool call carrying the complete pack set. She doesn't get to loop until she's satisfied, she doesn't get to decide she needs a new capability, and she doesn't get to persist anything herself. The control flow that surrounds the call is fixed: read posture, design, propose. The interesting, fuzzy, genuinely-hard reasoning happens in that one call, and nowhere else in the worker does the model get a vote.

## The Top Slice Does Not Trust Her

Then the output hits deterministic code, and the deterministic code assumes the model got it wrong until proven otherwise. Here's the actual parser that turns her proposed design into something the system will accept:

```typescript
export function parseProposedPacks(raw: unknown): readonly ProposedPack[] | null {
  const arr = (raw as { packs?: unknown })?.packs;
  if (!Array.isArray(arr)) return null;
  const out: ProposedPack[] = [];
  for (const p of arr) {
    if (typeof p !== 'object' || p === null) continue;
    const name = (p as { pack?: unknown }).pack;
    const pct = (p as { pct?: unknown }).pct;
    if (typeof name !== 'string' || name.trim() === '') continue;          // drop the nameless
    if (typeof pct !== 'number' || !Number.isFinite(pct) || pct < 0 || pct > 100) continue; // drop the impossible
    out.push({ pack: name.trim(), pct, rationale: /* ... */ '' });
  }
  return out.length > 0 ? out : null;   // all-empty is an honest null, not a fake design
}
```

Every branch in there is a small act of distrust. A pack with no name is dropped. A weight that isn't a finite number between zero and a hundred is dropped, silently and honestly, rather than coerced into something plausible. And if nothing survives, the function returns `null`, which the caller reads as an honest gap. It does not return an empty design dressed up as a real one. The model can produce garbage, and the worst that garbage can do is become a recorded absence, never a fabricated recommendation.

This is the same instinct Jason Liu compressed into a talk he titled <a href="https://jxnl.co/writing/2023/11/02/ai-engineer-keynote-pydantic-is-all-you-need/" target="_blank" rel="noopener">Pydantic is all you need</a>: make the model emit a typed object and let ordinary code inspect, validate, and retry it, instead of trusting prose. The parser above is that idea with the trust dialed to zero, which is what you want when the typed object it's checking decides where money goes.

That honest-gap discipline runs through every worker in the system, not just this one. The position-review worker records exactly why it produced nothing, from a small fixed vocabulary:

```typescript
// action is null; this is WHY, from a closed set — never a guessed action.
gapReason: 'model_unconfigured' | 'model_failed' | 'parse_failed'
```

A model that isn't wired up, a model call that failed, an answer the parser couldn't read: each becomes a typed, recorded gap. None of them becomes an invented trade. The sandwich's top slice turns every failure of the filling into a visible nothing.

And remember the honesty rule from the prompt, *cite only figures a tool actually returned?* The research worker enforces it in code, not on trust. It wraps every tool the model uses so it can capture what each one actually returned, and after the run it checks that every figure the model cited appears in that captured substrate. A single cited number that no tool produced rejects the entire turn:

```typescript
const cited = extractCitedFigures(answer);
if (cited === null) return { ...gap, modelGap: true, gapReason: 'unparseable answer' };
if (!validate(cited, substrate).ok) return { ...gap, fabricationRejected: true };
```

The prompt asks the model not to make up a number. The top slice assumes it might anyway, and catches it when it does. That's the difference between an instruction and a guarantee, and it's the whole reason the model gets to live inside a system that touches money.

## That's How You Turn an Agent Into a Worker

Step back and look at what Samantha actually is. A claim comes off a queue. Deterministic code assembles her input, including a prompt mounted from a ConfigMap. She makes one bounded model call. Deterministic code validates the result, dropping anything malformed, rejecting anything fabricated, and recording an honest gap when there's nothing trustworthy to keep. Then the worker completes, or releases the claim, and goes back to the queue. That's a Kubernetes worker's [reconciliation loop](/p/is-this-even-an-agent/) from end to end, and the model is one bounded step inside it, wrapped in bread.

The word "agent" was doing a lot of quiet work in my head for a long time. It made me think the model was the system, that its reasoning was the thing I was building around, that my job was to give it more room. The deterministic sandwich is the opposite instinct. The model is a component with a bounded job, the input it gets and the output it's allowed to emit are both decided by code I can read, and the fact that the thing in the middle is probabilistic changes almost nothing about the shape of the worker around it. I turned an agent into a worker by refusing to let the agent be the architecture.

## What the Bread Can't Do

I want to be precise about the limit, because it's easy to oversell this. The deterministic sandwich makes the model safe to be *wrong*. It cannot make the model *right*. The bottom slice can rule out whole categories of bad output, and the top slice can catch a malformed design, an out-of-range weight, a fabricated figure, or a missing regime read. What neither slice can catch is a design that is well-formed, correctly cited, internally consistent, and simply a bad idea. A pack set where every number is real and grounded and the overall shape is still wrong sails straight through, because nothing about it is detectably broken.

That's not a flaw in the sandwich. It's the sandwich telling you the truth about where its job ends. It bounds the blast radius of a model that fabricates or malforms, which is a large and real class of failures, and it does nothing about the model that reasons poorly in a way that looks fine. That last gap is exactly why the prompt ends where it does, with the rule the code can't enforce and won't pretend to: *you propose a design; the operator decides.* The sandwich makes the model a safe worker. It was never going to make it a safe decision-maker, and the honest architecture is the one that knows the difference and leaves the last call to a human.
