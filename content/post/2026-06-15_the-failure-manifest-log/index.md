---
title: "The Failure Manifest Log"
slug: the-failure-manifest-log
date: 2026-06-15
draft: false
description: "Most projects fix a failure and move on, which loses the reason a rule exists. The Failure Manifest Log keeps every constraint attached to the observed failure that created it."
tags:
  - ai
  - architecture
  - hasf
  - systems
  - state
categories:
  - AI Scar Tissue
image: cover.png
---

Most software fixes a failure and moves on. Something breaks, someone diagnoses it, a change goes in, and the incident is closed. The fix survives in the code, and the reason behind it starts evaporating the moment the ticket is marked done. Six months later the constraint is still there and the story is gone, and all that remains is a rule nobody can quite explain.

An earlier post in this series called that rot, and blamed it for a large part of what made PortfolioOS v2 unmaintainable. Rules that had been added for real reasons outlived the memory of those reasons, and a rule whose reason has been forgotten can't be defended or safely removed. It just sits there, half-superstition, until someone deletes it because it was inconvenient or routes around it because they couldn't see why it mattered. The failure isn't that we fix things. The failure is that we throw away the only record of why the fix was necessary.

This post is about the mechanism I use to stop doing that. On paper it has a perfectly dignified name, the Feature Memory Ledger, and a perfectly sensible job: it's how I keep track of all the work my coding agents and their subagents do, every capability they build, which one built it, and why.

The acronym, though, is FML, and nobody on earth reads FML as Feature Memory Ledger. They read it as fuck my life, and honestly they're right to, because a ledger where every entry opens with something that broke is a running log of exactly that feeling. The dignified name was supposed to win. It never stood a chance. That's the rule with dark names: the one that's honest about the pain is always more memorable than the sanitized version, so it wins, and once it wins it's canon forever. I've made my peace with it and settled on the Failure Manifest Log, which is at least a version of FML I can put in a blog title.

## The Reason Is the Part That Rots

It's worth being precise about what actually gets lost, because it isn't the fix. The fix is in the diff, permanently, and anyone can see what changed. What disappears is the connection between the change and the failure that motivated it, and that connection is the only thing that lets a future reader judge whether the constraint still earns its place.

There's an old programmer's joke that captures the end state better than any diagram I could draw. It's a source comment that has been passed around for years:

> When I wrote this code, only God and I knew how it worked. Now, only God knows.

It's funny because everyone has met that code, and underneath the joke it's a story about a reason that rotted all the way down to nothing. Whoever wrote it understood exactly why it was shaped that way, the understanding lived only in their head, and the moment they moved on the why went with them. Some versions of the comment even keep a running tally of the hours the next person wasted trying to change it, which is about the closest a codebase ever comes to admitting the cost of that lost reason out loud. The FML exists so that comment can't be true, because the why never lived only in someone's head in the first place.

Without that connection, every rule looks the same. A guardrail that prevents a catastrophe that happened twice looks identical, in the code, to a guardrail someone added because they were nervous one afternoon. You can't tell the load-bearing constraints from the anxious ones, so you treat them all as equally sacred or equally negotiable, and both of those are wrong. The reason is what carries the weight, and the reason is exactly what a normal fix-and-move-on workflow doesn't preserve.

## A Ledger That Opens With the Failure

The FML inverts the usual order of recording. Instead of writing down what was built and hoping the motivation is remembered, each entry opens with the concrete need or failure that justifies its existence, and the work is described afterward as the response to it. The need statement isn't a summary written at the end. It's the first thing on the page, and it is supposed to be produced as a by-product of noticing the failure, not reconstructed from memory later.

These need statements are deliberately specific, because a specific failure constrains and a vague one doesn't. They read like real incidents rather than categories. One entry opens on the fact that the tax seat couldn't argue for three quarters because realized-gain data was never wired, so the plan was set three times with no tax argument at all. Another opens on subjects that had waited on leverage data for four months. The point of writing the need this way is that the justification travels with the record forever. A future reader doesn't have to trust that the constraint was sensible. They can read the exact hole it was covering, and decide for themselves whether the hole is still there.

Here is one of those pages, reproduced close to how it actually sits in the repo. Notice that the need comes first, and the contract, the status, and the acceptance all hang off it rather than the other way around:

