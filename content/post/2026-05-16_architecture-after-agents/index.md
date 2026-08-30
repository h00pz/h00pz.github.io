---
title: "Architecture After Agents: Why AI Apps Are Becoming Distributed Systems"
slug: architecture-after-agents
date: 2026-05-16
draft: false
description: "Once models become bounded workers, AI applications start to look like familiar distributed systems, and AI engineering looks like software engineering again."
tags:
  - distributed-systems
  - architecture
  - systems
  - agents
categories:
  - Small Model Systems
image: cover.png
---

This series has spent a lot of words taking things away from the model. Stop making it the application. Put it behind a seam. Keep state out of it. Bound its context. Give it artifacts instead of conversations. Each of those posts shrinks the model's job a little more, until the model is doing one thing: bounded inference at a specific boundary, with everything around it owned by the system.

So it is worth stopping to ask what is actually left once you have done all of that. If the model is no longer the router, the memory, the state machine, the policy engine, the orchestrator, and the integration layer, then what is holding the application together? What is the architecture, when the agent is no longer the architecture?

The answer, the more of these systems I build, is a little anticlimactic and also very reassuring. What is left is a distributed system. Services, stores, queues, contracts, workers, schedulers, failure domains, and observability, with inference living in a handful of clearly marked boxes. The exciting part turns out to be surrounded by an enormous amount of deeply ordinary software, and that is exactly the point.

## The Shape That Keeps Emerging

When I look at pOS now, the diagram doesn't look like an AI application. It looks like any competently built distributed backend. There are subsystems that own responsibilities, the Brain, Hunt, Portfolio Construction, Loop, the Home Office. There are stores that own durable state. There are workers that do units of work on a schedule or in response to a queue. There are explicit contracts between all of them, and there are ports that keep each subsystem from reaching into the others.

The models are in there, but you have to look for them. They sit inside particular workers, at particular boundaries, doing the specific jobs that genuinely need inference: judging whether evidence changes a thesis, extracting structure from a messy document, detecting a nuance a rule would miss. Everything between those boxes, how work gets scheduled, how records get claimed, how failures get retried, how state gets written, is software doing what software has always done.

This isn't a disappointment. It's the sign that the architecture is working. The probabilistic part has been contained to where it earns its place, and the rest of the system gets to be as boring and reliable as the rest of the system has always been able to be.

## Work Queues Are Back, Because They Never Left

The clearest example is how work moves through the system. Once a model is a bounded worker rather than an autonomous agent, you need a way to give it work, know whether it finished, and recover if it didn't. That isn't a new problem. It's the oldest problem in backend engineering, and the old answers apply directly.

pOS uses a claim substrate for exactly this. Records get emitted onto a queue, workers claim them, process them, and mark them done, and an empty claim simply returns nothing so the worker sleeps and tries again. Leases, attempts, dead-letter states, all the familiar machinery is there, because the moment your inference lives inside a worker, the worker has all the ordinary needs any worker has ever had. Not every part of the system even needs the full queue. One evidence worker deliberately uses a simple poll-sweep instead, reading a pending list on an interval and processing what it finds, because the work arrives continuously and a lighter pattern fits better. That, too, is an old and well-understood choice. Poll or queue is a question distributed systems have been answering for decades, and it is answered here the same way, on the merits of the workload.

## The Dual-Write Problem Does Not Care That You Are Doing AI

This isn't only my read of it. The academic version of the same claim is Berkeley's <a href="https://aihub.org/2024/03/15/the-shift-from-models-to-compound-ai-systems/" target="_blank" rel="noopener">shift from models to compound AI systems</a>, which argues that state-of-the-art results increasingly come from systems of components rather than monolithic models, and that scaling often returns less per dollar than building the system around the model does.

If you want proof that AI applications are just distributed systems wearing a new hat, watch the classic distributed-systems bugs reappear, unchanged.

In pOS there's a spot where registering a demand means writing to two places: a store that records the demand, and a queue that dispatches it. Write the record, then emit to the queue. If the emit fails after the write succeeds, you get a torn state, a demand that is registered but not dispatched. This is the dual-write problem, named and solved in the distributed-systems literature long before any of this was about AI; the standard answer is the <a href="https://microservices.io/patterns/data/transactional-outbox.html" target="_blank" rel="noopener">transactional outbox</a>. It is exactly as old and exactly as unavoidable as it has ever been. No amount of model capability makes it go away, because it has nothing to do with the model.

What matters is that the system handles it the way distributed systems have learned to. The two writes are ordered deliberately so that the only possible torn state is the recoverable one: a record can exist without a queue entry, but a queue entry can never exist without a record. The half-failed operation returns an honest error, and a retry is idempotent, so replaying it collapses onto the existing record instead of duplicating it. That isn't AI engineering. That's the same discipline you would apply to an order-processing pipeline, and it applies here for the same reasons.

## Idempotency Is Not Optional When Your Workers Retry

Because there are workers and queues and retries, idempotency stops being a nicety and becomes structural. pOS fingerprints operations so that repeating them is safe. A trade is identified by a fingerprint of account, ticker, date, kind, and quantity, and re-submitting the same trade with a corrected note is a no-op rather than a duplicate. Artifacts are projected deterministically, so the same underlying belief always serializes to identical bytes and merges on retry. Position writes fold the candidate change against the existing history first and only persist if it is valid, so a rejected operation leaves the ledger untouched.

