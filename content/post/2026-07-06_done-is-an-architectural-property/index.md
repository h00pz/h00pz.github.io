---
title: "\"Done\" Is an Architectural Property"
slug: done-is-an-architectural-property
date: 2026-07-06
draft: false
description: "A feature that works once isn't finished, especially with inference. Done means deterministic, observable, repeatable, honest, safe, and narrow, by design."
tags:
  - architecture
  - evals
  - observability
  - systems
categories:
  - AI Coding Scar Tissue
image: done-is-an-architectural-property.png
---

The most expensive phrase in software is "it works." I've said it about things that worked exactly once, in a demo, on the one input I happened to try, and then called them done and moved on, which is roughly the confidence of a magician's assistant who's seen the trick performed a single time and is now ready to saw someone in half. It worked. It might even work again. But "it produced the right answer once" and "it's finished" are different claims, and the gap between them is where most of my scar tissue comes from.

That gap gets wider the moment inference is involved. A deterministic function that returns the right value once will return it again for the same input, so "it works" is closer to "it's done." A model that returns the right answer once might return something subtly different next time, or the same thing for the wrong reason, or the right thing right up until an input arrives that it quietly fumbles. So with AI in the loop, "done" can't mean "I saw it work." It has to mean something you can actually stand behind, and that something turns out to be an architectural decision rather than a vibe.

This post is about treating done as a property you design in, with parts you can name. It's meant to replace the feeling you get when the demo goes well, which is the least reliable signal in the whole business and the one I trusted the longest.

## "It Worked" Is Not "It's Done"

Start with the trap, because it's seductive. A feature demos successfully, everyone nods, and it ships, and the reason this feels safe is that a successful demo is genuine evidence. It really did work, once, in front of people. The problem is that a single success is evidence of capability, not of completeness, and those get conflated constantly because a demo is the most emotionally convincing form of evidence there is and also one of the weakest.

What a demo doesn't show you is what happens on the second input, or the malformed one, or the one where the upstream data is stale, or the one where the model is having an off day. It doesn't show you whether the thing can be understood after it runs, whether it fails safely, or whether it quietly did the right thing for a reason that won't hold next week. None of that is visible in the moment of success, which is exactly why the moment of success is such a bad place to decide you're done.

## Two Kinds of Done

The framework I build against forces a distinction here that I now consider one of its most useful, and it's simple: workflow termination and product completion are not the same thing, and a specification has to say which is which.

Workflow termination is the mechanical question. The job finished, the queue emptied, the retry cap was reached, the worker stopped, the operator canceled. Any of those ends the workflow, and a system that treats termination as done will happily report success the moment the process exits, regardless of whether anything useful happened.

Product completion is the real question, and it has an entirely different checklist. The required information exists or is honestly unavailable. The canonical state is coherent. The current state is visible, the history is preserved, and the operator can actually understand the result. Downstream routing is complete, and no unresolved contradiction is left hidden. The sharp line the framework draws is this: a workflow may terminate while the product outcome remains incomplete, so the spec has to state, explicitly, what each one means, because a background job that exits cleanly while producing nothing honest is the single most common way a system lies to you about being done.

## Done Has to Be Provable

Once you separate those, done stops being something you assert and becomes something you prove. The mechanism that enforces this lives in [the post on the failure ledger](/p/the-failure-manifest-log/), where a feature isn't allowed to call itself live until its acceptance has been demonstrated against the running system, with the command and its output recorded, because a green test suite that shares the code's assumptions is checking that I wrote what I wrote, not that the system does what it claims. What I want to add here is narrower: proof is a property of done, not a separate bureaucracy bolted on after. A result that can't be proven against reality isn't a smaller kind of finished. It's hopeful.

A feature that's built and merged but never proven against the running system stays in an honest "built" state and refuses to promote itself to done. That refusal is the whole point. It would be easy and comforting to let a passing test flip something to done, and it would also be a small manufactured completeness, which the framework treats as worse than an honest gap. The system would rather admit a thing is built but unproven than claim a doneness nobody actually witnessed.

## The Properties of Done

When you make done explicit, it turns out to have parts, and naming them is what lets you check for each one instead of squinting at a demo. Done is deterministic where it should be, so the parts that don't need inference behave the same way every time. It's observable, so you can see not just that it ran but what it received and what it concluded. It's repeatable, so a second run against the same state is safe rather than a fresh roll of the dice.

It's also honest, and this one is easy to miss. A feature that correctly reports "not available" is complete, while a feature that fills the gap with a confident guess is not, even though the second one demos better. Done is safe, meaning the failure modes are contained and no forbidden outcome is reachable, and each of those forbidden outcomes is specific enough to have a test that fires if the system ever produces it. And done is narrow, meaning the thing does its bounded job and doesn't quietly take on responsibilities nobody scoped. Miss any of those and you don't have a smaller version of done. You have something that looks done and isn't, which is worse, because it stops anyone from looking closer.

## Done You Can Check

The payoff of making done this explicit is that the system can start checking its own doneness instead of relying on me to remember. I described the concrete instrument [earlier in this series](/p/architecture-after-agents/): the pOS test whose only job is to reconcile the architecture with the code, failing if an endpoint is mounted that nobody declared or specified-and-built but wired to nothing, and proving it can catch both by injecting each failure. That test is this whole idea made mechanical, doneness the running system asserts about itself continuously rather than a thing I remember to check.

That's done as an architectural property in its purest form. It isn't a feeling anyone has about the code, and it isn't a demo anyone remembers going well. It's a specific, named, verifiable set of conditions that the running system continuously asserts about itself, and when one of them stops being true, something goes red. The reason I care about defining done this carefully is that the alternative is the version I started with, where done meant "it worked when I tried it," and the whole of this series is a record of what that phrase costs. A result produced once is a promising start. Done is when the system can prove, deterministically and against reality, that the result will keep being right, keep being honest about what it doesn't know, and keep failing safely when it fails. That isn't a feeling. It's a decision you write into the architecture, on purpose, before you're allowed to believe the demo.
