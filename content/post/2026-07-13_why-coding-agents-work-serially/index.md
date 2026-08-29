---
title: "Why My Coding Agents Work Serially"
slug: why-coding-agents-work-serially
date: 2026-07-13
draft: false
description: "Parallel implementation sounds faster until several agents independently change assumptions underneath one another. Serial execution can beat parallelism while the architecture is still evolving, and deliberate sequencing makes AI-generated work far easier to review and trust."
tags:
  - ai
  - architecture
  - agents
  - systems
categories:
  - AI Scar Tissue
image: why-coding-agents-work-serially.png
---

If you'd told me a year ago that I'd end up running my coding agents mostly one at a time, on purpose, I'd have assumed I was doing it wrong. The entire pitch of agents is parallelism. You have a fleet of tireless workers who never need coffee, so obviously you point all of them at the problem at once and collect your tenfold speedup. Running them serially sounds like buying a race car and driving it in first gear.

And yet here I am, sequencing them deliberately, because I've watched what parallel does to a system whose architecture is still moving, and it isn't a speedup. It's a very fast way to generate work that has to be redone. [The previous post](/p/subagents-cheap-coordination-expensive/) was about coordination being the expensive part of a multi-agent system. This one is the practical consequence I actually live by, which is that when the ground is still shifting, the cheapest coordination strategy is often just to go one at a time.

This isn't an argument against parallelism forever. It's an argument that parallelism has a prerequisite most people skip, and that serial execution is the honest default until you've met it.

## Parallel Assumes the Ground Holds Still

Here's the thing parallelism quietly requires: the agents have to be working against assumptions that don't change while they work. If agent A and agent B are both building against a stable, agreed architecture, they can absolutely run at the same time, because neither one is going to pull the rug out from under the other. Their worlds are fixed, so their work composes.

The moment the architecture is still being figured out, that guarantee evaporates. Agent A makes a reasonable decision about a boundary, agent B makes a different reasonable decision about the same boundary, and now you have two pieces of work built on two incompatible views of a thing that was never settled. Neither agent was wrong. They were both reasoning correctly from an unstable base, and the instability is the problem, not the agents. Parallel execution doesn't just fail to help here. It actively manufactures conflict, because it takes an unresolved question and lets several workers answer it independently at speed.

## What Parallel Actually Cost Me

I have the receipts, because I ran the experiment without meaning to. During one heavy build I had three implementations going at once, each touching the same few files, without giving them isolated workspaces. It felt efficient. It was the opposite. The three builds kept loading enormous overlapping context, stepping on each other's edits to the shared files, and the primary session ran itself out of context twice trying to hold all three in its head at the same time. The commit that came out of it acknowledged the whole thing as a self-inflicted wound: parallel implementers needed isolation I hadn't given them, and until they had it, running them together was slower than running them apart.

The subtler cost showed up in a different form: agents redoing each other's assumptions. One would decide how a thing worked, another would independently decide it worked differently, and the reconciliation afterward ate every minute the parallelism had supposedly saved, plus a few more for the confusion. Every time I ran unsettled work in parallel, I paid for the same decision twice and got a worse version of it than if one agent had just made it once and moved on.

## Serial Turns the Unknown Into the Known

Running one agent at a time has a property that sounds boring and is actually the whole point: each agent starts from a base that's more settled than the one before it. Agent one makes a decision and it lands. Agent two starts in a world where that decision is now a fact, not an open question, so it has one fewer thing to guess about and one fewer way to conflict. The sequence itself is doing work. It's converting open questions into settled facts, one at a time, so that later agents operate on firmer ground than earlier ones.

Parallel execution can't do that, structurally, because all the workers start at the same moment against the same unsettled base. They can't benefit from each other's decisions because those decisions don't exist yet when they start. Serial execution is slower in the trivial sense that only one thing runs at a time, and faster in the sense that matters, which is that far less of what runs has to be thrown away.

## Serial Is Also Reviewable

There's a second reason I keep the agents in a line, and it might matter more than the speed argument: I can actually review the work. When one agent makes one bounded change against a known state, I can look at what it did, understand it, and decide whether it's right before the next thing is built on top of it. The change has a clear before and after, and a clear reason, and it fits in my head.

When five agents change five things at once against a moving base, the diff is a smoothie. I can't tell which change caused which effect, I can't tell whether two of them quietly disagreed, and I certainly can't trust the whole thing the way I can trust five changes I watched land one at a time. Serial execution keeps AI-generated work at a size and cadence where a human can stay in the loop, and staying in the loop is not a nice-to-have when the thing writing your code is confident, fast, and occasionally, spectacularly wrong.

## Earn the Right to Parallelize

None of this means parallelism is bad. It means parallelism is a reward you earn by stabilizing the architecture first, not a default you start with. Once the boundaries are settled, the seams are contracts, and the work decomposes into pieces that genuinely don't touch each other's assumptions, then absolutely, fan it out, because now the ground holds still and the agents can't collide.

But while the architecture is still being discovered, which is most of the interesting part of any real project, serial is the honest speed. It looks slower on the diagram and it's faster in the wall-clock reality of not redoing things, and it keeps the work reviewable while it matters most. So I drive the race car in first gear on purpose, for now, because the track is still being built, and the fastest way through a course that's changing under you turns out to be one careful lap at a time.
