---
title: "Small Models, Explicit Boundaries"
date: 2026-04-29
draft: false
description: "Small models work best when their responsibilities are narrow, their seams are explicit, and the surrounding system stays deterministic."
tags:
  - slm
  - seams
  - architecture
  - systems
categories:
  - Small Model Systems
image: cover.png
---

There's a moment in almost every AI application where the architecture starts to get lazy. The first model works surprisingly well. It can read the input, reason about the problem, produce structured output, and even make a few decisions along the way. Someone adds another prompt, then another tool, then another responsibility. Before long, the model that started as one component has quietly become the application.

I've built that system before, and at first it feels elegant. One capable model sits in the middle, surrounded by context, tools, and instructions. Give it enough information, explain what you want, and let it figure out the rest. The model becomes the router, analyst, planner, classifier, formatter, and sometimes even the thing responsible for deciding whether its own output is valid.

The problems tend to appear later. Maybe the model starts misclassifying a subtle signal, or a prompt update improves one task while making another worse. Maybe you want to replace the model, but discover that half of the application behavior exists only inside a system prompt. Maybe someone asks why the system made a decision, and the best answer you can give is essentially, "the model thought that was the right thing to do."

That's usually when the architecture problem becomes visible. The issue isn't necessarily that the model is too small. More often, the problem is that the boundary around the model has become too large.

## Small Models Are Better When the Job Is Smaller

There's a common assumption that the way to improve an AI application is to use a larger model. Sometimes that is true. A larger model may reason better, understand more nuance, follow complex instructions more reliably, or operate over a larger context. If the task genuinely requires those capabilities, using a larger model can be the right engineering decision.

Model size can also hide architecture problems, though. If one model is responsible for understanding the user, identifying intent, gathering evidence, reasoning about that evidence, deciding what action to take, formatting the result, and validating its own output, then increasing model capability may make the system appear more reliable without making the architecture any better. You have simply purchased more intelligence to compensate for an undefined boundary.

Small models force a different conversation because their limitations appear sooner. Instead of asking whether a model can do everything the application needs, you start asking what exactly this particular model needs to do. That's a much more useful architectural question because it moves the discussion away from general intelligence and toward specific responsibilities.

In PortfolioOS, or pOS (my portfolio research and decision system), I don't want a model responsible for "understanding the market." That boundary is effectively meaningless. I want bounded workers responsible for specific inference tasks with defined inputs and outputs. One worker might classify evidence, another might determine whether a piece of news strengthens or weakens an existing thesis, another might extract entities and relationships from an article, and another might summarize a company's competitive position from a constrained evidence set.

Each of those jobs can be evaluated independently, and each can use a model appropriate to the task. More importantly, each worker can fail without taking the entire system with it. That's where small models become much more interesting because the smaller model is no longer being asked to compensate for the absence of architecture.

Eugene Yan argues the same thing from the systems-design side. His <a href="https://eugeneyan.com/writing/llm-patterns/" target="_blank" rel="noopener">patterns for building LLM systems</a> push against monoliths deliberately: separate models for separate tasks, retrieval so the model only has to handle what it's genuinely good at, each piece measurable on its own. The narrow job isn't a limitation you tolerate for a small model. It's the thing that makes the small model's behavior legible in the first place.

## The Boundary Is the Architecture

A model shouldn't receive whatever context might be useful. It should receive the smallest complete set of information required to perform its job. That distinction sounds minor, but it changes almost everything about the system because it forces you to decide what the worker owns and what belongs elsewhere.

Consider a worker whose responsibility is to determine whether new evidence affects an existing investment thesis. It doesn't need access to the user's entire portfolio, brokerage account balances, the history of every previous research session, or the system's current portfolio construction rules. It needs the existing thesis, the new evidence, a definition of the possible classifications, and enough supporting context to distinguish between them.