```text
# The demand seam — four customers, one record, and an honest answer

Canonical FML ID: demand-intake  ·  Sequence: FML-102
Lifecycle status: woven  ·  As-built: ✅ live  ·  Dependency health: clear
Altitude: feature  ·  Owner: operator

## Intent
- Operator need: Eight of a hundred and thirty-one position winds are
  instrumented, and almost every instrumented one is a tailwind. Nobody ever
  asked collection for the rest, because there was no way to ask - so the gaps
  were invisible rather than declined.
- Governing question: How does a lane say what it needs measured, and how does
  it find out whether it can have it?
- Why it matters: Collection's job is set by its customers, which is why this
  intake is the one endpoint deliberately open to every lane. And it never says
  whether the wind is a good one - the lane that owns the assumptions owns that.

## Architecture weaving & delivery
- Weaving state: baked 2026-07-31 as wave 13.
- Acceptance evidence: A demand from each of the four customers returns served,
  proxied or gap per instrument, with a cause on every gap.
```

The title is a claim about what the thing is for, the operator need is the specific hole it fills, and the acceptance evidence is what has to be true against the running system before it's allowed to call itself live. An agent that picks up this page a year from now doesn't have to guess why the demand seam exists. The page tells it, in the same breath as it tells it what to build.

That excerpt is just the top of the page. The whole thing, with its dependency edges and the decision history that records the exact moment this item went from built to proven-live on the running cluster, lives as a plain file in this site's repo: <a href="https://github.com/h00pz/h00pz.github.io/blob/main/examples/example-fml-demand-intake.md" target="_blank" rel="noopener">Example FML: the demand seam</a>.

That's the whole idea in one sentence. The failure and the fix live in the same record, permanently attached, so the reason can never quietly detach from the rule.

## The Detail Page Owns the Truth

For a ledger like this to stay honest, it has to be clear which copy of anything is the real one, because the moment two versions of a fact exist they begin to drift. The FML resolves this the same way the rest of the framework resolves it, with a single declared owner per concern. Each item's own detail page owns its truth. The ledger index and the deployment order are derived projections of those pages, and if a projection ever disagrees with a detail page, the detail page wins and the projection is regenerated.

This matters more than it sounds, because the tempting thing with a record like this is to maintain a nice summary table by hand and let it fall out of sync with the underlying entries. The FML forbids that by making the summaries generated artifacts that are never edited directly. You change the record, and the index and the order recompute from it. There's one place the truth lives, and everything else is a view, which is the same principle that keeps two data stores from both believing they're canonical.

## Design Maturity Is Not Deployed Reality

The most useful distinction the FML draws is between how finished a piece of work is in design and whether it actually exists in production, because those are different questions and conflating them is how a project lies to itself. Each item carries a deployed axis, with honest values like live, partial, merged, code-complete but not yet deployed, and pending, and that axis is kept strictly separate from the item's design maturity and its intended release. The deployment order keys on what is actually deployed, never on how mature the design happens to be.

This means the ledger can hold, without contradiction, an item whose design is complete and whose deployed state is nothing, and it can say so plainly rather than rounding a finished design up to a finished feature. That gap between the design and the reality isn't an embarrassment to be hidden. It's exactly the information you most need, and the next post in this series is entirely about why keeping desired architecture and as-built reality separate is worth the discipline it costs.

I can point at what this looks like in practice, because the ledger for the current system tells me, as I write this, that 245 of 405 declared features are actually deployed. That's sixty percent, and the number is deliberately unflattering, because the ledger refuses to count anything it hasn't watched run. There's a sharper rule sitting underneath it, too: this is a clean rebuild, so progress started at zero, and a feature that existed in the old version earns no credit at all. The old code is a harvest source, not a head-start. A ledger that let the mere existence of v2 quietly inflate v3's progress would be lying in exactly the way the whole thing was built to prevent.

## "Live" Is an Evidence Claim, Not a Status

The rule I find most bracing is the one governing when an item is allowed to be called live. In this ledger, live is an evidence claim rather than a status, which means an item is live only once its acceptance has been proven against the actually running system, through a real read against the deployed API and the real store, with the command and its real output recorded in the item's history. A green test suite doesn't make anything live, because a test that shares the code's assumptions will happily agree with the code and disagree with reality.

An item that is built and merged but whose behavior has never been proven in the running system stays in an honest built or merged state, and refuses to call itself live. That refusal is the whole point. It would be easy, and comforting, to let a passing test promote something to live, and it would also be a small fabrication of completeness, which the framework treats as worse than an honest gap. The ledger would rather admit that a thing is built but unproven than claim a liveness that nobody actually demonstrated.

## The Order Learns

