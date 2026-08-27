---
title: "Your AI Agent Probably Shouldn't Be an Agent"
date: 2026-04-17
draft: false
description: "The best AI systems know exactly where inference belongs, and where ordinary software should take over."
tags:
  - ai
  - architecture
  - agents
  - small-language-models
categories:
  - Small Model Systems
image: cover.png
---

A while ago I was looking at a workflow that had been proudly described as an AI agent. The agent received a request, inspected some state, decided which tool to call, assembled a few parameters, made the call, examined the response, updated a record, and returned the result. On paper, it looked impressive. There was a model in the middle of the diagram, arrows going everywhere, and enough autonomy to justify calling the whole thing agentic.

There was only one problem: almost none of the work required intelligence. The request had already been classified. The available tools were known. The parameters could be derived from structured data. The state transition was governed by explicit rules. The output format had a schema, and even the error handling had predictable branches.

We had taken a deterministic program and replaced a collection of perfectly ordinary functions with a language model repeatedly asking itself what to do next. That is becoming one of the stranger habits in AI application design.

We have spent decades learning how to make software predictable, testable, observable, and recoverable. Then large language models arrived, and suddenly we started handing deterministic responsibilities to probabilistic systems because the word *agent* sounded more sophisticated than *workflow*. The interesting question is not whether an AI model can perform a task. The interesting question is whether inference is actually required.

## The Agent Reflex

There is a pattern I keep seeing in AI systems. A team identifies a business process, places a language model at the center of it, gives the model access to several tools, writes a system prompt explaining the rules, and calls the result an agent.

The model becomes the router, the workflow engine, the policy evaluator, the state machine, and the retry handler. Sometimes it even becomes the database query planner, despite the fact that the application already knows exactly what data it needs. Then everyone is surprised when the resulting system is expensive, difficult to test, hard to reproduce, and occasionally does something spectacularly stupid.

The mistake is subtle because the model usually *can* do all of those things. A sufficiently capable model can examine a request, infer which function should execute, decide what state should change, and determine what happens next. That does not mean those decisions belong inside inference.

Capability is not the same thing as architectural responsibility. If there is exactly one correct next step, your application should probably take that step instead of asking a model for an opinion.

## Inference Is a Boundary, Not an Architecture

This distinction has become one of the foundational ideas behind how I build AI systems. Inference is a subsystem. It is not the system.

A language model is useful when software reaches a boundary where the input cannot be handled reliably through deterministic rules alone. Natural language interpretation is the obvious example. Nuance detection, semantic classification, summarization, entity extraction from messy text, and reasoning over ambiguous evidence are other good candidates.

Those are places where we genuinely do not know how to write a conventional function that produces the required result. So we invoke a model, let it cross that uncertainty boundary, and require it to produce a constrained result before control returns to deterministic software.

That is very different from allowing the model to orchestrate the entire application. The model should solve the fuzzy part, while the application solves everything else.

## Deterministic Work Should Stay Deterministic

Consider a simple portfolio research workflow. An application receives a piece of financial news. It needs to determine which company the article concerns, decide whether the information affects an existing investment thesis, store the resulting evidence, update the appropriate record, and notify another subsystem that new evidence exists.

Some of those steps require inference. Identifying the company from loosely written text might require a model. Determining whether the article strengthens, weakens, or does not materially affect a thesis probably requires one too.

But writing the evidence to the correct database table does not. Checking whether the company exists, generating an identifier, validating the response schema, recording a timestamp, publishing an event, and retrying a failed database transaction do not require inference either. Those are software problems.

Yet it is surprisingly common to see architectures where a model receives five tools and repeatedly decides which one to invoke until the workflow is complete. We already have technology for executing known sequences of operations. It is called software.

## Where Models Actually Belong

The easiest way to find the correct boundary is to ask what kind of uncertainty exists at each step. Suppose an incoming research document contains the sentence:

> Management expects accelerating demand from hyperscale customers despite near-term margin pressure from capacity expansion.

Several interesting questions require interpretation. Which business drivers are being discussed? Is the capacity spending evidence of weakness, or evidence of demand? Does the statement strengthen a long-term thesis while weakening near-term profitability? Is the language meaningfully different from management's previous guidance?

Those are inference problems because the answer depends on meaning. Once the model returns something structured, however, the nature of the problem changes.

Imagine the model produces:

```json
{
  "company": "Example Semiconductor",
  "signal": "thesis_supporting",
  "horizon": "long_term",
  "confidence": 0.84,
  "drivers": [
    "hyperscale demand",
    "capacity expansion"
  ]
}
```

From that point forward, the application should become boring again. It should validate the schema, resolve the company identifier, store the evidence, associate it with the thesis, update the evidence timestamp, publish the event, and continue the workflow.

Nothing about those steps becomes better because a language model decides whether they should happen. In fact, almost every desirable property of the system becomes worse.

## The Deterministic Sandwich

I have started thinking about good AI application architecture as a deterministic sandwich. Deterministic software prepares the problem, inference handles the ambiguous middle, and deterministic software validates and executes the result.

Conceptually, it looks something like this:

```text
INPUT
  │
  ▼
Deterministic preparation
  │
  ├── Load state
  ├── Validate inputs
  ├── Gather allowed context
  └── Construct bounded request
  │
  ▼
INFERENCE
  │
  ├── Interpret
  ├── Classify
  ├── Extract
  └── Reason
  │
  ▼
Structured result
  │
  ▼
Deterministic execution
  │
  ├── Validate schema
  ├── Apply policy
  ├── Persist state
  ├── Trigger services
  └── Record provenance
  │
  ▼
OUTPUT
```

