---
title: "Stop Building Agents. Start Building Systems."
date: 2026-04-02
draft: false
description: "Reliable AI apps bound model inference inside explicit architecture, persistent state, and clear seams, instead of handing everything to one autonomous agent."
tags:
  - ai
  - architecture
  - agents
  - small-language-models
categories:
  - Small Model Systems
image: cover.png
---

While working on PortfolioOS I eventually found myself staring at an architecture that I didn't trust. Nothing was technically wrong with it. The models worked, the prompts worked, and the tools worked. I could ask the system a question about the portfolio, have it gather information, reason about what it found, and produce a pretty good answer.

The problem came when I started asking what happened **after** the answer. If the model decided something about an investment, where did that decision live? If it changed its mind tomorrow, how would I know why? If it discovered a new company, was it allowed to add it to the portfolio? If one model produced a piece of analysis that another model needed, were they supposed to talk directly to each other? What happened if a model misunderstood the state of the portfolio but continued working anyway?

The easiest answer to every one of these questions was to give the agent another tool and another instruction. That worked for a while, but eventually I had something that could read almost everything, reason about almost everything, call almost everything, and decide what should happen next. In other words, I had accidentally built a giant application where the central integration layer was a language model.

I can point at the day it stopped being abstract. That system was PortfolioOS v2, and when I finally asked it what it believed, the reasoning had run fine, real findings were filed, and the field that was supposed to say whether any position was being watched against its thesis read `null` on every one of them. The intelligence worked and nothing heard it. I eventually [threw the whole thing away](/p/why-we-threw-away-portfolioos-v2/), and this first series is the set of rules I wrote so I wouldn't build it a second time.

That was the point where I stopped asking how to build a better agent and started asking a different question: **what if the agent is the wrong abstraction?**

This post covers where that question led me while building PortfolioOS, Atlas, and eventually the **h00pz Architecture Specification Framework (HASF)**.

## The Problem With The Agent

The basic agent pattern is incredibly appealing. You give a model a prompt describing what you want it to accomplish, give it some tools, and let it figure out how to get there. For smaller problems this works amazingly well, and it is still one of the fastest ways I know to prototype something that would have been prohibitively difficult to automate a few years ago.

The problems started appearing for me as the applications became larger. PortfolioOS is probably the best example because there isn't really one job called "manage a portfolio." There are a bunch of different jobs hiding underneath it. Something needs to understand the current market environment, something needs to discover companies worth researching, something needs to determine whether the evidence supports an investment thesis, and something needs to understand why each account exists in the first place. After all of that, something still has to turn those conclusions into an actual portfolio.

My first instinct was similar to what I see in a lot of AI projects today: build agents for those jobs and let the agents work together. The problem is that "work together" very quickly becomes an architectural black hole. Does the research agent talk directly to the portfolio agent? Can the portfolio agent ask the market agent to change its opinion? Can the market agent modify portfolio state? What happens when two agents disagree? Which version of the truth gets stored, and who owns the object they're both modifying?

You can answer all of these questions with prompts, but I eventually concluded that I didn't want to. Once I started asking these questions seriously, I realized I wasn't dealing with an AI problem anymore. I was dealing with a distributed systems problem that happened to contain AI.

## Models Are Really Good At Some Things

None of this is an argument against using models. Quite the opposite. The reason I keep building these systems is because language models can do things that would have been extremely difficult to automate a few years ago.

A model can read a collection of earnings reports and determine whether management's story is changing. It can compare competing pieces of evidence, take a messy meeting transcript and figure out what decisions were actually made, or look at several investment theses and identify where their assumptions contradict each other. These are exactly the kinds of problems where inference is valuable because the answer isn't sitting neatly in a database waiting to be retrieved.

The mistake I was making was assuming that because the model was good at reasoning about the problem, it should also control everything surrounding the problem. A model might be very good at determining whether new evidence weakens an investment thesis, but that doesn't mean the model should also decide where the thesis is stored, modify the portfolio, calculate the new position size, update historical records, and decide which other parts of the application should now run.

Those are completely different jobs, and once I separated them the architecture started getting much easier to understand.

## Make The Boring Parts Boring

