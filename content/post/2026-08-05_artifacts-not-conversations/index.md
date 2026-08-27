---
title: "Artifacts, Not Conversations: How Agents Should Collaborate"
slug: artifacts-not-conversations
date: 2026-08-05
draft: false
description: "Multi-agent systems drift when agents pass natural-language conversations back and forth. They should collaborate through typed artifacts with defined producers, consumers, schemas, and ownership."
tags:
  - ai
  - architecture
  - agents
  - seams
  - systems
categories:
  - Small Model Systems
image: cover.png
---

The most natural way to make two agents work together is to let them talk. One agent does some research and describes what it found. Another agent reads that description, does its own work, and describes what it concluded. A third agent reads both. Everyone is exchanging fluent, reasonable-sounding messages, and the whole thing looks like a team.

It also drifts, and it drifts in a way that is almost impossible to see while it is happening. The research agent says a company has "meaningful exposure" to something. The next agent interprets "meaningful" its own way. A third agent, reading a summary of a summary, treats a tentative observation as an established fact. No message was wrong, exactly. Each one was a plausible reading of the last. But by the end of the chain, the system is confidently acting on something nobody actually established, and there is no single place you can point to where the meaning changed.

I have come to think this is the central mistake in a lot of multi-agent design. The agents are collaborating through conversation, and conversation is the wrong medium for anything a system needs to depend on. What agents should exchange is not messages. It is artifacts.

## The Conversation Trap

A conversation between agents feels like collaboration because it looks like how people collaborate. But when people collaborate well on something that matters, they do not actually rely on the conversation. They rely on the document the conversation produced, the ticket, the signed contract, the schema, the commit. The talking is how they get to the artifact. The artifact is what they depend on.

Agent-to-agent conversation skips the artifact and keeps only the talking. That inherits every weakness natural language has as an interface. There is no schema, so nothing can be validated. There is no owner, so no one is responsible for what a term means. There is no provenance, so a claim cannot be traced back to its source. And there is no stable identity, so the same finding expressed twice becomes two findings, while two different findings expressed similarly blur into one.

None of these matter in a demo, because a short chain of capable models will paper over all of them. They matter enormously the moment the system is large enough that no single model sees the whole chain. That is exactly when the drift becomes invisible, because there is no longer anyone, human or model, holding the entire conversation in view.

## An Artifact Has a Producer and a Consumer

An artifact is the opposite of a message. It is a typed object with a defined shape, produced by exactly one component that owns its meaning, and consumed by others that agree to read it as it is rather than reinterpret it.

That definition is doing a lot of work, so it is worth pulling apart. Typed means there is a schema, and the schema can be validated before anything downstream trusts it. Defined shape means a consumer knows precisely what fields exist and what they mean. One producer that owns its meaning means there is a single authority for what the artifact says, so the definition cannot fork. Consumed as it is means the consumer's job is to use the artifact, not to re-derive it, argue with it in prose, or quietly extend it.

This is the same idea as the seam from earlier in this series, applied to the specific problem of agents working together. When two agents collaborate through an artifact, the artifact is the seam between them. Everything good about seams, replaceable implementations, contained uncertainty, explicit ownership, follows directly. Everything bad about conversation, drift, leakage, lost provenance, is what you were trying to escape.

## How Agents Actually Hand Off in pOS

This is concrete in pOS, and the concreteness is the point. When Hunt, the discovery subsystem, finishes researching a pack, it does not narrate its conclusions to the Committee that decides what to act on. It produces Findings.

A Finding is a typed artifact. It carries a finding identifier, the subject and pack it belongs to, the ticker, the thesis, and a fit assessment. When Hunt completes an agentic find, the flow is explicit and mechanical: it runs the research, turns the result into Findings, persists those Findings in its own candidate store, and then emits each one to the Committee through an injected port. The Committee reads Findings from a store. It never reads Hunt's conversation, because there is no conversation to read.

Two properties of that handoff matter more than they might appear. First, Hunt holds no handle to the Committee's store, or to Portfolio Construction's, or to the Brain's. Every cross-subsystem interaction flows through a narrow injected port, `findContext` on the way in and `emitToCommittee` on the way out. Hunt cannot reach into another subsystem and cannot be reached into. The only thing that crosses the boundary is the artifact. Second, that same store is written by Hunt through one door and read by the Committee through another, one store, two doors, so the Finding is a durable object with a single definition, not a message in flight that each side remembers differently.

## The Artifact Is Durable Before the Handoff Happens

