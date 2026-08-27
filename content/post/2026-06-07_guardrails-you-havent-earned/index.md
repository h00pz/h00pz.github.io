---
title: "Stop Writing AI Guardrails You Haven't Earned"
slug: guardrails-you-havent-earned
date: 2026-06-07
draft: false
description: "Durable guardrails trace back to concrete failure modes. Speculative governance eventually creates complexity without any matching increase in safety."
tags:
  - ai
  - architecture
  - systems
  - hasf
categories:
  - AI Scar Tissue
image: cover.png
---

There's a reflex that feels like responsibility, and it is one of the fastest ways I know to rebuild the system I just threw away. Something could go wrong with an AI component, so you add a rule to prevent it. Then you imagine another thing that could go wrong, and you add another rule. Each addition is individually defensible, and every one of them makes you feel like a careful engineer who is taking the risks seriously.

The previous post in this series described what that habit did to PortfolioOS v2. The safeguards accumulated faster than I could understand them, and eventually the defenses were harder to work through than the failures they were meant to prevent. What I left out is that most of those safeguards were never earned. They guarded against things I had imagined, not things that had happened, and an imagined failure produces a real constraint that a real reader then has to live with forever.

This post is about the difference between a guardrail you earned and one you merely felt. It's also about why the second kind is more dangerous than no guardrail at all.

## The Guardrail Reflex

The reflex is easy to understand because the incentives all point the same way. Nobody is ever blamed for a failure they prevented, so adding a rule feels free, while removing one feels reckless. The result is a ratchet: constraints only ever accumulate, because each one arrives with a plausible story about the catastrophe it averts and none of them ever come with an expiry date.

In an AI system the reflex is even stronger, because models genuinely can fail in strange and surprising ways. You can always imagine a new one. The model might fabricate a number, so add a validation layer. It might act on stale data, so add a freshness gate. It might do something with a tool that you didn't anticipate, so wrap the tool in a policy. None of those instincts is wrong on its face, and that is exactly the problem, because "not wrong on its face" is true of an unlimited number of possible rules.

At some point the sum of individually reasonable constraints becomes a system that no single person can hold in their head, and complexity is itself a source of failure. You didn't trade complexity for safety. You bought complexity and told yourself it was safety.

## An Earned Guardrail Has an Incident Behind It

The discipline that pulled me out of this is simple to state and surprisingly hard to follow. A guardrail earns its place when it traces back to a specific failure that actually occurred, and it doesn't earn its place otherwise. The test isn't whether the failure is plausible. The test is whether it happened, to this system, in a way someone can describe.

When I rebuilt the architecture, the strongest documents anchored each of their central rules on a real incident, named concretely. The Brain subsystem's document doesn't say "monitoring is important." It says that in v2 the thesis pipeline produced genuine work and the monitoring state was null on all fifty-six positions, and then it derives the rule from that wreck. The market intelligence document is anchored on semiconductors, a specific batch of expired puts, and stale cron jobs, not on the abstract idea that stale data is bad. An abstract failure mode constrains nobody, because it can be satisfied a hundred ways and argued away in any of them. A named one constrains the design, because everyone can see the exact hole it is covering.

This changes what a guardrail is. It stops being a fence you put up because the drop looks dangerous, and it becomes a patch over a place where someone actually fell.

## Architecture Is Not the Same as Worry

There's a failure mode that lives right next to the guardrail reflex, and I've watched my session walk straight into it during an architecture pass. Asked to write down where the system's data came from, it started generating concerns about paid-subscription licensing that nobody had raised and that had nothing to do with the architecture. My response, with the profanity removed, was clean and correct: this is architecture, not solution design.

The lesson took me a while to absorb. Architecture defines what a system is, and raising a risk early doesn't make that risk handled. It just makes the document longer and the end state harder to see. "We will consume paid sources" is an architectural fact. "How we will handle the licensing" is an implementation concern, and dragging it into the architecture pass doesn't protect anyone. It buries the shape of the system under a pile of anticipatory worry, which is precisely the sediment that made v2 unreadable.

The tell for this one is worth memorizing, because it is subtle. You are writing about how something will be dealt with rather than what it is, and the words "we should probably make sure that" are usually the first sign.

## A Guardrail Can Guard the Wrong Thing

Not every unearned guardrail is pure speculation. Some have a real motivation and are still wrong, because they were aimed at the wrong mechanism, and those are the most convincing ones of all. The clearest example I've hit recently was a token cap.

The workers in pOS share a single large local model slot, and I didn't want any one of them to monopolize it, so I capped the number of tokens each call was allowed to use. The cap was deliberate, commented, and justified in the manifest as exactly what it was, a bound to stop one worker from eating the whole slot. It looked like responsible engineering, and it promptly broke everything. Every research sleeve began failing with the same error, the model returning neither an answer nor a tool call, across every pack and every sleeve combination.

The reason was that the cap covered the model's thinking tokens and its output tokens in one shared budget. In thinking mode the reasoning consumed almost the entire allowance, which left too few tokens for the actual response, so the guardrail I had added to protect the slot was quietly starving the output of every worker that used it. The failures that looked like the model being bad at nuance were the cap strangling it, and I reverted the whole thing the next day.

