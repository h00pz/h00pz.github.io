---
title: "Context Windows Are Not Architecture"
date: 2026-07-22
draft: false
description: "A larger context window can hide missing boundaries for a surprisingly long time, but it does not create durable state or clear responsibility."
tags:
  - ai
  - architecture
  - systems
  - context
  - retrieval
categories:
  - architecture
image: cover.png
---

There is a particular kind of relief that arrives with a larger context window. A problem that used to demand careful engineering, deciding what the model should see, retrieving the right documents, and trimming everything that did not belong, suddenly seems to dissolve. The window is bigger now, so you put more into it. The whole research history, every prior analysis, the entire filing, the complete conversation. And it works.

That is the dangerous part. It works well enough, and for long enough, that the architecture never gets built.

I have done this. The first time a model could hold far more than I expected, my instinct was not to design better boundaries. It was to stop designing them. Why bother deciding what a worker needs when I can simply hand it everything and let the model sort out what matters? For a while the system got simpler, the prompts got longer, and the results stayed good.

Then the inputs grew, the history accumulated, two documents in the pile quietly contradicted each other, and the model started making confident decisions based on information that should never have been in front of it. Nothing had broken in the ordinary sense. The window had just been doing a job that belonged to the architecture, and eventually it could not do that job well enough.

## A Context Window Is Memory, Not Architecture

I have written before that state belongs to the system while context belongs to the model. A context window is temporary working memory. It exists for the duration of a single inference, holds whatever you decided to put in it, and then disappears. It has no owner, no schema anyone else can inspect, no history, and no authority. It is scratch space.

That is exactly why it is so tempting to overload. Scratch space feels free. If a worker might need something, you can add it to the prompt, and the model will probably ignore what it does not use. The window absorbs indecision, and indecision is comfortable.

Architecture is the opposite of scratch space. It is the set of durable decisions about who owns what, which component may depend on which, what persists, and what crosses each boundary. None of those decisions live inside a context window, because the window forgets everything the moment the request ends. Whatever a model needed to know, whatever it concluded, and whatever authority it appeared to exercise all vanish with it.

So when I put the entire system into the window, I am not building an architecture that happens to use a model. I am building an application whose memory, boundaries, and reasoning all live inside a temporary buffer that no other part of the system can see, audit, or reuse.

## Bigger Windows Hide Missing Boundaries

The reason this pattern survives so long is that a larger window is genuinely good at compensating for absent architecture. This is the same compensating behavior I keep running into. A capable model handed enough context will paper over an enormous amount of missing design.

If two subsystems have no clear seam, you can hand the model both of their internal states and let it reconcile them. If a worker's responsibility was never bounded, you can give it everything and let it decide what its job actually is. If the system does not really know what it remembers, you can pour the whole history into the prompt and let the model reconstruct the current state on the fly.

Each of those is a boundary problem wearing a context-window costume. The window makes the symptom disappear without touching the cause. And because the result looks fine, there is no pressure to fix the underlying design. The architecture is missing, but nobody can tell, because a large enough buffer is quietly holding the system together.

The failure, when it comes, does not look like a missing boundary. It looks like the model suddenly getting something wrong. The instinct is to fix the model or enlarge the window further, which buys more time and hides the cause a little longer. You can ride that curve for a remarkably long time. You just cannot ride it forever.

## What the Window Cannot Do

It helps to be precise about what a context window structurally cannot provide, no matter how large it becomes.

It cannot create durable state. Anything the model concludes is gone unless some component outside the window writes it down deliberately. A window full of history is not memory; it is a copy of memory that belongs to whoever assembled the prompt.

It cannot establish ownership. Putting Brain's market view and Hunt's candidate evidence into the same prompt does not decide which subsystem owns which concept. It just places two definitions next to each other and hopes the model does not blend them. In PortfolioOS, or pOS (my portfolio research and decision system), that blending is exactly the kind of quiet failure I most want to avoid.

It cannot carry authority. A model that appears to make a decision inside a giant prompt has not been granted the right to make it. The window cannot enforce that a research worker is allowed to classify evidence but not allowed to change a position. Authority has to be a property of the architecture, checked deterministically after the model returns, not an accident of what happened to be in scope.

It cannot guarantee provenance. When everything is dumped into one buffer, the model's conclusion is no longer traceable to specific evidence. You are left with an answer and a haystack, and no reliable way to say which straw produced it.

And it cannot make the result reproducible. Reassemble a slightly different pile of context, or let the history grow by one more document, and the same request can produce a different answer for reasons no one recorded.

Every one of those is an architectural property. A window cannot supply any of them, because it is the wrong kind of thing.

## The System Should Decide What the Model Sees

The healthier stance is that the model does not get to see whatever is available. The system decides what it sees, deliberately, for each task.

This is the same discipline as bounding a worker's responsibility, applied to its inputs. A worker that judges whether new evidence changes an investment thesis needs the thesis, the new evidence, the set of allowed classifications, and enough surrounding context to tell them apart. It does not need the entire portfolio, every prior research session, or the household's financial plan, even if all of that would fit.

