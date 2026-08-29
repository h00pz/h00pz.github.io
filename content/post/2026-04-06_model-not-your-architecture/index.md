---
title: "The Model Is Not Your Architecture"
date: 2026-04-06
draft: false
description: "Models are replaceable components. The architecture around them is the durable part of an AI application."
tags:
  - ai
  - architecture
  - small-language-models
  - software-architecture
categories:
  - Small Model Systems
image: cover.png
---

A few months ago I was working through an AI application architecture with someone when the conversation took a familiar turn. We had spent most of the time talking about the actual system: how requests entered the application, which components owned state, where deterministic code should replace inference, how workers communicated, how failures were contained, and what happened when one part of the system was unavailable.

Then someone asked the question that seems to eventually dominate every AI architecture discussion: **“What model are we using?”** The entire conversation immediately collapsed into model selection. Should it be Llama? Qwen? Gemma? Claude? GPT? How many parameters? What context window? What benchmark scores? Should we use a reasoning model? What about mixture-of-experts? Could we squeeze something larger onto the GPUs?

These are useful questions, but they aren't architecture questions. The model is one component inside the architecture, and if replacing the model requires redesigning the application, then the model was never really a component. It was the architecture, and that is usually a mistake.

I got to test this claim for real. When [the Gold Trap](/p/the-gold-trap-small-models-are-not-interchangeable/) forced pOS to move its document work from one small model to another, the swap was a configuration change rather than a redesign, precisely because the boundary around that model was explicit and the rest of the system didn't know or care which model sat behind it. That's the actual test of whether a model is a component or the architecture: when you replace it, does anything else have to move?

There's a serious objection to all of this that I don't want to dodge: that the durable architecture I'm describing is itself just scaffolding for today's models, and the next model will absorb it the way bigger context windows absorbed a lot of retrieval code. I think that's half right, and the half it gets wrong is the whole point, so I take it on directly in a later post.

## The Model Trap

AI development has an unusual tendency to start from the most volatile part of the technology stack. A team gets access to a model, immediately asks what it can build around it, and then lets the application grow outward from that model.

Prompts become business logic. Conversation history becomes state management. Tool descriptions become application programming interface contracts. The model learns which databases exist, which operations it can run, how to interpret the results, and what should happen next. Before long, the model is doing far more than inference. It's routing requests, coordinating workflows, maintaining state, applying policy, interpreting schemas, handling errors, and deciding when work is complete.

This can feel incredibly productive at first because the first version is wonderfully simple. One model, one prompt, a handful of tools, and the demo works. Then the system grows, and suddenly you need another model because the original one is too expensive, a smaller model can perform one task faster, a new model produces better structured output, the organization changes vendors, the application programming interface changes, or the original model simply stops being competitive six months later.

That's when you discover that changing the model means changing everything around it. The model was never contained by the architecture because the application was built outward from the model in the first place. That's the model trap.

## Models Are Dependencies

We already know how to think about this problem in traditional software. Databases are dependencies, message brokers are dependencies, object stores are dependencies, authentication providers are dependencies, and cloud services are dependencies. We design boundaries around them because we assume implementations can change, because they frequently do.

Models should be treated the same way. A model is an inference dependency. It accepts context, performs a probabilistic computation, and returns a result. That result may be extraordinarily sophisticated. The model may reason across hundreds of pages of information, interpret an image, classify an event, write code, or propose a strategy, but none of those capabilities make the model the architecture.

The architecture determines where inference is allowed to happen, what information is available to it, what output is expected, how that output is validated, and what happens after inference completes. Those decisions belong to the system, not the model.

## What Actually Survives Model Changes

Imagine an AI application that lives for five years. During that time it will probably see several model generations, multiple model families, and possibly more than one vendor. The best model for a task today may not be the best model next year, and in this market it may not even be the best model next quarter.

Other parts of the system are much more durable. Your domain boundaries will probably still exist. Your application programming interfaces will probably still exist. Your data model, security policies, workflow semantics, observability requirements, and audit requirements will probably still exist. Those are architectural assets because they represent how the system behaves, not which implementation happens to perform one part of the work.

This is why I increasingly think about AI systems in terms of model-independent contracts. The contract defines the job, while the model is simply one implementation capable of performing that job. When that distinction is clear, model replacement becomes an implementation decision instead of an architectural rewrite.

## The Architecture Should Constrain the Model

A strange inversion has happened in many AI systems. Instead of the application telling the model exactly what responsibility it owns, the model is given a large pile of context and allowed to figure out what the application is trying to accomplish. The more ambiguous the system becomes, the more context gets pushed into the model in the hope that the model can reconstruct the intent.

That's backwards. The architecture should constrain the model. A worker should have a bounded responsibility, receive a bounded input, operate within a known context, and return a defined output that the rest of the application understands. The model shouldn't need to understand the entire system in order to perform one task.