The real lesson wasn't that the cap value was set too low. It was that the failure I was guarding against, one worker monopolizing the slot, is a concurrency problem, and the honest fix was to let the slot serve more than one request at a time rather than to squeeze what each request was allowed to produce. I had reached for the guardrail that was easy to add instead of the one that matched the actual failure, and an unearned guardrail aimed at the wrong mechanism does more than fail to help. It manufactures the very symptom it appears to prevent.

## Forbidden Outcomes: Guardrails That Come With Fixtures

The framework I now build against has a specific answer to all of this, and it is my favorite section in the whole document. Every specification is required to declare its Forbidden Outcomes, and each forbidden outcome is a concrete, named pairing of a situation and the wrong thing that must never follow from it. They read like this:

```text
Projection stale
+ displayed as current

Operator correction exists
+ reprocessing removes it

Same retry
+ duplicate canonical task

Missing source
+ model fabricates a fact

Live-required question
+ memory-only answer
```

The important line is the requirement that follows the list: each forbidden outcome should have a deterministic fixture. That single rule is what separates an earned guardrail from a felt one. A forbidden outcome isn't a vague intention to be careful. It's a specific bad result, specific enough that you can write a test that fails if the system ever produces it. If you can't write that test, the guardrail isn't real yet, and the discipline of having to write it forces the failure to be concrete before the constraint exists.

This is the inversion that matters. A speculative rule says "the model might do something bad, so here is a policy." A forbidden outcome says "here is the exact bad result, here is the fixture that catches it, and here is the situation that produces it." One is worry expressed as architecture. The other is a failure expressed as a test.

There's a second half to this, because a fixture is only worth something if it actually catches the failure it claims to. The way I check is to break the guard on purpose and watch what happens. In one part of pOS, two guards protect how capital plans are set: the rule that never having had a plan is a different state from having an old one, and the rule that a risk limit is a bound rather than a preference. To confirm they were load-bearing, I injected each failure directly, replacing the first guard with an invented default plan and disabling the second with a hard-coded false. The invented default turned three tests red, the disabled limit turned one red, and each red test named the exact thing the guard existed to prevent. That's the difference between an earned guard and a hopeful one. A guard whose removal breaks a specific, named test is protecting something real, and a guard whose removal breaks nothing was never protecting anything at all.

## The Rule Has to Carry Its Reason

Even an earned guardrail rots if you record the rule and forget the incident. This is the thing that killed v2 more than any single bad decision. Rules were added in response to real events, the events faded, and what remained was a constraint nobody could explain, which then got deleted the first time it was inconvenient or quietly routed around by the next person who couldn't see why it was there.

So the architecture documents carry their doctrines as two-part entries, and the second part isn't optional. Each doctrine is one line of rule and one line of reason. "Collection owns the only egress" is the rule, and "one untrusted-input boundary to harden, monitor, and fail visibly, rather than two" is the reason. A rule with its reason attached doesn't get deleted when it becomes inconvenient. It gets argued, on the merits, against the specific failure it was built to prevent, and argument is exactly the outcome you want, because sometimes the failure no longer matters and the rule really should go.

A guardrail without its reason is a superstition. A guardrail with its reason is a decision you can revisit, and the difference between those two is the difference between a system you can maintain and one you can only accrete.

## Restraint Is Part of the Design

The framework builds restraint into the process in two more places, and both are really guardrails against the guardrail reflex itself. The first is a required Non-Goals section, an explicit statement of what won't be built, which exists specifically to prevent the drift where a system slowly grows to cover every risk anyone ever imagined. The second is a Stop Rule, a defined condition that ends a slice of work, and it comes with a striking constraint: the stop rule must not require a positive or exciting outcome. You are done when the declared thing works honestly and no known failure lacks a disposition, not when you have finished adding every safeguard you can dream up.

Both of these treat "adding more" as the default failure rather than the default virtue. That's the opposite of the guardrail reflex, and it is deliberate. The framework assumes that a competent, worried engineer will always be able to justify one more constraint, so it makes stopping an explicit, defined act rather than something you back into once you run out of fears.

## What a Speculative Rule Actually Costs

It's worth being precise about the cost, because the guardrail reflex survives on the belief that its rules are close to free. They aren't. Every constraint you add is something the next person has to understand before they can safely change the system, and something the model has to satisfy on every call whether or not the guarded failure was ever possible in that path. A speculative rule spends real complexity to buy protection against a failure that may not exist, and complexity, unlike the imagined failure, is guaranteed to be there.

The deeper cost is that speculative rules crowd out earned ones. When half your constraints guard against things that never happened, nobody can tell which of them are load-bearing, so all of them get treated as equally negotiable or equally sacred, and both of those are wrong. A system where every guardrail traces to a real incident is a system where you can reason about your own defenses. A system where guardrails are a sediment of past anxieties is one where you can only add more.

So the rule I hold myself to now is narrow and a little uncomfortable. Don't write the guardrail until the failure is real, name the incident when you do, keep the reason attached to the rule, and make the bad outcome concrete enough to test. Earn it, or don't build it. The alternative is a system that feels safe right up until it is impossible to change, which, as it happens, is exactly where this series began.