Fitting is not the test. The test is relevance and authority. Every additional thing in the window is something the model might weight, misread, or let override the piece that actually mattered. A larger window raises the ceiling on how much irrelevant material you can accidentally include, which is not obviously a gift.

When the system owns the decision about what enters the window, that decision becomes inspectable. You can look at exactly what a worker received, reason about why, change it on purpose, and test the worker against a known input instead of against an ever-growing accumulation of whatever happened to be lying around.

The worker that writes my weekend brief makes this concrete. The evidence handed to the model is governed by a budget. It started at three hundred thousand characters and I later cut it to a hundred and twenty thousand, roughly thirty thousand tokens. The number matters less than the behavior at the edge. When a branch has more evidence than the budget allows, the system does not silently truncate to fit. It keeps the freshest evidence, drops the older tail, and writes the names of everything it dropped into a `couldNotCover` list attached to the result. The model still gets a bounded input, but nothing disappears quietly. A person can look afterward and see precisely which older material never reached the model and decide whether that was the right call. That honesty is only possible because a component I can inspect made the decision, rather than a window silently absorbing whatever fit.

## Size the Context to the Task

Once the system owns what a worker sees, a second question follows immediately, and it is one I think most AI systems never actually ask. How much context does this particular job need? Not how much will fit, and not how much is available. How much does the decision in front of this worker genuinely require.

The answer is not a constant. It is a property of the task, and it varies enormously across a system. A worker that transforms one known structure into another, taking a reasoned decision and emitting strict schema, needs almost nothing beyond its input. A worker that classifies evidence into one of a handful of categories needs the item, the category definitions, and just enough surrounding detail to tell the close cases apart. A worker that has to judge whether a later statement supersedes an earlier one, the kind of relationship the Gold Trap turned on, needs every statement that could plausibly interact, but chosen for relevance, not swept in by volume. And a genuinely open-ended reasoning task may justify both a larger context and a larger model. Those are four different sizes, and using one budget for all of them is how you end up simultaneously starving the hard jobs and drowning the easy ones.

The framing I have found useful is the same one I use for choosing models. There, the question is not which model is best but which is the smallest model that can reliably do the job. For context, the question is not how large the window is but what is the smallest complete context for this decision. Completeness is the real constraint. Too little context and the worker fills the gap with a guess that arrives looking like a fact. Too much and the one decisive sentence competes with a thousand irrelevant ones and sometimes loses. There is a right size in between, it belongs to the task, and it is discoverable. You can hold a worker's evaluations fixed, add or remove context, and watch whether the answer actually changes. If more context does not change the answer, it was never load-bearing.

In practice this means a context budget is part of a worker's contract, not a global setting. Different workers get different budgets for the same reason they get different models. The per-pack token caps and the evidence budget in pOS are not arbitrary numbers I picked to be safe. They are attempts to name, per job, how much context that job actually needs, so the window is spent deliberately instead of filled by default.

## Retrieval Is an Architectural Decision

This reframes retrieval. It is easy to treat retrieval as a workaround for windows that used to be too small, a way to cram a large corpus through a narrow opening. As windows grow, that framing suggests retrieval becomes less necessary. I think it is the reverse: retrieval is how the architecture decides what a model sees, and it matters more as the window grows, not less.

The point of retrieval was never only to fit. It is to choose. Choosing the right five documents is not a compression tactic; it is an act of design that says these are the inputs this task depends on and the rest is noise. Doing that well requires the surrounding structure I care about anyway: stores that own the durable state, APIs that expose it through explicit contracts, and identifiers that let a worker ask for precisely the state it needs.

This is concrete enough in pOS that it has its own seam. When I built the conversational side of the Home Office, the subsystem that translates a household's goals into mandates, the very first component was not the model. It was a topic context-retrieval seam whose only job is to decide which slice of the ongoing conversation a given turn should actually see. The model that answers the turn never gets the whole history. It gets what the retrieval seam selected, because deciding that is architecture and answering the turn is not.

The Gold Trap taught me this from the failure side. A model handed a large document extracted every true fact and still reached the wrong conclusion, because a later update had silently superseded an earlier recommendation. More context did not help. What would have helped was context assembled by a system that understood which statement still governed. Retrieval that understands supersession, recency, and ownership is architecture. A bigger window that simply holds both the stale and the current claim is not.

## Everything-in-Context Has a Cost

Dumping everything into the window is not free, even when it fits and the bill is affordable.

There is the well-known problem of attention spread thin, where the one decisive sentence competes with thousands of irrelevant ones and sometimes loses. There is staleness, where old context outranks new because there is simply more of it. There is leakage, where information that should have stayed on the far side of a seam ends up shaping a decision it was never supposed to touch. And there is the quiet erosion of reproducibility, because the input is no longer a defined contract but a snapshot of an accumulating pile.

