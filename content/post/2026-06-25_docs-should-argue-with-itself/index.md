---
title: "Architecture Documentation Should Argue With Itself"
slug: docs-should-argue-with-itself
date: 2026-06-25
draft: false
description: "An architecture doc and its derived seams drift apart. Cross-reading, checking adjacent specs for disagreements, catches it before production does."
tags:
  - ai
  - architecture
  - hasf
  - seams
  - systems
categories:
  - AI Coding Scar Tissue
image: architecture-docs-agrue-with-themselves.png
---

Here's a thing nobody tells you about architecture documents: each one can be perfectly correct on its own and the set of them can still be wrong. A document is written by one person, or one session, holding one subsystem in their head, and it comes out internally coherent, every section agreeing with every other section, the whole thing humming along in tidy self-consistency. The contradictions don't live inside the documents. They live in the space between them, at the boundaries, exactly where nobody is looking because everybody is busy admiring how consistent their own document is. This is the [locally correct, globally wrong](/p/why-we-threw-away-portfolioos-v2/) shape moved up to the level of documents: each one right, the set of them wrong, and the error waiting in the seams nobody read across.

I learned this the way I learn most things, which is by being wrong at scale and then getting corrected. During the week I rebuilt pOS I produced a stack of clean, confident subsystem and seam documents, felt pretty good about them, and then discovered that the single highest-yield activity in the entire process wasn't writing any of them. It was reading two finished documents against each other and hunting for the place they disagreed.

This post is an argument for making that a deliberate practice. I've started thinking of it as making the documentation argue with itself, on purpose, in a folder, before the running system does it for you in production.

## Coherent Is Not the Same as Correct

The trap is that internal coherence feels like correctness. When you finish a document and every part of it lines up, you get a satisfying sense that the thing is done and right. And it might be done and right about its own subsystem. That tells you almost nothing about whether it agrees with the subsystem on the other side of the seam, because you wrote it while thinking about one side and only one side.

A seam has two documents describing it, one from each lane, and the failure mode is that they were written at different times by different sessions who each made a locally sensible assumption. One lane thinks it's reading from the other; the other thinks it's publishing somewhere else. Both documents are clean. Both are internally consistent. Together they describe a system that cannot exist, and you will not find that by reading either one carefully, no matter how carefully. You find it only by reading them against each other.

## Architecture and Seams Are in a Race

The sharpest version of this isn't two static documents that happen to disagree. It's two documents that are supposed to stay in sync and drift out of it over time, which is a race condition in the most literal sense: the correctness of the system depends on the order things were written in, and on which document a reader happens to open first.

Here's the mechanism, and it's the whole reason the problem exists. A subsystem's architecture document decides what a lane owns. Its seam documents describe what crosses that lane's boundary, and they are derived from the ownership, so a seam is only correct relative to the architecture that produced it. The moment you change the architecture, move an ownership from one lane to another or redraw a boundary, every seam that was derived from the old ownership is now describing a world that no longer exists. If you update the architecture document and don't chase down every seam that depended on it, you have left two documents describing the same boundary in two incompatible ways.

And nothing decides which one wins. The next person to touch that boundary opens one of the two documents, and whichever they open first is the version they believe. That is the race. It isn't that the documents are wrong, it's that the system's behavior now depends on a reader's arbitrary choice of which file to read, which is exactly the kind of nondeterminism you spend a whole career designing out of running systems and then cheerfully reintroduce into your own documentation.

I hit this one dead on. A seam document had a lane reading custody directly, which was true when it was written, because that lane fetched its own material. Then the architecture changed: collection became the only egress, and that ownership moved. The architecture document knew. The seam document didn't, because nobody had propagated the change down to it. For a while both sat on disk, both read cleanly, and they described two different systems. A stale seam is worse than a missing one for exactly this reason: a missing seam announces itself the moment someone needs it, while a stale seam gets found by whoever opens it first, believed, and faithfully implemented, rebuilding a world that stopped being true.

## Winning the Race on Purpose