This is one of the architectural ideas behind PortfolioOS, or pOS (the financial system I've been building to separate market intelligence, investment research, portfolio construction, household planning, and portfolio maintenance into bounded subsystems). Instead of building one giant financial agent that understands markets, portfolio construction, household goals, risk, taxes, security selection, and trade execution, those responsibilities are deliberately separated.

Market Intelligence (the pOS subsystem responsible for determining the current market regime and publishing a dated market posture) owns a different problem from Hunt (the subsystem responsible for researching and ranking potential investments). Portfolio Construction (the subsystem responsible for assembling securities into portfolios) owns a different problem from Loop (the subsystem responsible for ongoing portfolio maintenance and detecting when something materially changes).

Each subsystem owns a bounded responsibility, and none of them require a model that understands all of PortfolioOS. That boundary is what makes the system architecture durable even when the models inside it change.

## Why Bounded Workers Matter

Once responsibilities are bounded, model selection starts to look very different. A reasoning-heavy research task may justify a larger model, while a classification task may need something much smaller. A document extraction worker might use a vision model, while a compiler that converts an already-reasoned decision into a strict schema might use another model entirely. Some tasks may not need a model at all.

This is where multi-model applications become interesting, not because using several models is inherently clever, but because architecture allows models to become interchangeable workers. A worker isn't defined by the model running inside it. It's defined by its contract with the rest of the system.

If a 30-billion-parameter model performs that contract today and a 7-billion-parameter model performs it tomorrow, the architecture shouldn't care. The worker still receives the same job, the system still expects the same result, and everything outside that seam remains unchanged.

That's a fundamentally different way of building AI applications. Instead of choosing one model and asking it to become the application, the application defines the jobs, and models compete to perform them.

## Deterministic Software Still Has a Job

The enthusiasm around models has also caused us to forget something fairly obvious: traditional software is extremely good at being deterministic. If I need to calculate a portfolio weight, I don't want a language model estimating it. If I need to determine whether a value exceeds a threshold, I don't need reasoning. If I need to enforce a permission boundary, I definitely don't want the model deciding whether that boundary applies.

Models are useful when the problem contains ambiguity, while software is useful when the problem doesn't. Good AI architecture deliberately separates those two worlds so probabilistic behavior exists only where probabilistic behavior actually adds value.

A model might determine that a company's competitive position has materially weakened, while software determines whether that assessment crossed the threshold required to trigger a portfolio review. A model might extract obligations from a hundred-page document, while software validates that the required fields exist. A model might propose an action, while software determines whether that action is actually allowed.

That division of labor makes the system easier to reason about because the model is no longer being asked to compensate for every kind of application logic. Inference does inference, and software remains responsible for the things software already does well.

## State Should Not Live in the Model

Another architectural smell appears when the model becomes responsible for remembering how the system arrived at its current state. Conversation history slowly turns into the database, and the application keeps feeding larger and larger transcripts back into the model because important decisions happened somewhere inside them.

Eventually the model isn't just reasoning about the current request. It's reconstructing the application from its own history. That's fragile because the system no longer owns its state in a form that anything else can reliably inspect.

State should belong to the system. If PortfolioOS decides that the market regime is late cycle, that decision should become persistent state with evidence, timestamps, confidence, and history. The next worker shouldn't need to reread an old conversation and infer that a late-cycle decision occurred. It should read the current market posture.

This distinction sounds small, but it fundamentally changes how the system behaves. The model produces information, while the system owns information. Once that separation exists, models can disappear, restart, or be replaced without taking the application's memory with them.

## Design the Seams First

The most durable part of an AI architecture isn't the prompt. It's the seam between responsibilities. A seam defines where one responsibility ends and another begins, what crosses that boundary, what can't cross it, what the producer guarantees, and what the consumer is allowed to assume.

This is why I spend so much time designing contracts between subsystems before worrying about which model will execute the work. If the seam is good, models become easier to replace. If the seam is bad, the model gradually becomes responsible for compensating for architectural ambiguity.

The prompt gets longer, more context gets injected, and more hidden assumptions accumulate. Eventually the model appears indispensable because it is the only thing that understands all of the accidental coupling inside the system.

At that point, replacing the model becomes terrifying, but the problem was never model replacement. The problem was that there was no durable architecture around it.

## What This Looks Like in PortfolioOS

PortfolioOS has gone through several architectural iterations, and one of the most important changes was moving away from thinking about intelligence as a single central capability. There's no PortfolioOS super-agent that understands the entire financial system and decides what happens next.

Instead, there are systems that produce specific forms of intelligence. Market Intelligence evaluates market conditions. Hunt evaluates investments. Portfolio Construction assembles portfolios. Home Office (the pOS subsystem responsible for translating household goals, obligations, and timelines into capital requirements) determines what the household actually needs the portfolio to accomplish.

Those systems communicate through explicit contracts and persistent state, while models operate inside those systems only where inference is useful. The model responsible for investment research can change without redesigning Home Office. The model performing market analysis can change without rewriting Portfolio Construction. A deterministic calculation service can replace a model entirely if we discover that a particular task never required inference in the first place.

The application survives because the intelligence is bounded. The architecture owns the relationships between the pieces, while the models perform jobs inside those boundaries.

This also changes how model selection happens. Instead of asking, **“What model should PortfolioOS use?”** the question becomes, **“What characteristics does this worker require?”** Reasoning depth, context size, structured-output reliability, latency, vision capability, cost, and hardware requirements become engineering constraints for a specific job rather than requirements for the entire system.

That's a much healthier place to be because model selection becomes local. You can optimize one worker without destabilizing the rest of the application.

## Build for the Model You Have, Architect for the Model You Don't

There's nothing wrong with being excited about models. They are extraordinary pieces of technology, and better models absolutely unlock new categories of applications. The mistake is assuming that any particular model will remain important long enough to deserve architectural ownership of the system around it.

Models are moving too quickly for that. The model you choose today should be treated as temporary, while the architecture should be designed to survive its replacement.

Build the prompts, tune the inference parameters, measure the model, and exploit every capability it gives you. At the same time, put a seam around it, give it a bounded responsibility, keep persistent state outside of it, use deterministic software where deterministic software is better, and make both its inputs and outputs explicit.

Then assume that one day you will delete the model and replace it with something better. If doing that sounds terrifying, the model has probably become too much of your system.

The model isn't your architecture. The architecture is everything that allows the model to be replaced.

