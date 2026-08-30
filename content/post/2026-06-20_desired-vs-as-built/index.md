---
title: "Desired Architecture vs. As-Built Reality"
slug: desired-vs-as-built
date: 2026-06-20
draft: false
description: "Diagrams describe intent; running systems accumulate difference. Keep the desired end state and the as-built reality in separate documents to trust either one."
tags:
  - ai
  - architecture
  - hasf
  - systems
  - state
categories:
  - AI Coding Scar Tissue
image: as-built-vs-desired.png
---

For a long time my architecture diagrams were a kind of flattering fiction. They showed the system I wished I had, drawn with confident boxes and clean arrows, and I kept mistaking that picture for documentation of the system I actually had. The two were related, the way a real estate listing is related to the apartment, but they were not the same thing, and the gap between them was exactly the information I most needed and least wanted to look at.

The honest version of the problem is this. A diagram describes intent, and a running system accumulates difference. Implementation makes compromises the diagram never anticipated, discovery reveals dependencies nobody drew, and every deadline leaves a little residue of "we'll fix that later" that quietly becomes permanent. If your one architecture document tries to be both the plan and the record, it ends up being useless for both, because you can't tell from it what you're building toward or what actually exists today.

This post is about the discipline that fixed it for me, which is almost aggressively simple: keep the desired end state and the as-built reality in different documents, and never let one pretend to be the other.

## The Diagram Is a Wish, and That's Fine

There's nothing wrong with an architecture document being aspirational. That is what it's for. It describes where the system is going, what each part is supposed to own, and how the pieces are meant to fit, and all of that is a statement about the future, not a report on the present.

The mistake is letting it also claim to be the present. The moment a document says "here is how it works today," every temporary hack in the codebase gets promoted to a decision, because it's now written down next to the real decisions and nothing distinguishes them. The accidents acquire the authority of intent. Six months later someone reads the doc, sees the hack described in the same calm prose as the architecture, and faithfully preserves it, because how were they supposed to know it was a wart and not a feature?

## Never Put As-Built in an Architecture Doc

So the rule I now follow, and the single most repeated correction from the week I rebuilt pOS, is blunt: never put as-built state in an architecture document. Every subsystem document carries the rule literally, near the top, so no reader can miss it:

```text
> This document describes the DESIRED END STATE, never the current one.
```

That line is doing real work. It tells the reader that everything below it is a target, that any gap between the document and the running system is a gap in the system and not an error in the document, and that "but it doesn't actually do that yet" is never a valid objection to anything the document says. The document is allowed to describe a subsystem that is only half-built, or not built at all, without apologizing, because describing the destination is its entire job.

## The Now Lives Somewhere Else

Current state absolutely matters. You have to know what's actually collected, what's merged but dark, what's still a stub. That truth just belongs in a different kind of document, one whose whole job is to change.

In pOS the desired end state lives in the subsystem and seam documents, and the "now" lives in a separate register that holds the as-built status and the migration debt. That register is the [Failure Manifest Log](/p/the-failure-manifest-log/) from the last post, doing at the subsystem level exactly what it does at the feature level, which is to keep the messy present in a document that expects to be wrong soon. When I split the collection lane out of two older subsystems, the architecture doc described the clean end state, and a register carried the messy truth in plain rows: what had changed, what state the lane was actually in, what was missing, what was still open. One entry admitted that the lane was "merged and dark," which is a wonderful phrase for a thing that is fully built, wired end to end, has fired on real data, and is sitting there with every feature flag defaulted to off. Not a prototype. A working system with the lights deliberately switched off, and the register said so, while the architecture document stayed serenely focused on where it was all headed.

The inventory documents work the same way. A line like "488 iShares tickers are collected while GDX, GLD, and XLE are absent" is true today and false next month, so it lives somewhere that expects to be wrong soon, not in the document that's supposed to be durable.

## The Deployed Axis Is the Honest Half

The Feature Memory Ledger from [the previous post](/p/the-failure-manifest-log/) tracks the same split at the level of individual features, and it's the cleanest example of why the separation matters. Every item carries a deployed axis, live or partial or merged or built-but-not-deployed or pending, and that axis is kept strictly apart from how finished the design is. A feature can have a complete, blessed design and a deployed state of nothing, and the ledger says exactly that rather than rounding a finished design up to a finished feature.

There's a rule underneath it that I find genuinely bracing: because the current pOS is a clean rebuild, progress started at zero, and a feature that existed in the old version earns no credit at all. The old code is a harvest source, not a head-start. A ledger that let v2's mere existence inflate v3's progress would be lying in precisely the way the whole apparatus exists to prevent, so it refuses to, even when the honest number is embarrassing.

## One Rule Against the Gap Filling Itself

The framework has a small rule that guards the boundary between current and historical state, and it's worth stating because it's the same instinct at the field level. When a current value is missing, the system shows unavailable. What it must never do is go rummaging through the history for an old value to display in the gap:

```text
Current field missing
→ display unavailable

Never:
search historical revisions for replacement current text
```

That is the whole thing in five lines. A system that quietly backfills the present with the past is confidently wrong, which is the worst way to be wrong. I'd much rather my portfolio system admit it doesn't currently know a number than hand me last quarter's figure dressed up in this quarter's clothes and let me trade on it.

## You Need Both, and You Need the Distance

None of this is an argument that as-built reality is unimportant. It's the opposite. The as-built record is often the most valuable thing you have, because the distance between the target and the truth is the actual work, and you cannot manage a distance you refuse to measure.

What you can't do is store both truths in the same sentence. Mixing them gives you a document that can't be trusted for either purpose, the way a map that draws the road you're planning to build in the same ink as the road that exists will get somebody lost. Keep the desired architecture pure, keep the as-built reality in something that expects to change, and keep an honest count of the gap between them. That gap isn't an embarrassment to be smoothed over in the diagram. It's the most useful number in the whole system, and the only way to keep it honest is to give it a document of its own.
