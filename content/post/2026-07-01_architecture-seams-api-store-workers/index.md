---
title: "Architecture → Seams → API → Store → Workers"
date: 2026-07-01
draft: false
description: "A practical construction method for building AI systems from durable architecture down to replaceable model workers."
tags:
  - ai
  - architecture
  - systems
  - small-language-models
  - agents
categories:
  - architecture
image: cover.png
---

There is a moment at the beginning of almost every AI project where the repo is empty, the architecture diagram is suspiciously clean, and somebody asks the question that quietly determines how the next six months are going to go: “What model should we use?” It sounds reasonable. The application needs intelligence, so you choose the intelligence first.

A model gets deployed, a prompt gets written, some tools get attached, memory gets bolted on, and within a few days the demo is doing something impressive enough that everyone feels like the architecture is taking shape. Except it is not architecture yet. It is a prototype wrapped around a model.

A few weeks later, the prototype needs persistent state. Then multiple workers need access to that state, one worker needs to call another, retries start duplicating work, somebody adds a status field, and suddenly half the system depends on an undocumented JSON structure that originally existed because it was convenient to put it in a prompt.

Then the model changes, and the prompts change with it. The output format shifts slightly, downstream logic breaks, and the team discovers that what looked like an implementation detail was actually carrying architectural responsibility. The model was not inside the system. The system had quietly formed around the model.

I have built enough of these systems to stop starting there. The construction order I use now is deliberately backwards from how most AI demos are built: **Architecture → Seams → API → Store → Workers.**

That sequence is not documentation order. It is implementation order, and each step exists to remove a class of ambiguity before the next one begins. By the time a model worker finally enters the picture, most of the important decisions have already been made, and the model has a job instead of being asked to invent the company.

## 1. Architecture: Decide Who Owns What

Architecture begins before Kubernetes, before the database schema, before the model server, and definitely before the prompt. The first question is not, “What components do we need?” The first question is, “What responsibilities exist?”

That difference sounds academic until a system becomes complicated. Components change constantly, while responsibilities are much more durable, and the most important architectural decision is usually deciding which part of the system has authority over which responsibility.

Consider PortfolioOS, or pOS (the portfolio management system I have been building around explicit responsibilities, bounded inference, persistent state, and deterministic control). One responsibility is understanding the current market environment. Another is discovering investment candidates, another is deciding how those candidates belong together inside a portfolio, and another is continuously watching existing positions for changes.

Those responsibilities became separate subsystems because they represent different kinds of authority. Brain (the subsystem that publishes the current market regime, risk posture, and market context) can describe the environment, but it cannot construct a portfolio. Hunt (the subsystem responsible for mandate-aware investment discovery, evidence collection, ranking, and candidate maintenance) can decide which opportunities deserve attention, but it cannot decide portfolio weights.

Portfolio Construction, or PC (the subsystem that assembles candidates into a portfolio while handling sizing, diversification, and portfolio-level constraints), can determine how positions fit together. It does not own the underlying investment thesis. Loop (the subsystem responsible for continuously monitoring existing positions and initiating actions such as trims when conditions change) can react to what is already owned, but it does not get to silently rewrite the mandate that created the portfolio.

Those boundaries are architecture, and none of them require me to decide which model is running inside each subsystem. Brain might eventually use several models, Hunt might use small models, deterministic services, search infrastructure, and human input, while PC might barely need inference at all.

The technology used to perform a responsibility is secondary to determining who owns the responsibility in the first place. This is also where I decide what must be deterministic and what is allowed to use inference.

If the system is calculating a portfolio weight, validating a schema, enforcing an authorization policy, checking whether a state transition is legal, or determining whether an operation already happened, I generally want deterministic software doing that work. If the system is interpreting a document, detecting nuance, comparing competing explanations, extracting meaning from unstructured evidence, or ranking uncertain possibilities, inference might be appropriate.

Architecture defines that border. It says where judgment belongs, where rules belong, where state belongs, and where authority belongs, and only after those decisions are reasonably stable do I move on.

---

## 2. Seams: Define Where Responsibility Stops

Once responsibilities exist, the next problem is figuring out how they touch each other. I call those boundaries **seams**, and a seam is the point where one part of the system stops knowing how another part works.

That last part matters more than it might initially appear. If Hunt needs market context from Brain, Hunt should not need to know how Brain produced it, which model Brain used, what prompts were involved, what data sources were consulted, or whether the result came from an inference worker, a deterministic calculation, or a human override.

Hunt should know only what Brain promises to provide. Conceptually, that seam might look something like this:

```text
MarketContext
    regime
    risk_posture
    effective_at
    confidence
    evidence_refs
```

That is not an Application Programming Interface, or API (a defined software contract that describes how one component interacts with another), yet. It is a statement about architectural responsibility. Brain owns `MarketContext`, consumers can use it, and consumers cannot reconstruct it behind Brain's back.

That distinction prevents one of the most common architectural failures I see in AI systems. Two components technically have separate names, but one reaches directly into the other's database, imports internal libraries, knows its prompt structure, or depends on undocumented output behavior.

