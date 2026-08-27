---
title: "Introducing HASF: Specifying a System Before You Build It"
slug: introducing-hasf
date: 2026-05-27
draft: false
description: "The h00pz Architecture Specification Framework is a way of deciding a system's boundaries, ownership, and failure states on purpose, before features accumulate into an accidental architecture."
tags:
  - ai
  - architecture
  - hasf
  - systems
  - pos
categories:
  - AI Scar Tissue
image: cover.png
---

The previous post ended with a system I threw away and two things that replaced it. This is the first of those two: the framework. I've been referring to it obliquely since the very first post, promising it was a subject for another day. This is that day.

It's called HASF, the h00pz Architecture Specification Framework, and the plainest way to describe it is this: it is a way of deciding what a system is before you build it, so that its boundaries, its ownership, and its failure states are chosen on purpose rather than discovered at runtime. PortfolioOS v2 was discovered at runtime. HASF exists so that never has to happen again.

I want to be careful about what this post is. HASF is a large document, and this isn't a tour of it. It's an argument for why it exists and the handful of ideas that do most of the work. The mechanics (the failure ledger, the desired-versus-as-built split, cross-reading, spec-before-code, and the definition of done) each get their own post later in this series. Here I only want to convince you that specifying a system first is a real discipline with real rules, not a synonym for drawing a diagram before you code. Where the document's own words land harder than my summary of them, I will quote them directly.

## Most Frameworks Describe Systems That Already Make Sense

Most architecture frameworks are good at describing a system after its architecture is already understood. They give you components, containers, deployment views, runtime interactions, interfaces, technology choices. All of that is necessary, and none of it catches the failures that actually hurt in an AI system, because those failures aren't about whether services can talk to each other.

The failures that hurt are semantic and operational. The system answers the wrong question correctly. A model's interpretation quietly becomes more authoritative than the source it came from. Current state and historical state get mixed until nobody can say what is true now. Two stores each look canonical. A retry duplicates work. The interface shows a conclusion that was superseded an hour ago. An operator can't tell why a result exists. A background job finishes without producing an honest outcome. A system fabricates confidence, or freshness, or completeness, and nothing catches it because everything it did was locally valid.

The framework opens with a long catalogue of exactly these failures, stated plainly. A sample of it reads:

> - the system answers the wrong question correctly;
> - a model-generated interpretation becomes more authoritative than the source;
> - current state and historical state are mixed;
> - two data stores each appear canonical;
> - a retry creates duplicate derived work;
> - the UI presents a stale or superseded conclusion;
> - an operator cannot tell why a result exists;
> - a background workflow terminates without producing an honest product outcome;
> - a system silently fabricates confidence, freshness, completeness, or certainty.

That list isn't hypothetical. It's close to a catalogue of what went wrong in v2, and a box-and-arrow diagram would have shown none of it, because every box was fine. The framework exists to prevent exactly these, and preventing them requires deciding things that a component diagram never asks you to decide.

## Start From the Operator, Not the Database

The first rule is about where you begin. HASF starts every substantial piece of work with one question: what must the operator be able to understand, decide, or accomplish? Not which database, not which model, not which framework. What decision is this system responsible for.

This sounds obvious and is routinely skipped, because the technical questions are more fun and feel more like progress. But architecture exists to serve an operator outcome, and if you can't state that outcome precisely, every downstream choice is unanchored. The governing sequence HASF insists on runs operator outcome, then canonical semantics, then workflow and information flow, then the operator's surfaces, then system architecture, then implementation, then acceptance. The usual order (services, then schemas, then APIs, then UI later) is that sequence run backwards, and running it backwards is how you end up with a system that works and answers the wrong question.

The document draws the order it wants, and directly beneath it the order it refuses. The whole inversion fits in two small diagrams:

```text
Operator outcome
    ↓
Canonical semantics
    ↓
Workflow and information flow
    ↓
Operator surfaces
    ↓
System architecture
    ↓
Implementation slices
    ↓
Acceptance
```

That's the order the framework insists on. Here's the one it rejects, and the contrast is the entire argument:

```text
Services
    ↓
Schemas
    ↓
APIs
    ↓
UI later
```

## Semantics Before Machinery

The second rule is the one I underrate most often. A deterministic implementation of an ambiguous concept is still wrong. Before you define services or schemas or queues or prompts, you have to define what the result actually means: which question it answers, which facts support it, which facts don't, how uncertainty is represented, which state is current and which is historical, and what is allowed to happen next.