The fix isn't to cross-read harder after the fact, though you should do that too. It's to make a change to the architecture propagate to every seam it touches in the same motion, so the two documents never get a window in which to disagree. When regime and cycle moved from one lane to the Brain in pOS, that was a one-sentence change about who owns an assumption, and following the derivation it landed as twelve seams renumbered in the same pass. One architectural decision, every derived seam updated with it, and no moment where the architecture and its seams told different stories.

There's a cheap invariant that catches the race when it slips through anyway: count your seams, and put the number in the commit message. Every seam change ends with a line like "Hunt drops to twelve seams." The count is almost free to maintain and it works as a tripwire. When the number moves and you didn't expect it to, something in a boundary changed that you didn't consciously decide, which is your signal that the architecture and the seams have started to race and you'd better go find out who's ahead.

## Cross-Reading Is the Actual Work

So the technique is to stop treating documents as things you read one at a time and start treating adjacent ones as a matched pair whose entire reason for being examined together is to find the disagreement. It felt disproportionate the first time. After I got stopped mid-mistake, the instruction was to read the finished architecture documents, their seams, and the platform contracts before writing another word, and that read came to roughly eight thousand lines across twenty-one documents. I was sure it was overkill.

It was not overkill, and every single contradiction it surfaced was a real design error rather than a naming nit. Cross-reading isn't overhead you do before the work. It is the work, and budgeting for it explicitly is the difference between catching a broken boundary in a document and catching it in production six weeks later.

There's a way to do it without drowning, which is to read for crossings and not for prose. You aren't savoring the writing. You're hunting for exactly four things: an endpoint one document offers that another doesn't know exists, a record two lanes both think they write, a direction that has quietly flipped since it was written, and a rule one lane states that another lane's flow casually violates.

## What It Actually Caught

The abstract version isn't convincing, so here are the real ones. A good example beats a paragraph of theory, and every one of these was caught exactly this way, by holding two clean documents up against each other.

Reading the Committee's seam document against the Evidence document, the Committee's turned out to contradict itself the moment it was held next to its neighbor. It listed a cross-lane write, a "macro promotion" posting into a shared registry, while its own later section said that exact write was forbidden, and the entire prior repair effort had been about removing precisely that kind of cross-lane write. Nobody was ever going to find that by reading the Committee document alone, because inside its own four corners it made a kind of sense. You only see it when you read it against the document on the other side of the boundary it was violating.

That one was a live contradiction between two lanes. The stale-custody seam from earlier was the same shape stretched across time, one document that had quietly lost its race with the architecture it was derived from. Both kinds are found the same way, by refusing to read a document alone.

## Even a Document Can Contradict Itself Out Loud

My favorite one, though, I found while writing the very reconstruction that these posts are based on, which is a fittingly humbling place to trip. When two old subsystems were merged and renamed, a mechanical find-and-replace ran across the documents, and it corrupted the exact sentence that explained the rename. The result was a subsystem document whose supersession line, in plain text, on disk, read:

```text
Supersedes pos-collection and pos-collection.
```

A document solemnly announcing that it supersedes itself, twice. Its neighbor had the matching bug, claiming to supersede a document by its own name. Neither changes a design decision, and both are exactly the sentence a future reader needs to be correct about where the truth moved. The lesson isn't that find-and-replace is dangerous, though it is. It's that a document talking about a change is the most likely place for a blind edit to quietly break, and the only thing that catches it is reading the sentence as if you didn't already know what it was supposed to say.

## Make the Argument a Habit

The reason I like the phrase "argue with itself" is that it reframes contradiction from something embarrassing into something you're actively fishing for. When two documents disagree and both look deliberate, the worst move is to quietly pick one and make it match, because you've just erased a real question. The right move is to surface the contradiction with both sides stated and let it be argued, because a contradiction found this way is a design decision that was never actually made, wearing the costume of a decision that was.

So a mature set of architecture documents shouldn't read like a collection of confident, self-satisfied essays that happen to sit in the same folder. It should read like a system under interrogation, where the interesting moments are the seams where two honest documents can't both be true. Those seams are where the real architecture lives, and cross-reading is just the discipline of going to look. The documents that agree with themselves are comfortable. The documents that argue with each other are correct.