Every one of those is a technique software engineering already had. What is new is only the reason they're suddenly non-negotiable: a system with probabilistic components and autonomous-ish workers is going to re-run things, and re-running things has to be safe. The presence of inference raises the stakes on idempotency; it doesn't change what idempotency is.

## Failure Domains and Observability Come Along For the Ride

A distributed system has failure domains, and so does this. A hand-off to the Committee can fail without failing the research that produced the finding. A worker can die and its record can be released back for another worker to claim. A scheduled job can fail to fire, and you need to notice. These are containment boundaries, drawn so that a failure in one place doesn't become a failure everywhere, and drawing them is ordinary systems work.

Observability comes along too, with one genuine addition. In a normal system, knowing what happened is enough. In a system with inference, you also need to know why the model decided what it decided, which means the artifacts crossing your seams have to carry provenance, timestamps, versions, and evidence references. That's more than a traditional system usually bothers with, but it is an extension of observability, not a replacement for it. You still need the logs, the metrics, the traces, and the record of what each component did. You just also keep the receipts for the inference.

## This Shape Is Designed, Not Discovered

Everything so far can sound emergent, as if you assemble enough workers and stores and the distributed system precipitates out on its own. It doesn't. Left alone, a pile of model calls doesn't converge on clean failure domains and idempotent seams; it converges on the tangle this series started by complaining about. The distributed-systems shape is something you get on purpose, by specifying the architecture before you build it.

The discipline I use for that is a framework of its own, and it is a subject for another day. But two of its ideas are load-bearing for the point here, because they're what keep the distributed system from quietly rotting back into an agent.

The first is that the architecture describes the desired end state, never the present. A document that records how things work today silently entrenches whatever happens to exist, hacks included, because the moment the doc says "this is how it works," every accident acquires the authority of a decision. So the end state and the as-built now are kept apart. The architecture is normative, the ownership and seams and contracts as they're meant to be, while a separate register tracks what is actually built, what is merged but dark behind flags, and the distance between the two. The design never bends to accommodate the mess. The system knows what it is supposed to be even while it is still becoming it, and the gap is made explicit instead of absorbed.

The second is that each subsystem's most important boundary gets named before any code exists. For Hunt, the discovery subsystem, the governing decision is simply where Hunt stops: it finds and researches candidates and doesn't evaluate them into the portfolio, because evaluation is another subsystem's job. Drawing that line too generously is precisely how Hunt drifts back into doing everyone else's work, so the line is named, owned, and defended up front. Most of the failure modes this series has worried about are, underneath, a boundary drawn too generously. Naming the boundary before building is how you keep from drawing it by accident.

## Done Is Something the System Checks

Specifying the architecture first has a payoff that lands squarely in distributed-systems territory: "done" stops being a feeling and becomes something the running system verifies about itself.

pOS has a test whose only job is to reconcile the architecture with the code. It fails if any endpoint is mounted that nobody declared, and it fails if any endpoint that was specified and built is wired to nothing. It even proves it can catch both, by injecting each failure and confirming the guard fires, so a green result actually means something. Deliberately breaking a thing to prove the alarm for it works is <a href="https://principlesofchaos.org/" target="_blank" rel="noopener">chaos engineering</a> shrunk down to a single test. And it separates a plan from a bug the way the end-state rule implies: an endpoint specified but not yet built is a plan and allowed, while an endpoint built but mounted nowhere is an inconsistency and not. The list of known gaps may only shrink.

In an ordinary distributed system you would call that contract testing or drift detection, and that is exactly what it is, aimed at the seam between the specification and the deployment, which is the precise place an AI system rots if nobody is watching. It's the same discipline that produced idempotent workers and honest torn states, applied one level up: not just did the operation succeed, but does the system still match what it was designed to be.

## Why This Is Good News

It would be easy to read all of this as deflationary, as if the exciting AI application turned out to be a boring backend with a few model calls in it. I read it the opposite way. The fact that AI applications are converging on distributed-systems architecture is the best news the field has had, because it means we aren't starting from scratch.

We have spent forty years learning how to build systems out of unreliable parts. We know how to draw service boundaries, define contracts, run work queues, make operations idempotent, contain failures, and observe what happened. All of that knowledge transfers directly the moment you stop treating the model as a magic box that dissolves the need for architecture and start treating it as one more component, a fast-moving, probabilistic, occasionally-wrong dependency that needs the same discipline as every other dependency we have ever integrated.

The teams that will build reliable AI systems aren't the ones with the cleverest prompts. They are the ones who remember how to build software, and who recognize that a language model, for all its novelty, is a component inside an application, not a replacement for the craft of building one.

## Architecture After Agents

The agent era was a useful phase. Handing a model some tools and telling it to figure things out was the fastest way we have ever had to discover what these systems can do. But the prototype was never the architecture, and as these applications grow up, they're shedding the agent framing and revealing the distributed system that was always underneath.

That's the arc this whole series has been tracing. Stop building agents and start building systems. Keep the model out of the architecture. Make the seam the product. Bound the context, own the state, exchange artifacts. Follow each of those far enough and you arrive somewhere familiar: an application made of services and stores and queues and contracts, with intelligence applied deliberately at a few well-chosen points.

AI engineering, done well, is starting to look a lot like software engineering again. After everything, that turns out to be the destination, not the consolation prize. The model was the new thing. The system was always going to be the hard thing, and we already know how to build systems.