The v2 monitoring failure was, underneath, a semantics failure. Nobody had pinned down what it meant for a position to be "monitored against its thesis," so nothing owned making it true, so the field sat null while every mechanical part reported success. You can't build your way out of an undefined concept. You can only build a very efficient, very well-tested implementation of the confusion.

## One Canonical Truth Per Concern

The third rule is a direct answer to the two-stores-each-look-canonical failure. Every mutable concern must have exactly one declared canonical owner: one current revision, one write store, one identity record, and one lifecycle state. Other stores are allowed to exist, but only as projections, indexes, caches, read models, or history. They must never quietly become competing truth.

This is the rule that keeps a system from developing two hearts. The moment two components both believe they own the meaning of the same thing, they will drift, silently, while continuing to exchange perfectly valid data, the exact failure I wrote about several posts ago. HASF makes ownership a thing you declare in writing, per concern, up front, so that drift becomes a boundary violation you can see rather than a mystery you debug six months later.

## Honest Incompleteness Beats Fabricated Completeness

The fourth rule is almost a moral stance, and it is one of my favorite things about the framework. Faced with a gap, HASF prefers the honest word (unknown, incomplete, unavailable, stale, unresolved, exhausted, or unsupported) over the comfortable lie: a guessed value, a silent default, a false certainty, an invented relationship, a synthetic completeness, or a misleading success state.

The document doesn't leave this to interpretation. It writes the preference out as two facing lists:

> Prefers: unknown, incomplete, unavailable, stale, unresolved, exhausted, unsupported.
>
> Over: guessed values, silent defaults, false certainty, invented relationships, synthetic completeness, misleading success states.

This matters more with inference than anywhere else, because a model will happily manufacture a plausible answer to fill any hole you leave open, and a plausible fabricated answer is indistinguishable from a real one until it moves money. A system built on this rule says "not available" and means it. A field that has no honest value stays empty and says so. That single preference, that a visible gap is worth more than an invisible guess, removes an entire category of the failures the framework was built to prevent.

## KISS Is a Constraint, Not a Slogan

The last rule I will pull out here is the one that keeps the framework from becoming the thing it replaced. HASF is comprehensive in what it asks you to decide and deliberately minimal in what it asks you to build. One state machine. One canonical read model. One authority ladder. One bounded retry. One honest unavailable state. It explicitly warns against duplicate concepts, generalized platforms built before there's a need, arbitrary configurability, and architecture that exists only to compensate for semantics nobody bothered to define.

That last phrase is v2's epitaph. A great deal of what I threw away was architecture that existed only to compensate for unclear meaning. HASF treats simplicity as a governing constraint precisely so that the framework for avoiding accidental complexity doesn't itself become a generator of it. Comprehensive about the thinking; ruthless about the building.

## Rules Govern Behavior, Repository Artifacts Govern Truth

There's one more idea worth stating, because it is what makes the whole thing survive contact with AI coding agents. HASF separates how work is performed from what the project says is true. The operating instructions an agent follows stay short, stable, and behavioral. The truth of the system (its architecture, its decisions, its state, and its history) lives in canonical, versioned, and linked artifacts in the repository, not in a prompt and not in a conversation.

The framework compresses this whole idea into a single governing line. It's the sentence I come back to most:

> Rules govern behavior. Repository artifacts govern truth.

An implementation agent shouldn't need a forty-page prompt stuffed with copied architecture, component inventories, and current state, because all of that goes stale the moment it is copied. The rules stay small and enforceable; the repository carries the complexity. When a rule file and a canonical artifact disagree about what is true, the canonical owner wins and the stale assertion gets corrected in the same change. This is the same principle as keeping state out of the model, applied to the project's own knowledge: the truth lives in something owned, versioned, and queryable, never in something remembered.

## What the Framework Buys

None of these rules is exotic. Operator-first, semantics before machinery, one owner per concern, honesty over fabrication, simplicity as a constraint, truth in the repository. What makes HASF a framework rather than a list of good intentions is that it forces you to answer each of them, in writing, in a fixed order, before implementation begins, and it defines what a complete answer looks like for each one.

That forcing is the whole value. Left to my own enthusiasm, I will start from the model, define the machinery, discover the semantics at runtime, let ownership emerge by accident, fabricate the missing pieces, and add complexity to paper over the confusion. That path has a name now. It was called v2.

The next post is the other half of the answer: not the framework, but the lived process of using it, the actual week of building a subsystem this way, including every place the process broke. HASF is what I decided the rules should be. The method is what it felt like to follow them.