There is also a harder wall than any of those, and it is easy to forget when you are used to enormous hosted windows. A lot of pOS runs on local models. The nuance role, the one asked to make the subtle semantic calls, is a 26-billion-parameter Gemma model with a real context ceiling of about eighty-four thousand tokens. That ceiling is not a suggestion. One long research turn on a precious-metals pack quietly grew its context, call after call, until a single request reached eighty-six thousand tokens against that eighty-four thousand limit. The model did not degrade gracefully or drop the least important half. It returned a hard error and the turn died. The window was never architecture; it was a finite resource, and the accumulation strategy walked straight off the end of it.

The reflex, when you hit that wall, is to cut. That has its own trap. I once capped how much room one reviewing worker had to work in, and set the cap low enough that the thinking-heavy agents starved, producing worse results than before. I reverted it the next day. The lesson was not that budgets are bad, because the evidence budget above is a budget and it earns its keep. The lesson was that a context budget is an architectural decision with real consequences on both sides, not a knob you turn blindly to make a number go down.

Most of these costs, though, do not announce themselves. The schema still validates, the request still succeeds, and most of the time the answer is fine. They show up as occasional, hard-to-reproduce wrongness, and sometimes as something subtler still. Under context pressure I have watched workers stop making progress and start repeating themselves, one research loop calling the same tool three dozen times in a row, a session rewriting the same plan again and again because it had lost track of what it already knew. That is the most expensive kind of failure a system can have, because you cannot point at the boundary that caused it. There is no boundary. That was the whole problem.

## Assembling Context in pOS

In practice this turns context assembly into a first-class, deterministic step that happens before inference, not a prompt someone hand-tuned once and forgot.

When a research worker needs to source candidates for a portfolio sleeve, it does not receive the whole portfolio. A deterministic port assembles its input first. In pOS that port is literally a function called `findContext`, and it reads exactly what the task depends on from the live stores: the sleeve's mandate, meaning its role, its constraints, its add and trim conditions, and its target allocation; the current construction, meaning which packs hold what; and the existing holdings for that sleeve. It reads those three things and stops. The worker gets a bounded, explainable input rather than a copy of everything the system knows.

The most useful part of that port, to me, is what it does when a piece of context is not there yet. At the time of writing, the market regime and the multi-horizon view are not wired into `findContext`; supplying them is still another subsystem's job. So the port does not improvise them. Those fields come back reading `not available`, and every store read is wrapped so that a gap degrades honestly. The field is simply absent, and the prompt says so, instead of the system inventing a plausible regime to fill the hole. An honest gap in the context is worth far more than a fabricated value, because a fabricated value looks exactly like a real one right up until it moves money.

The model then performs the judgment and returns a bounded result across the seam. Deterministic code takes over again to validate the result, check that the worker stayed within its authority, attach provenance and a timestamp, and decide whether the proposed change should be written to the store. In fact the found candidates are written straight into the store the committee reads from, so the durable consequence of the inference lives in the system the moment it is trusted, not in a buffer that is about to be discarded. The window held exactly what the port decided it should hold, and nothing else.

The difference between this and a giant prompt is not the model and not the window size. It is that a component I can inspect decided what the model saw, and another component I can inspect decided what the model was allowed to change. The context window is a place where that assembled input is briefly staged. It is not the thing that made any of the decisions.

## The Window Is a Resource, Not a Design

I have come to think of the context window the way I think of memory or bandwidth. It is a resource the architecture spends, not the architecture itself. A larger window is genuinely useful, in the same way that more memory is useful. It raises the ceiling on what a single inference can consider, which lets workers take on richer tasks and lets me worry less about squeezing inputs through a narrow opening.

But no one would confuse having more memory with having a data model. The capacity is not the design. What determines whether a system is durable is still the same set of decisions it always was: what persists, who owns it, what crosses each seam, and what each component is allowed to see and to change. A bigger window changes how comfortably those decisions can be implemented. It does not make them for you, and it does not excuse you from making them.

The trap is that capacity feels like progress. Each increase makes the undesigned version work a little better, which makes the designed version feel like unnecessary effort. Right up until the pile grows, or two facts collide, or someone asks why a decision was made, the window will happily stand in for the architecture you did not build.

## Context Windows Are Not Architecture

So the rule I keep returning to is simple. The size of the context window tells me how much a model can hold. It tells me nothing about whether my system knows what it remembers, who owns which concept, what each component may do, or why any particular decision was made.

Those questions are answered by stores, contracts, seams, and the deterministic code that decides what a model sees and what it is allowed to change. When those answers exist, a larger window is a gift, because it lets well-designed workers do more. When they do not exist, a larger window is an anesthetic. It removes the pain that would otherwise tell me the architecture is missing.

I would rather feel that pain early. It is the signal that I still have design left to do, and no window, however large, is going to do it for me.

The model can be given everything. The question worth asking is what the system decided it should see, and that decision is the architecture. The context window is only where the answer briefly sits.
