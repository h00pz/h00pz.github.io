---
title: "Separating Market Intelligence From Portfolio Decisions"
slug: market-intel-vs-portfolio-decisions
date: 2026-08-25
draft: false
description: "The thing that reads the world and the thing that moves my money are two different subsystems. Why the seam between them is structural, not a rule I remember."
tags:
  - seams
  - architecture
  - systems
  - state
  - agents
categories:
  - AI Systems Engineering
image: market-intel-vs-portfolio-decisions.png
---

When I read the news as a person, one act does two jobs at once. I take in what happened, and somewhere in the same breath I've decided what it means for what I own. Fed minutes land, and before I've finished the paragraph I'm already thinking "trim the long-duration sleeve." That fusion feels like intelligence. It's how every good analyst I've ever met works, and it's exactly the wrong shape to build software around, because when the reading and the deciding are the same act, you can never inspect either one. You can't ask the system "what do you believe about the world, independent of what you happen to hold," because it never believed anything independent of what it holds. It baselined its worldview against its own book.

I know that failure by heart because [PortfolioOS v2](/p/is-this-even-an-agent/) was built on it, and this post is about the line v3 draws that v2 never did. Reading the world is one subsystem. Deciding the portfolio is another. The seam between them is the most load-bearing boundary in the whole system, and the entire trick is that I refused to let it be a rule I remember and made it a fact about where the code lives instead.

## The Two Things Are Not One Thing

Say it plainly. Market intelligence answers "what is true about the world." Portfolio decisions answer "what should I do about what I hold." Those sound adjacent, and they are, which is precisely why they collapse into each other if you let them. The [Brain](/p/the-living-thesis-graph/) reads filings and prices and macro data and writes down beliefs. The portfolio loop reads those beliefs, joins them against the actual book, and proposes actions. Both are necessary. Fused, they produce a system that's locally sensible at every step and globally impossible to reason about, which is the same failure I've been naming all series: [each part correct, the whole wrong](/p/the-thesis-that-can-be-wrong/) in the relations between the parts.

The concrete version of that failure has a name in the codebase. In v2 the function that decided whether a capital action was allowed imported the macro-market rules and blocked a trade on a read of the economic cycle:

```typescript
import { isActionRestrictedByCycle, getCycleBehavior } from '../rules/cycle.rules'
// ...
const cycleRestricted = isActionRestrictedByCycle(action.type, portfolio.cycleState, sleeve.type)
if (cycleRestricted) {
  // block a capital action because of a macro-market read
}
```

Look at what that one gate is doing. A judgment about the world, the cycle read, is wired directly into the gate that permits or denies moving money. The market intelligence isn't informing the decision. It *is* the decision, fused into the same function, and once it's there you can't change what you believe about the cycle without touching the code that trades, and you can't audit a trade without re-deriving a macro thesis. v2's worse cousin of this was in the research side, where "baseline every ticker" quietly became "evaluate every ticker," and the gathering of facts and the judging of them collapsed into a single pass. Same disease, twice: judgment showing up where it doesn't belong.

## The Fix Is Structural, Not a Rule

The obvious fix is a rule. "Intel workers must not look at holdings." I've written rules like that and I've watched them rot, because a rule is a thing a future version of me has to remember at three in the morning, and the whole [thesis of this series](/p/persistent-state-beats-agent-memory/) is that the architecture should make the wrong thing hard to express, not merely forbidden. So the position-blindness of the Brain isn't a rule. It's a missing field.

The container the Brain publishes, the thing that holds a belief, has no place to put a position:

```typescript
// POSITION-BLINDNESS (seam-brain): the container carries NO position field. The
// Brain never knows what is held; the Portfolio Loop reads this container and joins
// branch -> position on its own side. Enforced structurally -- ThesisContainer
// has no position-shaped field -- and asserted in the test suite.
```

A belief node is a statement and its [falsifier](/p/the-thesis-that-can-be-wrong/) and its evidence. There's no ticker on it, no weight, no lot, no cost basis, because the type doesn't have anywhere for those to go. An intel worker literally cannot leak a holding into a thesis, not because it's forbidden to, but because the destination doesn't exist. That's the difference between a rule and a shape. A rule says don't. A shape says can't.

And the join, the actual matching of "this belief" to "this position I hold," lives on the far side of the seam, in the portfolio loop, by deliberate design:

```typescript
// FML-706 -- the join happens on THIS side of the seam.
// THE DIRECTION IS THE ITEM. The Brain publishes branches and learns nothing;
// the loop reads them and does the join here, caching the match on its own
// record. The Brain's position-blindness is therefore a fact about where this
// function lives, not a rule someone has to remember.
```

"The Brain publishes branches and learns nothing." That's the whole seam in one sentence. Information flows one direction across it. The Brain emits beliefs about the world and never hears back what was done with them, so it can't start shading its worldview toward the book, because it doesn't have the book. This is [command-query separation](https://martinfowler.com/bliki/CQRS.html) drawn through the middle of a money system: the side that reads the world and the side that changes the portfolio are different models with a one-way channel between them, and neither can reach into the other's job.

## The Gateway Makes It Physics

The seam gets one more layer under it, and this is the one I'm proudest of, because it stops being a property of my types and becomes a property of the runtime. Every connector, the things that reach the outside world, has a *kind*, and the kind decides which capability planes can ever engage:

```typescript
export function planesForKind(kind: ConnectorKind): ReadonlyArray<Plane> {
  switch (kind) {
    case 'source':    return ['protocol', 'business'];              // news, filings
    case 'model':     return ['protocol', 'business'];
    case 'financial': return ['protocol', 'business', 'capital'];   // IBKR orders
    default: {
      const _exhaustive: never = kind;   // add a kind without updating this -> fail closed
      void _exhaustive;
      return ['protocol'];
    }
  }
}
```

A `source` connector, the kind that pulls news and filings, the raw material of market intelligence, never gets the `capital` plane. It cannot move money. Not "is not supposed to." *Cannot*, because the plane that authorizes moving money doesn't engage for its kind, and the check that gates capital returns a hard refusal for anything that isn't a `financial` connector. So the news reader and the order placer aren't just different subsystems in my head. They're different callers with different authority at the gateway, and the one that reads the world has no path to the one that spends. The `never` in that default is the good kind of paranoia: add a new connector kind and forget to classify it, and it fails closed to protocol-only rather than silently inheriting the power to trade.

The intel side even says it out loud in the one place a model gets to reason, the [worker's prompt](/p/the-deterministic-sandwich/): "you rank the world's facts, you never see or reason about the book." The instruction is there for the model's benefit, but I don't trust it to the instruction. I trust it to the missing field and the denied plane. The prompt is a courtesy. The architecture is the guarantee.

## Where the Ticker Finally Shows Up

Cross the seam and everything the Brain refused to hold suddenly appears, because now it's allowed to. The decision side traffics in objects that are all about specific positions:

```typescript
export interface DecisionCandidate {
  readonly ticker: string;         // the Brain never had this
  readonly sleeveId: string;
  readonly kind: DecisionKind;     // 'enter'|'harvest'|'trim'|'protect'|'exit'|'add'|'hold'
  readonly horizon: Horizon;
  readonly rationale: string;
  readonly status: DecisionStatus; // 'open'|'acted'|'dismissed'|'superseded'
  // ...
}
```

This is where a belief becomes a candidate action against a named holding, and it's the right place for it, because this side is allowed to know the book. The mandate shows up here too, and it's deliberately soft: constraints are surfaced to the decision loop as information to reason over, warned rather than blocked, because the hard, catastrophic limits live in a separate capital-law surface and the mandate's job is judgment, not enforcement. The world-reading is done. This is the deciding, and it happens in its own subsystem, with its own types, holding the one thing the intel side was never allowed to touch.

## What the Seam Doesn't Buy Me

Here's the honest edge, because it's easy to mistake a clean boundary for a correct outcome. The seam guarantees that my worldview isn't contaminated by my book and my trades aren't secretly re-deriving a macro thesis inside a permission check. It guarantees I can read what I believe about the world without any position leaking in, and audit any decision without reverse-engineering a worldview. Those are real and they're exactly what v2 couldn't give me.

What it does not guarantee is that the join is right. When the portfolio loop takes a true belief about the world and matches it to a position and proposes a trim, every part of that can be clean, the belief well-formed and falsifiable, the position correctly identified, the mandate honestly applied, and the resulting decision can still be a bad one. The seam moves the judgment to one clearly marked place. It cannot make the judgment good. That last call, "this true thing about the world means this specific thing for this specific holding," is exactly the join FML-706 puts on the portfolio side, and it's the one part of this whole system I can't make structural, because it isn't a shape. It's a decision, and it stays [mine to get wrong](/p/the-weekend-brief/). The architecture's job was never to make that call for me. It was to make sure that when I make it, I'm making it in the open, on one side of a line I can see.
