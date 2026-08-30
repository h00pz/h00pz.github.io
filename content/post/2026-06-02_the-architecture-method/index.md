---
title: "The Architecture Method: Argue First, Write Second"
slug: the-architecture-method
date: 2026-06-02
draft: false
description: "HASF is the rules for specifying a system first. This is what following them felt like: a week building a subsystem, including every way I got it wrong."
tags:
  - ai
  - architecture
  - hasf
  - seams
  - systems
categories:
  - The Agentic SDLC
image: cover.png
---

[The previous post](/p/introducing-hasf/) was the framework, the rules for deciding a system before you build it. This one is the other half, and it is the half you can't get from a document. It's what following those rules actually feels like, reconstructed from about a week of work that produced the v3 architecture: ten subsystems, their seams, and the shared API and persistence contracts. I had it written down for the same reason the framework exists at all: the process was the valuable thing, and processes evaporate.

I'm going to include the parts that went wrong. That isn't modesty. The failure modes are the most useful thing in the method, because each one comes with a tell, a recognizable moment where you can catch it before it costs a day. If you only take one thing from this post, take the tells.

## Two Loops, Nested

The whole method is two loops, one inside the other. The outer loop is a conversation:

```text
operator says something short
        ↓
session works out what it means everywhere: every lane, every seam, and every layer
        ↓
session argues it back, with the consequences named
        ↓
operator corrects, confirms, or kills it
        ↓
only then does anyone write a document
```

Underneath the conversation runs a second loop. It isn't a discussion but a fixed order:

```text
architecture  →  seams  →  API  →  store  →  workers
```

The outer loop is a conversation and the inner loop is a sequence. Almost everything in this post is a consequence of getting one of the two wrong at some point during the week.

## The Order Is the Discipline

The inner loop isn't a suggestion, because each step is derived from the one before it. Architecture asks what a subsystem is for and what it owns. Seams ask what crosses its boundary and in which direction, derived from what it owns. The API asks which endpoints those crossings require, derived from the seams. The store asks what shape the API must persist, derived from the API. The workers ask who claims what and when, derived from the store and the seams.

Skip a step and the gap fills itself with something worse. A worker designed before its seams are known invents its own integration, because it needs data from somewhere and no crossing has been declared, so it reaches for a database or another subsystem's internals. That integration is now real, undocumented, and load-bearing. Do that ten times and you have the previous version of the system: modules with no seams, because the integration was implicit and nothing forced anyone to state it. The order is the discipline precisely because each step, done in sequence, forces you to declare the thing the next step would otherwise invent in the dark.

And architecture has to be settled before any of the four begins. Twice that week the session started drafting a seam register while the subsystem's purpose was still moving, and both times the register had to be thrown away, not edited but thrown away, because the seams change when the ownership changes. The four layers describe how you reach an end state. They are meaningless against a target that is still being argued.

## Argue First, Write Second

This is the largest lesson of the week and it cost the most to learn. Writing is a commitment device. Once a paragraph exists, everything after it defends it. So the argument has to happen before the file opens, in conversation, out loud, with the consequences named.

The failure case: my session wrote a subsystem's seam document straight from its architecture document, without reading the two demand documents sitting a few directories away. What it produced invented a brand-new endpoint to solve a problem another document had already solved, and in doing so quietly broke the subsystem's central rule. I stopped the work cold: don't edit anything, tell me exactly what you changed, reverse all of it, read everything, and only then write the document. Not edit, but revert. A document built on a wrong premise repairs worse than it rewrites.

The success case, the same week, went the opposite way. Before the collection subsystem's document existed, there was an hour of pure conversation with no file open. It was an argument about where a contested responsibility should land, about which of two subsystems should own gathering data. That hour produced the boundary test that settled it. The document that followed took one pass and needed four small corrections, none of them structural. Arguing costs an hour. Unwriting a wrong seam register costs a day and leaves residue in four other documents that referenced it.

The rule that came out of it is short and unforgiving. If you can't state a subsystem's boundary in one sentence, and defend it against the hardest counter-example you can think of, you aren't ready to open the file.

## What a Finished Lane Document Looks Like

All of that arguing produces a specific kind of document, and once you have written a few they all have the same bones. Here is a trimmed piece of a real one, the collection lane, so the shape is visible rather than described:

```text
# Subsystem Architecture — pos-collection

The lane that gathers. It measures and preserves what the system has said it
depends on, and it says loudly when it cannot.

> This document describes the DESIRED END STATE, never the current one.

## Doctrines (the rule, and why it exists)
| doctrine                                | why it exists                                          |
|-----------------------------------------|--------------------------------------------------------|
| Collection owns the only egress         | one hardened boundary is worth more than two           |
| An absence is an observation            | otherwise checked and never-checked are one record     |
| Cite or reject                          | an ungrounded answer that looks grounded is worse than none |
| Preserve before interpreting            | a conclusion whose source has changed can't be examined|
| Store what was known when it was known  | revisions make a naive backtest lie                    |

## Degradation (what happens when each dependency is gone)
| absent            | collection behaviour                                        |
|-------------------|-------------------------------------------------------------|
| a source          | it goes stale against its contract and says so. No          |
|                   | substitute is ever silently used.                           |
| the ibeam gateway | price and FX gathering stops. There is no second source.    |
| model-serving     | agentic gathering and classification queue. Everything      |
|                   | deterministic is unaffected.                                |

The rule is uniform, and it comes from one failure: a missing record announces
itself and a stale one does not.
```

