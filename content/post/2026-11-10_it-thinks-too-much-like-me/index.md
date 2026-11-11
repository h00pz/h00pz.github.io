---
title: "It Thinks Too Much Like Me"
slug: it-thinks-too-much-like-me
date: 2026-11-10
draft: false
description: "I hoped a language model could read a trading day like a person and beat the quants at it. It read exactly like a person, agreed with me on every single day, and we turned out to be wrong together, because the one thing it could not do was be wrong differently than I am."
tags:
  - slm
  - evals
  - agents
  - guardrails
  - prompts
categories:
  - Small Model Systems
image: it-thinks-too-much-like-me.png
---

I wanted to know if a language model could beat a quant. Not at arithmetic, and not in general, but at one specific thing I had been personally losing at for months: reading a trading day well enough to know when to get out of a position.

The hope underneath the experiment was quieter and a little embarrassing. I read a market day like a story, I always have, and a language model, whatever else it is, reads like a person too. So maybe the human way of seeing a day, the thing the pure statistics throw away, was an edge, and maybe the model could do it faster and without getting bored or scared. I set the model up as a control to find out, fully expecting to be delighted.

I was not delighted. I was unsettled, which turned out to be the more useful thing.

## What a day looks like when you stop seeing numbers

To explain what went wrong I have to explain how I read a day, because the whole experiment lives inside that way of seeing.

A trading day is not a column of numbers to me. It is a day in the life of a crowd, and like any character the crowd gives off **tells**. A tell is a small behavior that leaks intent. SPY pokes below the morning's range, the volume drying up as it slips, and then it snaps hard back above the line, and *that* is a tell. The information in it is not the poke. It is the snap-back. The poke was the provocation, the response is where the intent lives, and a crowd that pushes below support only to buy it right back is a crowd that was testing, got its answer, and is not actually leaving. Same event, opposite meaning, and the meaning sits in the reply.

Tells assemble into **chapters**. A chapter is a stretch of the day where one story explains everything coming in. "Buyers are in control" is a chapter, and it stays the chapter for as long as every dip gets bought, every poke snaps back, every tell fits the story. The chapter does not end because the price fell. It ends the moment a tell arrives that the story can no longer explain, a dip that doesn't get bought, a snap-back that never comes. That failure to explain is the **chapter break**, and reading a day well is mostly feeling the break the instant the current story stops accounting for the tape, rather than three chapters later when the loss is already on the screen.

The whole day is those chapters stacked against a slow backdrop, the session's drift, the question of who has been winning the longer contest. That stack is the **story**. Reading it is not predicting the next bar. It is characterizing the present: who is winning right now, and has that just changed.

I am decent at this. The entire question was whether a model could do it, and whether doing it was worth anything.

## Two readers, one tape

I made the model read days the hard, honest way. One bar at a time, revealed in sequence, with the decision committed before the next bar existed, so it could never peek at the future and launder hindsight into a clean call. It wrote each day's tells, named the chapters, marked the breaks, and at every step said whether to hold the position or get out. I read the same days myself. Then we compared, bar by bar, for a whole month of them.

## We agreed more than was comfortable

We agreed. Constantly. Across the test month the model's blind read reproduced the chapters I had marked and called the turn on essentially every day, and where we diverged it was granularity, not substance: it saw the same shakeout I saw, named the same breakdown I named, and felt the same chapter breaks within a bar or two of where I felt them. Twenty-one days, twenty-one agreements on the shape of the story.

For about a day that felt like the result. Two independent readers, one of them a machine with no memory of my notes, converging on the same account of the same day. That is what validation is supposed to look like.

Then I graded it, and the agreement curdled into something worse than disagreement would have been.

## And the dumbest rule in the room beat us both

I scored both our reads against the stupidest policy available, a rule with no reading in it at all: get in, hold to the close, take whatever is there. Ride to flat. No tells, no chapters, no judgment, a rule a potted plant could run.

The potted plant won.

Every principled exit the read produced, mine and the model's alike, lost to just holding. The reason is exact and a little brutal. At the bar where you have to decide, the day where a deep, gut-wrenching dip is about to recover and the day where the identical dip is the first move of a real breakdown look *the same*. The two largest buckets in the whole corpus are "the dip that shook you out and then ran to a winner" and "the move that went your way and then quietly died," and at the decision bar their tells are the same tells. The evidence that would separate them lives in the bars that have not printed yet. So a good reader, playing it straight, says "it's turning, get out," and about half the time gets out at the exact low of a shakeout that was about to pay. The read was not sloppy. The information was not there.

Then I let the model think harder. Longer reasoning, more deliberation, the move everyone reaches for when a model underperforms. It got worse. With thinking on it beat the plant *less* often than with thinking off. Given more room to tell itself a story, it told a more elaborate one, and bailed with more conviction out of the shakeouts it should have sat through.

## The human-likeness was the bug

Here is the part I did not want. The statistical floor I had been hoping to beat, a boring base-rate lookup that at a given decision bar just asks what happened on the most similar past days and follows the majority, beat both of us, and it beat us precisely because it does not read. It sees no shakeout and no breakdown. It sees a distribution, declines to call the one bar nobody can call, and holds. It is not smarter than the model or than me. It is immune to the specific thing the model and I share.

Because that is what our agreement actually was. I had read it as two readers confirming a signal. It was two readers importing the same bias. The model agreed with me not because we had both found the truth, but because it reads the way a human reads: hungry for the noise to mean something, quick to promote a scary-looking dip into a story about sellers taking over, built to resolve ambiguity into narrative because narrative is what makes a sequence feel understood. I do every one of those things. The model's human-likeness, the exact quality I had hoped was the edge, is a faithful copy of the cognitive habit that was costing me money. When the machine that thinks like you agrees with you, you have not been confirmed. You have been reflected.

## What the read is actually for

I am not going to tell you the read is worthless, because that is its own clean-sounding wrong answer. The read is real. The model genuinely characterizes a day, and so do I, and twenty-one days of blind agreement is not nothing, it says the capability exists. The mistake was pointing a *characterization* tool at a *prediction* job. "Who is winning right now" is a question the tape can answer. "Will this specific dip recover" is a question whose answer is not on the chart yet, and no amount of reading, human or synthetic, conjures information that has not happened. I had [just made the same mistake from the other direction](/p/a-coin-flip-by-morning/), asking a different model to call a next bar whose answer wasn't on the chart either, and collecting a coin flip for it. That job belongs to the quant, who gets it right by refusing to take it.

So the read keeps its seat, just not the one I tried to hand it. It can label the regime, size the bet when the day is legible and stand down when it isn't, flag the day that doesn't look like the others. All of that is characterization. The exit stays with the dumb rule that beats me, and I have made a quieter peace with the fact that my best reading of a market day is a genuine skill that does not, by itself, print money.

The lesson I actually walked out with is not about trading. It is that a second opinion is worth something only to the degree it can be wrong *differently* than you are. I went looking for a second reader and built one that shares my blind spot, then nearly mistook our matching blind spots for sight. The reader I needed was the one that doesn't think like me at all, and it had been sitting there the entire time, holding to the close, saying nothing, being right.