The model gets a very specific job, and more importantly, it does **not** get all of the other jobs. This architecture gives inference room to do the thing it is good at while keeping the surrounding system conventional enough to reason about.

That turns out to matter enormously once the application grows beyond a demo.

## Why Tool Calling Does Not Automatically Mean Agency

Tool calling has blurred this boundary. Modern models can emit structured function calls, which makes it tempting to treat every operation as something the model should decide to invoke.

Sometimes that is exactly right. If a user asks:

> Find out why our application slowed down yesterday.

The system may genuinely need inference to determine whether it should inspect metrics, logs, traces, deployment history, or several of them together. The path through the investigation may depend on evidence discovered along the way, which makes it a legitimate reasoning loop.

Now compare that with:

> Generate the monthly report.

If the monthly report always requires loading the same records, running the same calculations, generating the same charts, and placing them into the same document structure, there is no meaningful decision for an agent to make. The workflow already exists.

Adding a model as the coordinator does not make the workflow intelligent. It makes the workflow probabilistic. This is one of the tests I use when looking at an agent design: **Does the model actually have a decision to make?** If the answer is no, remove it from that step.

## The Cost of Putting Models in the Wrong Places

Using inference unnecessarily creates costs that are easy to ignore during prototyping. The obvious one is compute. A function call takes microseconds or milliseconds, while a model decision may require hundreds or thousands of tokens, specialized hardware, and substantially more latency.

The deeper cost is uncertainty. A deterministic function can usually be tested against known inputs and expected outputs. The same input should produce the same behavior every time. Inference does not provide that guarantee.

Even with constrained decoding and structured outputs, the model is still interpreting the problem rather than executing formally defined logic. That uncertainty then spreads outward into the rest of the system.

Retries become harder to reason about because a second execution may choose a different path. Debugging becomes harder because reproducing the exact decision may require reconstructing prompts, context, model versions, sampling parameters, and external state. Observability becomes more complicated because knowing *what happened* is no longer enough. You also need to understand *why the model decided it should happen*.

Policy enforcement becomes dangerous if the model is responsible for interpreting whether an operation is allowed, and testing becomes statistical rather than exact. None of these problems mean models are bad. They mean inference has a cost, and you should spend uncertainty where uncertainty buys you something.

## Bound the Model

This is where the idea connects back to the architecture I have been building in PortfolioOS (pOS, the AI-driven portfolio research and management system I use as a running architecture experiment).

pOS does not treat intelligence as one giant agent wandering around the system. It breaks inference into bounded workers. A worker gets a defined input, a defined responsibility, a limited set of context, and a defined output contract. The model performs the semantic work inside that boundary, then control returns to the surrounding system.

One worker might classify evidence. Another might evaluate whether evidence changes an investment thesis. Another might synthesize competing signals. Those workers can still use sophisticated models, reason over complex evidence, and make judgments that conventional software cannot realistically make.

What they cannot do is quietly inherit responsibility for the rest of the application. State remains state, policy remains policy, storage remains storage, workflow remains workflow, and inference remains inference.

That separation makes the individual models much more replaceable because the architecture does not depend on a particular model behaving like an application framework. That matters more than it might initially appear.

As I wrote in *The Model Is Not Your Architecture*, models are components. They will change constantly, while the boundaries around them should not.

## The Architecture Test

When I look at a proposed AI agent now, I mentally walk through each responsibility and ask a few questions.

| Question                                                               | If the answer is yes               |
| ---------------------------------------------------------------------- | ---------------------------------- |
| Is there one known correct next step?                                  | Use deterministic code.            |
| Can the rule be expressed explicitly?                                  | Use deterministic code.            |
| Is the operation a state transition?                                   | Use deterministic code.            |
| Is this validation against a known contract?                           | Use deterministic code.            |
| Is this access control or policy enforcement?                          | Definitely use deterministic code. |
| Does the task require interpreting ambiguous meaning?                  | Consider inference.                |
| Does the correct path depend on evidence discovered dynamically?       | Consider bounded agency.           |
| Are multiple reasonable answers possible?                              | Consider inference.                |
| Would writing conventional rules require approximating human judgment? | Consider inference.                |

This does not eliminate agents. It makes them smaller, which is probably a good thing.

The places where genuine agency is useful become much easier to see once we stop calling every model-backed workflow an agent. There are real problems where an application needs to investigate an unknown environment, generate hypotheses, choose among tools, evaluate intermediate results, and adapt its strategy. Those systems deserve agentic architectures.

Your CRUD (Create, Read, Update, Delete) workflow probably does not.

## Build Software That Knows When Not to Think

There is an odd assumption hiding inside much of the current agent conversation: more reasoning is treated as inherently better. I think mature AI systems will eventually move in the opposite direction and become extremely deliberate about where reasoning is allowed to occur.

Most of the application will look surprisingly conventional. There will be APIs (Application Programming Interfaces, structured boundaries through which software components communicate), schemas, databases, queues, state machines, policy engines, validators, and ordinary services doing ordinary software things.

Then, at carefully chosen boundaries, the system will encounter something conventional software cannot reliably understand. A model will be invoked, make the judgment, return a constrained result, and get out of the way.

That architecture is less exciting than drawing one giant box labeled **AGENT** in the middle of a diagram, but it is much easier to operate. The goal is not to build the most agentic system possible. The goal is to build a system that knows exactly when it needs intelligence, and perhaps more importantly, exactly when it does not.