The output should be equally constrained. Perhaps the worker returns `strengthens`, `weakens`, `neutral`, or `insufficient evidence`, along with a confidence score and references to the supporting evidence. The model shouldn't then decide whether the position should be sold, rewrite the thesis, rebalance the portfolio, or determine what happens next. Those responsibilities belong to other parts of the system.

This is the boundary that matters. The model performs inference inside it, returns a result across a seam, and stops. Once the responsibility is that narrow, the rest of the architecture becomes much easier to reason about.

## Intelligence Should End at the Seam

In [the previous post](/p/the-seam-is-the-product/), I wrote about why the seam is the product. The seam is the explicit contract between components. It defines what crosses a boundary, what doesn't, and what each side is allowed to assume. Small model systems depend on those seams because without them, you don't really have a collection of specialized models. You have a distributed prompt.

That failure mode is easy to create. Every worker starts reaching into shared state, every model begins depending on undocumented context, one worker assumes another already normalized something, and another quietly compensates for malformed output. Eventually, the behavior of the system depends on an invisible network of assumptions spread across prompts.

The alternative is to make intelligence terminate at the boundary. A model receives a contract, performs inference, and produces a contract. Everything outside that transformation belongs to the system. Validation belongs to deterministic code, persistence belongs to the store, retries belong to infrastructure, authorization belongs to policy, and routing should usually belong to deterministic logic whenever the routing decision can be expressed deterministically.

The model should own only the part that genuinely requires inference. That separation is one of the most important architectural distinctions I've found while building AI systems because it makes the uncertain behavior explicit instead of allowing it to spread throughout the application.

## Models Should Not Own State

Persistent state is one of the easiest ways to accidentally enlarge a model's boundary. Suppose a research worker analyzes a company every week. It might be tempting to give the model the previous analysis, continue the conversation, and ask it to update its understanding. That works, but now the definition of the system's current understanding lives inside an evolving model conversation.

Instead, the system should own the state. The store contains the current thesis, previous evidence, classifications, timestamps, confidence values, and whatever else the application considers durable. The worker receives the specific state required for the current operation and returns a proposed change. The application then decides whether that change is valid and whether it should be persisted.

This is more cumbersome than simply continuing the conversation with the model, but it is enormously easier to debug. You can inspect the state before the model ran, inspect exactly what the model received, inspect exactly what it returned, rerun the same operation with another model, compare model versions, and reject malformed output without corrupting persistent state.

Most importantly, you can replace the model without replacing the application's memory. The system should be responsible for remembering what happened, while the model is responsible for performing the bounded inference required at that moment.

## Small Models Make Failure Smaller

One of the strongest arguments for bounded models has very little to do with cost. It has to do with failure containment. If a general-purpose model performs six different cognitive tasks during a single operation, determining why the final result is wrong can be surprisingly difficult.

Maybe it misunderstood the source, classified the evidence incorrectly, misunderstood the existing thesis, reasoned correctly but chose the wrong action, or produced the right decision and then serialized the output incorrectly. When all of those operations happen inside one inference, failure becomes ambiguous because there's no obvious place to isolate the problem.

Bounded workers turn one large failure surface into several smaller ones. If the evidence classifier is wrong, test the evidence classifier. If the thesis impact worker is wrong, test the thesis impact worker. If the model output violates the schema, reject it before anything downstream sees it. Each boundary can have its own evaluations instead of forcing you to evaluate the intelligence of the entire application at once.

This becomes especially useful with small models because their weaknesses tend to be more visible. A 3 billion parameter model that consistently struggles with one classification boundary tells you something concrete about the job you have defined. You can improve the prompt, change the representation, add deterministic preprocessing, or replace that worker with a stronger model. A giant model may simply absorb the ambiguity for longer, which can make a weak boundary look acceptable until an input finally arrives that the model can't rescue.

## Different Boundaries Deserve Different Models