Those are not separate systems. They are one tightly coupled system wearing two name tags, and the coupling only becomes visible when somebody tries to change one side independently.

A good seam removes knowledge. Portfolio Construction should not understand Hunt's internal scoring machinery, and it should receive candidates through a defined boundary instead. Loop should not need to understand how Portfolio Construction arrived at a position weight, and it should receive enough state to monitor the position and enough provenance to understand why the position exists.

The seam tells each subsystem what it may depend on, but just as importantly, it tells the subsystem what it must not depend on. That negative definition is incredibly useful because most architecture documents explain what components communicate, while far fewer explain what knowledge is forbidden from crossing the boundary.

Those forbidden dependencies are often where the real architecture lives. They are what keep internal implementation choices from quietly turning into system-wide dependencies.

---

## 3. API: Turn the Seam Into a Contract

Only after I understand the seam do I design the API. This ordering is intentional because APIs are concrete, and concrete things have a nasty tendency to become permanent.

If you begin with endpoints, you tend to expose whatever the implementation already happens to have. If you begin with the seam, the API has to represent an architectural promise instead of becoming a reflection of whichever component happened to get written first.

Suppose Hunt needs Brain's current market context. The seam has already established what Brain owns, so now I can define the API that exposes that responsibility.

```http
GET /market-context/current
```

The response might look something like this:

```json
{
  "regime": "late_cycle",
  "risk_posture": "elevated",
  "effective_at": "2026-08-26T14:00:00Z",
  "confidence": 0.81,
  "evidence_refs": [
    "evidence://macro/credit-spreads/2026-08-26",
    "evidence://macro/labor/2026-08-25"
  ]
}
```

The interesting part is not the endpoint. The interesting part is what is missing, because there is no prompt, no model name, no chain-of-thought field, no internal scoring weights, and no temporary intermediate objects.

The API exposes the responsibility, not the machinery. This becomes especially important when AI is involved because model outputs naturally tempt developers to expose too much.

A worker produces some large JSON object, so the easiest implementation is to pass that entire object downstream. Another worker starts depending on three fields inside it, a third worker discovers another useful field, and six months later the original model output has accidentally become the system's public interface.

Now you cannot change the model without changing the architecture, which is exactly backwards. I want the API contract to outlive the worker implementation, so Gemma can become Qwen, a large model can become a small model, or a model can disappear entirely and be replaced by deterministic code without forcing every consumer to change.

The consumer should not care as long as the contract remains true. That is why the seam comes first, and the API is simply the seam made executable.

---

## 4. Store: Make State Explicit

Then comes the store, and this is another place where my order differs from a lot of AI application development. Teams often start building workers first, then add persistence after they discover that the workers need memory, which frequently leads to a database containing whatever the workers happened to emit.

I want the opposite. The store should persist **system state**, not model exhaust, and before a worker exists I want to know what the system needs to remember.

For an investment candidate in Hunt, that might include its identity, mandate membership, evidence references, thesis state, ranking history, reevaluation dates, and current lifecycle status. For a portfolio position, it might include target weight, actual weight, entry thesis, risk state, provenance, monitoring conditions, and the history of changes made to it.

Those are durable system concepts. A model's internal explanation might be useful evidence, but it is not automatically a durable system concept simply because the model happened to produce it.

This distinction changes database design dramatically. Instead of building storage around generic agent history, I want domain state that reflects the concepts the application itself understands.

```text
candidate
candidate_evidence
candidate_rank_history
candidate_thesis
portfolio_position
position_monitoring_state
decision_record
```

Now the store represents what the system knows, what happened, and why it happened. The workers become producers and consumers of that state rather than owners of it, which is a much healthier relationship.

This also makes retries far easier to reason about. If a worker crashes after analyzing an earnings call, the system should know whether that analysis was committed, and if the job runs again it should be possible to determine whether the operation is new, incomplete, duplicated, or already finished.

That requires identities, lifecycle states, provenance, timestamps, and explicit transitions. Those are storage and application concerns, and they should not depend on a model remembering what it did.

The store is where the system acquires continuity. Without it, you do not really have a persistent intelligent system, you have repeated inference with increasingly elaborate memory tricks.

---

## 5. Workers: Add Inference Last

Only now do I build the workers, and by this point their lives are wonderfully constrained. A worker has an input contract, an output contract, a defined set of state it may read, a defined set of state it may write, and a clear understanding of which deterministic services are available to it.

It also knows what authority it possesses and, more importantly, what authority it does not possess. That is a much better environment for inference because the model is being asked to solve a bounded problem rather than navigate the entire application.

Imagine Hunt needs a worker that evaluates whether a newly published earnings transcript materially changes an existing investment thesis. The worker does not receive unlimited access to PortfolioOS, and it does not get an open-ended instruction to “figure out what to do.”

Instead, it receives the thesis, the transcript, relevant evidence, and a bounded task. Conceptually, the task might be:

```text
Determine whether this evidence:
    supports the thesis
    weakens the thesis
    contradicts the thesis
    adds no material information
```

The worker returns a bounded result, and another part of the system decides what that result means operationally. The worker does not directly edit the portfolio, change the market regime, sell the security, or decide that some other subsystem's policy is inconvenient and route around it.