A record like this would be nearly useless if it were written once and left to age, because the whole problem it solves is the passage of time. So the deployment order the FML produces is a living projection rather than a fixed plan. After every item is genuinely implemented, and before the next one is selected, the process reconciles that item's record with what implementation actually revealed, adds or flips every dependency edge that turned out to be real, reviews the items that depended on it, and regenerates the whole order.

Tiers move, merge, split, and disappear as the architecture learns, and even an order that comes out unchanged has to record that it was recalculated. This is what keeps the ledger honest against reality rather than against its own past assumptions. It isn't a monument to a plan. It's a record that updates itself every time the system teaches it something new, which is the only kind of record that survives contact with a real project.

## Why Not Just Use Jira?

When I explain the FML, the reasonable question is why I built a ledger at all instead of using a real project tracker. I've used Jira. I'm not in a hurry to relive it. But the honest reason isn't that Jira is unpleasant, it's that Jira is in the wrong place and speaks the wrong language for the thing actually doing the work here, which is a fleet of coding agents and their subagents.

Start with location. My agents don't have a Jira login, and I don't want them to have one. They live in the repository, and the only truth they can cheaply read, diff, and regenerate is the truth that lives in the repository with them. The FML is plain text, generated from a Python file, tracked in git, and reviewed in pull requests, so an agent can read the current state, propose a change to it, and have that change land through the exact same process as a code change. A ticket behind a web UI and an API token is a place an agent has to be taught to reach, remember to update, and be trusted to update honestly, and every one of those is a seam I'd rather not build.

Then there's what "done" means. In Jira, done is a human dragging a card, or an automation dragging it for them, and it's a claim. The FML refuses to let done be a claim. Its live state is an evidence claim, proven against the running system with the command and its output recorded, the way I described earlier. A tracker whose statuses are asserted rather than proven would smuggle back in the exact lie the ledger exists to prevent, the one that says shipped when it's merely written.

And there's the shape of the plan. Jira gives you a board and a backlog; the FML gives you a deployment order that's a living projection, recomputed from typed dependency edges every time an item actually lands. After each agent finishes a piece of work the order regenerates, tiers move, and newly discovered dependencies flip. That isn't a workflow you run by hand in a ticket system. It's something you generate from a machine-readable record, which is one more reason the record has to be code the agents can regenerate rather than rows in someone else's database.

Underneath all of it is the real point, and it's the reason the dignified name is Feature Memory Ledger. A coding agent doesn't remember. It finishes a task, the session ends, and whatever it understood about what it built leaves with it. If I run several agents and their subagents against this system, and I do, then the only thing that knows the whole story, what's been built, by which agent, against which need, and whether it actually runs, is a durable record that sits outside all of them. Jira could hold a list of intentions. It couldn't be the shared, queryable, git-tracked memory that keeps a room full of forgetful agents from stepping on each other, which is the entire job.

Here's a slice of what the generated ledger actually looks like, straight out of the repo. I'm including it so it's clear this isn't a diagram of a nice idea:

```text
| Subsystem        | Implemented | Progress            | Live | Pending |
|------------------|-------------|---------------------|------|---------|
| pos-collection   | 34 of 41    | ████████████░░ 83%  | 34   | 6       |
| pos-brain        | 32 of 43    | ██████████░░░░ 74%  | 32   | 9       |
| pos-hunt         | 24 of 33    | ██████████░░░░ 73%  | 23   | 1       |
| pos-home-office  | 7 of 30     | ███░░░░░░░░░░░ 23%  | 7    | 16      |
| pos-aep          | 11 of 38    | ████░░░░░░░░░░ 29%  | 11   | 25      |
| All subsystems   | 245 of 405  | ████████░░░░░░ 60%  |      |         |
```

Every row there was written by the agents doing the work, and every "live" was proven, or is honestly still waiting to be proven, against the running system. That's a memory Jira was never going to keep for me.

## Why This Beats a Changelog

A changelog records what changed. An architecture decision record, at its best, records why a decision was made at a point in time. The FML is trying to do something neither of those quite does, which is to keep the failure, the constraint, and the current truth of the system in one living record, so that the reason a rule exists is never separated from the rule and never allowed to drift from reality.

The reason I care about this so much is that the alternative is the exact failure this whole phase of the series is about. A system accumulates constraints, the constraints lose their reasons, the reasons can't be reconstructed, and eventually nobody can tell the necessary rules from the anxious ones. The Failure Manifest Log is the discipline that refuses to let that happen. Every rule opens with the wreck it was built from, the truth lives in one owned place, liveness has to be earned against the running system, and the order relearns itself as the project goes. It is, in the end, just a way of making the system remember why, which turns out to be the hardest thing for any system to keep.