Two things in there do most of the work. Every doctrine carries its reason in the next column, which is the whole point, because a rule you can see the reason for is a rule you can argue with instead of one you either worship or delete. And the degradation table isn't decoration; the act of filling it in is what forces you to admit which dependencies you actually have, and three times that week a row I couldn't fill was a seam I had forgotten to declare.

That's a trimmed piece, cut down to fit here. The complete document, all fifteen sections of it, lives as a plain file in this site's repo, so you can see what a finished one actually weighs and how much of it turns out to be doctrine with its reason attached: <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/pos-collection-architecture.md" target="_blank" rel="noopener">Subsystem Architecture: pos-collection</a>.

## Read Everything, Then Cross-Read

After I stopped the work, my instruction was explicit: read the finished architecture documents, their seams, and the API and persistence contracts, and only then write. That read ran to around eight thousand lines across twenty-one documents. It sounds disproportionate, and it wasn't.

The highest-yield activity in the entire method turned out to be neither writing nor diagramming. It was reading two finished documents against each other and hunting for the place they disagree. Every contradiction found that way was a real design error, not a naming problem, and a stale seam that says different things on its two sides is worse than a missing one, because a missing seam gets noticed the moment someone needs it while a stale one gets quietly implemented.

This turned out to deserve a post of its own, so I gave it one. [A later post](/p/docs-should-argue-with-itself/) is entirely about cross-reading: why the contradictions live in the space between individually correct documents, the specific crossings worth hunting, and how to do it without drowning in eight thousand lines. For the method, the point is only this: the reading isn't overhead in front of the work. It's the work.

## The Failure Modes, With the Tell

Each of these happened. The tell is what makes it recognizable next time.

**Inventing problems during an architecture pass.** I asked the session to record where the data comes from, and it started generating licensing concerns about paid subscriptions that nobody had raised. My response, once the profanity is filed off, was clean: this is architecture, not solution design. "We will consume paid sources" is architecture. "How we handle the licensing" is implementation, and raising it early doesn't make it handled; it just makes the document longer and the end state harder to see. *Tell: the work is describing how something will be dealt with rather than what it is.*

**Inventing vocabulary.** The session coined a word, "the waterfall," for something the system already had a name for. I had it dropped, with a commit that said so plainly: the word did no work. New vocabulary has to earn its place; a term that duplicates an existing name splits search, splits the reader's model, and makes the document sound like it knows something it doesn't. *Tell: a noun has appeared that duplicates an existing rule's name.*

**Presenting a free query as an open design question.** The session raised "should coverage be groupable by direction?" as an open question. The records already carried a direction field, so it was a query parameter, not a decision. I asked whether there was actually a decision to be made or just the ramblings of an AI, and the honest answer was ramblings. Open questions cost my attention, which is the scarcest thing in the process, and padding the list devalues the real ones. *Tell: the open question's answer is already a field on an existing record.*

**Over-abstracting when asked for surfaces.** The session's first cockpit design collapsed nine subsystems into one conversation stream and three views. It was elegant and it was wrong, because it answered "show me the system" by hiding the system behind a single interlocutor. Everything is a conversation is true about the interaction, not about the structure, and I need to see the structure, because the subsystems are what I reason about. *Tell: the design has fewer visible parts than the architecture has subsystems.*

## Short Sentences In, Long Consequences Out

The division of labor that made this work is worth stating plainly. I supply the mission, the constraints, the real incidents, and every boundary call, and I kill things. The session works out consequences, drafts, cross-reads, finds contradictions, and argues back. A bounded subagent executes against a written packet and doesn't get to widen its own scope.

The thing that makes it run is an asymmetry: my sentences are short and the consequences aren't. "Regime and cycle are the Brain's, settle it there" is eleven words, and it moved four layers across six documents. The session's whole job is that expansion. If a decision produces a one-line diff, the session probably didn't look hard enough for who else depended on it.

The session's single most valuable output is the objection. Every time it argued back, about a duplicated egress or about a direction the join should flow, the design got better. Every time it agreed with me too quickly, it produced work that had to be redone. An AI that only ever complies isn't cheaper than one that pushes back; it is more expensive, because you pay for the agreement twice.

## The Commit Message Carries the Reasoning

One habit did more than any other, and it is nearly free. The reasoning goes in the commit message, because the diff can't carry it.

A documentation diff shows that a table gained a row. It can't show that the row exists because a data series has three consumers reading it with opposite polarity, that the alternative was rejected because it recreated a boundary split we had just removed, or that the change closed a question that had been sitting open in two other documents for two days. Written into the message, all of that survives. The commit log for that branch became a decision log: it held reasoning that never made it into any document, and it was the primary source I used to reconstruct this method in the first place. If a commit message would be shorter than the argument that produced it, the argument is being thrown away.

## What I Would Tell Someone Starting the Next Subsystem

Read the mission, and read the two subsystems on either side of yours. Argue before you write; if you can't state the boundary in one sentence and defend it against your own hardest counter-example, you aren't ready. Derive the subsystem's job from its customers, never from a wish list. Write architecture first, and never let it describe the present. Then seams, then API, then store, then workers, in that order, no skipping, and if you catch yourself designing a worker, go back and check the seams exist. Fill in what happens when each dependency is unavailable early, because that is what surfaces the seam you missed. Say what crosses no boundary; the omissions are decisions. Read your document against every neighbor and hunt for the disagreement, because that is where the real errors are. Put the reasoning in the commit message. And leave your open questions in, numbered, but only the ones you genuinely can't answer.

The end state isn't the point of the exercise. The point is that every rule in it can be traced back to something that actually broke, and anyone who arrives later can see the wreck the rule was built from. That's the difference between a method and a style guide, and it is the difference between this system and the one I threw away.