There is a detail in that flow that took me a while to appreciate. The hand-off to the Committee is fire-and-forget. If the emit fails, the find does not fail, because the Finding has already been persisted as a stored artifact in Hunt's own store before the hand-off is even attempted.

Compare that with a conversation. If one agent tells another something and the message is lost, the thought is gone; the only copy was in flight. A conversational architecture makes the transient act of communication load-bearing, which means every dropped message is potentially lost work.

An artifact architecture inverts that. The durable object exists first, independently of whether anyone has been notified about it yet. Notification becomes a convenience rather than a lifeline. The Committee can be told a Finding exists, or it can discover the Finding by reading the store later; either way the Finding is safe. Collaboration stops depending on the reliability of a message and starts depending on the durability of an object, which is a much better thing to depend on.

## Schemas Turn Retries Into No-Ops

The typed nature of an artifact buys something that conversation can never offer: a stable identity, which makes the whole system safe to retry.

Because a Finding, or a queued proxy, or a demand, is a defined projection of some underlying belief, the system can make its serialized form deterministic. The same belief produces byte-identical bytes. That sounds like a small implementation nicety and is actually a large architectural property, because it means a retried hand-off collapses onto the existing record instead of creating a duplicate. Emit the same Finding twice and the second one lands on the first. In pOS this shows up all over: a trade replayed with a corrected annotation is a no-op because the idempotency fingerprint ignores the annotation, and a demand re-emitted after a failure produces the identical payload and merges.

Now imagine trying to make a conversation idempotent. You cannot. Replaying a conversation produces a new conversation. There is no identity to collapse onto, because a message is an event, not an object. The moment your agents need to retry, and in any real system they will, the difference between an artifact and a message stops being philosophical and becomes the difference between a system that self-heals and one that quietly duplicates its own work.

## Ownership Is What Actually Stops the Drift

The deepest reason to prefer artifacts is ownership. Every artifact has exactly one producer that owns what it means, and that single fact is what kills the drift I described at the start.

When the Brain owns the market regime and publishes it as an artifact, no other subsystem gets to decide what the regime means. Hunt can read it, weight it, or ignore it, but Hunt cannot redefine it, because Hunt did not produce it. The definition lives in one place. In a conversation, the definition lives nowhere and everywhere at once: each agent holds its own interpretation, and those interpretations drift apart precisely because no one owns the canonical version.

This is why I think of artifact-based collaboration as governance rather than plumbing. Deciding who owns each artifact is deciding where meaning is allowed to be defined in the system. Once that is explicit, an agent reinterpreting another agent's output is not a subtle semantic bug that surfaces three hand-offs later. It is a boundary violation you can see, because the consumer tried to do something only the producer is allowed to do.

## What Conversations Are Still Good For

None of this means language is banned. It means language is not the contract. A model still reasons in natural language internally, and the boundary between a system and its human operators is genuinely conversational, because that is the interface humans want. Open-ended exploration, brainstorming, and ambiguous back-and-forth are exactly what language is good at.

The rule is narrower than "no conversation." It is that nothing a system depends on should live only in a conversation. The moment an exchange between agents carries a decision, a fact, or a piece of state that another component will act on, that exchange needs to become an artifact with a schema, an owner, and an identity. Let the models talk while they work. Just make sure that what they hand each other is an object, not a paraphrase.

## The Failure Mode Underneath All of This

I have watched the conversational version fail from the inside, in the system I use to build pOS itself. When I run several coding agents at once and let them share a working tree, they collide. One agent's leftover files get picked up by another's test run and produce dozens of failures that have nothing to do with the code. The same task, launched twice after a context reset, spawns two agents racing in the same space, each half-aware of the other. The shared mutable medium was the problem, and the fix was isolation: give each agent its own worktree and let them integrate through committed artifacts rather than through a space they all reach into at once.

That is the same lesson at a different altitude. Whether the agents are writing code or researching investments, collaboration through a shared, unstructured, mutable medium drifts and collides. Collaboration through owned, typed, durable artifacts does not. The medium is the architecture.

## Artifacts, Not Conversations

So when I design a multi-agent system now, I do not ask how the agents will talk to each other. I ask what each agent produces, who owns it, what shape it has, and who is allowed to consume it. The answers to those questions are the real architecture. The messages the models exchange along the way are just how they get there.

A conversation between agents feels like collaboration and quietly erodes into a game of telephone. A set of typed artifacts with clear producers and consumers feels more rigid and is actually what keeps a large system coherent. Agents should not hand each other paraphrases of what they think is true. They should hand each other objects that say exactly what is true, who said it, and when.

Not conversations. Artifacts.