One of the rules I eventually adopted is simple: **if something can reasonably be deterministic, make it deterministic.** Databases already know how to store things, APIs already know how to expose things, functions already know how to calculate things, and schedulers already know when something should run. We don't need a language model to reinvent any of that.

In PortfolioOS, for example, a model might determine that the evidence supporting an investment thesis has materially changed. That's exactly the kind of fuzzy reasoning problem I want a model working on. Once that conclusion exists, however, everything around it can become much more boring. The result has a defined structure, the system knows where it gets stored, the previous result doesn't disappear, the time the analysis occurred gets recorded, and other components can react to the changed state using explicit rules.

The model did the thing it was good at and software did the things software is good at. This became one of the most important architectural ideas behind both PortfolioOS and Atlas: the goal isn't to eliminate probabilistic behavior, because the entire reason I'm using models is to solve problems that require inference. The goal is to contain that probabilistic behavior so it doesn't become the operating model for the entire application.

## Building Seams Instead Of Connections

Once I stopped thinking primarily about agents, I started thinking a lot more about seams. A seam is the boundary between two parts of the system, and the more I worked on PortfolioOS the more important those boundaries became.

If Portfolio Construction (the subsystem responsible for turning investment mandates, research, and market context into actual portfolio allocations) needs information from Hunt (the subsystem responsible for discovering and researching potential investments), I don't want Portfolio Construction to know how Hunt thinks. I want Hunt to produce a defined artifact with a contract that Portfolio Construction understands.

This sounds like incredibly normal software engineering because it is. The interesting part is how much more important it becomes when one side of the seam contains a language model. Without an explicit contract, it becomes very easy to let the model compensate for a poorly defined architecture. One component produces something ambiguous and the model figures it out. Another component changes its output and the model adapts. Some required information is missing and the model makes a reasonable assumption.

At first this feels like flexibility, but it is also how uncertainty starts leaking throughout the entire application. Explicit seams force me to answer the uncomfortable questions early: what exactly does this component produce, who owns the data, what is allowed to modify it, what assumptions are safe, what happens if the output is incomplete, and what happens if the next component rejects it?

Once those questions have answers, the model has a much smaller job. That's a feature, not a limitation.

## State Belongs To The System

The next problem was memory. A lot of agent systems talk about memory as though the application needs to somehow make the model remember what happened previously, but I think this mixes together two very different things: models need context while systems need state.

If PortfolioOS decided six months ago that I purchased a company because it controls a specific infrastructure bottleneck, that decision shouldn't exist because an agent remembers having a conversation about it. The thesis should be an object in the system. The evidence should exist alongside it, changes to the thesis should be recorded, previous conclusions should remain available, and the relationships between all of those things should be explicit.

When a model later needs to reason about that investment, the system can assemble the relevant state and provide it as context. The model's context window is temporary working memory; the application's state is durable memory. Treating those as separate concerns turned out to be a major architectural simplification.

It also makes the models replaceable. I can change models without changing the history of PortfolioOS, rerun an analysis using a different model, or compare what two different models concluded from the same underlying state. The accumulated intelligence of the application doesn't disappear because I restarted an inference server or swapped one model for another.

## Small Model Workers

This eventually changed how I thought about the models themselves. Instead of building a giant intelligent agent, I started building workers where each worker gets a bounded task, enough context to perform that task, and a specific output it is expected to produce.

One worker might challenge an investment thesis while another classifies evidence. Another might summarize a collection of documents, look for contradictions, or convert the operator's intent into a structured plan. The important part isn't that every worker necessarily uses a Small Language Model. The important part is that the **job itself is small**. This has since become something close to received wisdom in agent engineering: HumanLayer's <a href="https://github.com/humanlayer/12-factor-agents" target="_blank" rel="noopener">12-Factor Agents</a> makes "small, focused agents" a numbered principle, on the same reasoning, that a bounded job keeps the context small enough for the model to stay reliable.

That distinction gives me a much more interesting scaling mechanism than continually making one agent smarter. Different workers can use different models based on what the job actually requires. A simple extraction task doesn't need the same model as a difficult reasoning problem, a vision task doesn't require keeping a vision-capable model involved in the rest of the workflow, and a deterministic calculation doesn't require a model at all.