It performs inference inside a box. That constraint is what makes the worker reliable enough to use as part of a larger system rather than treating the model itself as the system.

This is also where small models become incredibly useful. Because the task is narrow, I can select the model based on the actual capability required, so one worker may need strong nuance detection, another may need excellent structured extraction, another may need vision, and another may need very little intelligence at all.

The architecture does not care which model wins those evaluations. Workers are replaceable implementations of bounded capabilities, which turns model selection into an optimization problem rather than an architectural commitment.

Instead of asking, “Which model can run my application?” I can ask, “What is the smallest model that can reliably perform this job?” That question leads to cheaper systems, faster systems, easier testing, clearer failure modes, and much more freedom to change models later.

It also keeps us from making everything an agent. Some workers are inference workers, some are deterministic services, some are schedulers, some are validators, and some are simple state machines.

The architecture decides what the job requires. The excitement of the technology does not get to make that decision for us.

---

## 6. Why the Order Matters

The sequence works because every layer constrains the next one. **Architecture** defines responsibility, **seams** define dependency, **APIs** define contracts, **stores** define durable state, and **workers** perform bounded work inside those constraints.

Reverse the order, and each layer starts leaking upward. Start with workers, and worker behavior influences the data model. Start with the data model, and database convenience influences the API. Start with the API, and endpoint convenience influences subsystem boundaries.

Eventually the architecture becomes a description of whatever happened to get implemented. That is how prototypes become permanent, because every temporary implementation choice slowly acquires consumers, dependencies, and expectations around it.

The sequence also gives you natural checkpoints for testing the design before the system becomes expensive to change. If I cannot describe the architecture without talking about specific models, the responsibilities probably are not clear enough yet.

If I cannot explain a seam without describing the other subsystem's internals, the boundary is probably wrong. If the API contains fields that only make sense because of the current model, I am probably leaking implementation details.

If the store contains mostly transcripts of inference rather than durable domain state, the system probably does not understand its own state. If a worker requires broad authority across the system, the task probably has not been bounded tightly enough.

Each layer acts as a test of the layer before it. That is why I think of this as a construction method rather than simply an architecture pattern.

---

## 7. What This Looks Like in a Real System

When I started rebuilding PortfolioOS, I deliberately stopped thinking about it as a collection of agents. I started with responsibilities because I wanted the architecture to survive changes in models, tools, implementation languages, and deployment patterns.

Brain owns market context, Hunt owns discovery and candidate intelligence, Portfolio Construction owns portfolio assembly, and Loop owns continuous monitoring and position-level reactions. The Home Office (the subsystem that translates household goals, accounts, tax constraints, timelines, and funding requirements into investment mandates) owns the household requirements that the investment system ultimately needs to satisfy.

Those became architectural boundaries, and then I defined the seams between them. The Home Office can give Portfolio Construction a mandate, but it should not tell Portfolio Construction how to choose individual securities.

Brain can publish risk posture, but it should not reach into Hunt and alter candidate rankings directly. Hunt can publish candidate evidence and rankings, but it should not modify an existing portfolio because it discovered something interesting.

Loop can identify that a held position needs attention, but it should not quietly redefine the household's objectives. Each subsystem owns its part of the problem and communicates across explicit boundaries rather than reaching into another subsystem's internal implementation.

Once those boundaries existed, the APIs became much easier to reason about. Once the APIs existed, I could design state around the actual domain objects crossing those boundaries rather than around whatever one model happened to emit.

Only after that did individual model workers become interesting. At that point I could discover that Qwen handles one kind of nuance better than Gemma, or that Gemma performs better for another bounded task, without changing who owns the responsibility.

That is the payoff. Model selection becomes an implementation decision again instead of quietly becoming an architectural decision.

---

## 8. The Construction Rule

When I begin a new intelligent subsystem now, I work through the same sequence every time. First, I draw the architecture and define ownership, then I define the seams and deliberately remove knowledge between components.

After that, I turn those seams into APIs with explicit contracts, and I build the store around durable domain state, provenance, lifecycle, and history. Only then do I add the workers that actually perform inference.

Sometimes implementation proves that the architecture was wrong, and that is completely fine. The point is not that architecture must be perfect before code exists, but that architectural decisions should be intentional, visible, and revisited consciously rather than emerging accidentally from prompts, database tables, or model output formats.

The order gives you somewhere to stand because it keeps the durable parts of the system above the volatile parts. That matters even more in AI because the lowest layer is changing unbelievably quickly, and models get cheaper, smaller, faster, more capable, and occasionally worse at exactly the thing the previous version did well.

I want to be able to take advantage of that churn without rebuilding the rest of the application every time the model landscape changes. I cannot do that if the application has already formed around a particular model's prompts, output formats, assumptions, and quirks.

So the construction method stays deliberately boring: **Architecture → Seams → API → Store → Workers.** Decide what the system is, decide where the boundaries are, decide what crosses them, decide what must persist, and only then decide how intelligence helps.

The model comes last because the model is the thing I expect to replace. Everything above it should be designed to survive.