Once model workers are genuinely isolated, there stops being a reason for every worker to use the same model. This sounds obvious, but many AI applications still treat the model as an application-level decision. The team chooses GPT, Claude, Gemini, Llama, Gemma, Qwen, or something else, and then builds the application around that choice.

I think that is backwards. The boundary should choose the model because different inference jobs reward different capabilities. A worker that needs nuanced language classification may perform best with one model, while a worker extracting structured data from predictable documents might work perfectly with something dramatically smaller. A vision worker may require a multimodal model, while a reasoning-heavy worker may justify a larger model. A compiler-style worker that transforms one known structure into another may require very little general reasoning at all.

This is the lesson behind my earlier experience with Qwen and Gemma. Both models were small enough to run locally, and both looked capable on paper, but they behaved very differently when the task required subtle semantic judgment. One was better at following the visible structure of the problem, while the other was better at understanding the meaning hiding underneath it.

That didn't mean one model was universally better. It meant the boundary cared about something the benchmark didn't capture. Once workers are isolated, those differences become useful because you can place each model where its behavior fits the task instead of forcing one model to serve every responsibility in the application.

The result is a heterogeneous system by design. Model selection becomes a worker-level decision rather than a platform-level commitment.

## Determinism Around Inference

The smaller the inference boundary becomes, the more of the surrounding system can become deterministic, and that is exactly what I want. A model can classify whether evidence strengthens a thesis, while code verifies that the classification belongs to the allowed set. A model can extract a set of entities, while code verifies their identifiers, removes duplicates, and resolves references.

The same pattern applies elsewhere. A model can propose an action, while policy determines whether that action is allowed. A model can produce a summary, while the system attaches provenance, timestamps, version information, and the identifiers of the evidence used to produce it. The model handles the ambiguous part, while software handles everything we already know how to define.

That separation produces systems that are much easier to reason about because the uncertain parts are visible. Instead of spreading probabilistic behavior throughout the application, you can point to the exact places where inference occurs. Those become the places that require evaluation, observability, stronger guardrails, and careful model selection.

Everything around those boundaries should behave like software.

## Explicit Boundaries Make Models Replaceable

There's another architectural advantage that becomes increasingly important as models improve. If a worker accepts a defined input contract and emits a defined output contract, the implementation behind that boundary can change without requiring the rest of the system to care.

Today, that worker might use Gemma. Tomorrow, it might use Qwen. Next month, it might use a fine-tuned model. Eventually, you may discover that the task never required a model at all and replace the worker with deterministic code. That should be considered a successful architectural outcome rather than a retreat from AI.

The goal isn't to maximize the amount of AI inside the system. The goal is to use inference exactly where inference provides value. Models are unusually fast-moving dependencies, and their capabilities, context sizes, licensing, inference costs, hardware requirements, and performance characteristics change constantly. An architecture built around a particular model inherits that volatility.

An architecture built around explicit boundaries can take advantage of it instead. When a better model arrives, you replace the worker. When a cheaper model becomes good enough, you replace the worker. When a local model catches up with the hosted model, you replace the worker. The rest of the application should remain largely untouched because the contract, not the model, is what the system depends on.

## The Architecture Starts Looking Boring

The strange thing about well-designed AI systems is that they eventually stop looking very AI-centric. There are APIs (application programming interfaces, the contracts services use to communicate), schemas, persistent state, queues, workers, policies, and deterministic services coordinating operations. Inside a handful of carefully chosen boundaries, there are models doing the things ordinary software can't reliably do.

That's the architecture I increasingly trust because the model is no longer being asked to be the application, orchestrator, database, policy engine, and reasoning layer at the same time. It becomes what it should have been all along: a bounded inference component inside a larger system.

Once you accept that idea, small models stop looking like compromises. They start looking like architectural primitives because their usefulness comes from having a narrow, explicit responsibility rather than pretending to possess enough general intelligence to understand the whole application.

You don't need one model smart enough to understand your entire system. You need a system designed well enough that no model has to.