The application becomes a collection of specialized components instead of one extremely talented employee with the keys to the building. This is also where I think a lot of the discussion around Small Language Models gets more interesting. The useful question isn't simply whether a small model can replace a large model; it is whether we can design the problem small enough that the large model was never necessary in the first place.

## What Happens When Things Go Wrong

Another thing I learned building these systems is that failure needs to be part of the architecture. Models are going to be wrong, sources are going to be missing, APIs are going to fail, two pieces of evidence are going to disagree, and eventually the system is going to encounter something nobody anticipated.

The answer can't simply be "hopefully the agent figures it out." Sometimes the correct system behavior is to stop because the evidence is insufficient, a state transition is invalid, a worker is trying to read information outside of its boundary, or the system simply can't prove that the requested work has been completed safely.

This became especially important as I started building Loop (the PortfolioOS subsystem responsible for continuously monitoring existing positions and deciding when a position needs to be reconsidered). A system watching real money can't treat uncertainty as an invitation to improvise. If Loop identifies a possible problem but can't establish enough evidence to act, I would rather have the system surface the uncertainty than manufacture confidence so the workflow can continue.

The goal isn't to build a model smart enough that failure disappears. The goal is to build a system where failure is visible, contained, and understandable.

## HASF

After repeatedly encountering these same problems in PortfolioOS and Atlas, I eventually realized I needed a repeatable way to describe an architecture before I started building it. That became the **h00pz Architecture Specification Framework (HASF)**.

HASF formalizes a lot of the ideas described here: defining architecture before implementation, identifying ownership and seams, separating deterministic services from model inference, making failure states explicit, and establishing what "done" actually means before a model starts producing code.

There's quite a bit more to HASF than I can reasonably cover without turning this into a completely different article, so **HASF got [a post of its own](/p/introducing-hasf/)**, and the entire framework is <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/hasf.md" target="_blank" rel="noopener">reproduced in full in this site's repo</a> if you want the whole thing rather than the tour. For this discussion, the important point is that it grew out of the same realization: the quality of an AI application depends at least as much on the architecture surrounding the model as it does on the model itself.

## Atlas And PortfolioOS

Atlas and PortfolioOS solve completely different problems, but architecturally they have been converging on the same idea. PortfolioOS is becoming a collection of bounded financial systems and model workers operating around explicit state, while Atlas is becoming a collection of bounded personal productivity and knowledge systems operating around the same principles.

PortfolioOS has Market Intelligence (the subsystem responsible for maintaining the current market-cycle and risk posture), Hunt for discovering and researching investments, Portfolio Construction for assembling those investments into portfolios, and Loop for continuously reevaluating what the system already owns. Those subsystems can use models heavily without needing to become autonomous agents with unrestricted access to each other's internals.

Atlas has a very different set of concerns, but the same architectural idea applies. A model can understand a handwritten note, extract useful information from a meeting transcript, relate new knowledge to something that already exists, or determine that an item represents a task. None of those jobs require giving the model ownership of Atlas itself.

From the outside, both systems can still look highly agentic. PortfolioOS can discover something, investigate it, challenge an existing thesis, and eventually cause another part of the application to reconsider the portfolio. Atlas can receive a note, understand what it means, associate it with existing information, and make that knowledge available somewhere else later.

Inside, however, I increasingly want them to look like software. There are contracts, stores, workers, permissions, deterministic services, and explicit transitions between states. Most importantly, there are places where models are allowed to reason and places where they aren't.

That's the distinction I had been missing.

## Final Words

I started down this path trying to build better agents, but what I actually needed was better systems. I still think agents are incredibly useful, especially as a way to experiment with what models are capable of doing. Giving a model some tools and telling it to solve a problem is probably the fastest way we have ever had to prototype a new piece of software.

I just don't think that prototype is necessarily the architecture.

As Atlas and PortfolioOS have grown, I've found myself giving models less freedom rather than more. Their individual jobs are getting smaller while the systems around them are getting more capable, and oddly enough the applications feel more intelligent because of it. The model doesn't need to understand the entire system; it needs to understand the problem directly in front of it, while the system takes care of everything surrounding that problem.

That's the idea behind HASF, and increasingly the rule I use whenever I start designing an AI application:

**Stop building agents. Start building systems.**
