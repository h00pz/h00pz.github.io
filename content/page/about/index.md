---
title: About
menu:
    main:
        weight: 1
        params:
            icon: user
comments: false
---

I'm Mark Hooper. Online, and on this blog, I go by **h00pz**. The name is older than any of this. Day one at Brak Systems I showed up as the second Mark in the room, and with a last name like Hooper the jump to Hoopz was short. My dad answered to the same nickname, so I came by it honestly.

I'm a Principal Solution Architect at Red Hat, based in Chicago, and I spent a couple of decades in security and infrastructure getting here, holding the certifications that come with that life (CISSP, CISA, CISM, CCSP) and, more usefully, collecting the scar tissue those letters don't mention. My work lives in the Kubernetes and OpenShift world, which is not an accident you'll fail to notice reading this blog. When I reach for a way to run AI work reliably, I keep reaching for the reconciliation loop, because it's what my hands already know.

## Why this blog exists

The same mistake keeps finding me everywhere I work. Someone puts the most exciting, fastest-moving thing in the middle, a model, a shiny tool, an agent, a clever bit of automation, and lets the whole system grow outward from it. It feels great, right up until the thing in the middle changes and takes the architecture with it. This blog is the long argument for the opposite: keep the volatile thing bounded, and put the durable engineering around it. That's as true of an OpenShift platform or an Ansible run as it is of a language model, and over time the writing here widens to cover all of it.

It started with two systems I build for myself. **PortfolioOS**, or pOS, is a self-hosted financial system: it reads the world, holds what I believe about it, and helps me run my own money without a bank deciding how. **Atlas** is the same ideas pointed at personal knowledge instead of markets. Both run on small models I host myself, on purpose, for sovereignty, because I'd rather own the whole stack than rent it from a vendor whose pricing, terms, and availability I don't control. They're where a lot of the scar tissue in these posts came from, and the running examples I reach for most, but the instincts aren't financial, and they aren't even AI-specific. They're the same ones I bring to the Kubernetes, OpenShift, and automation work I do the rest of the time.

Neither of those two is open source, and there's no public repository for their code. What I share of them here is the architecture and the reasoning behind it, along with real artifacts pulled straight out of the systems, a spec, a plan, a config, a full weekend brief, a chunk of the actual code, reproduced in a post when it makes a point better than prose would. The source of pOS and Atlas stays private; the thinking, and the pieces that carry it, don't. The OpenShift and automation work is a different story, and some of it will likely land here as real, public repos you can actually clone.

pOS started somewhere less tidy than an architecture diagram. For a while I wrote a market letter for a few friends, a running argument with myself about where the world was heading, and the writing wasn't the hard part. The hard part was the reading, the endless hunting for the handful of things that actually bore on what I believed, and eventually it got too heavy and the letter stopped. Around the same time I looked at what a family office costs to buy off the shelf and decided I'd rather build the apparatus than rent it. So pOS is that bet: my own home office, my own market letter, except written by a system I can actually trust to be honest about what it doesn't know.

## What you'll find here

The blog is one long argument, made in pieces: the model is a bounded component, not the architecture. Small models with explicit seams, state the system owns rather than the model remembers, deterministic code wrapped around the probabilistic part, and failure treated as a first-class outcome instead of a surprise. Some of it is theory. Most of it is me being wrong in a specific, expensive way and writing down what it taught me. Right now most of that argument is made in AI, because that's where I've been living; the OpenShift and automation versions of it are on the way.

Everything here is an opinion from building real things, and it gets revised when the real things teach me something new. If a post argues with a post I wrote six months ago, that's the system working, not a bug.

The views on this blog are my own. They don't represent Red Hat, and nothing here is written on their behalf.

You can find me on [GitHub](https://github.com/h00pz) and [LinkedIn](https://www.linkedin.com/in/mark-hooper-8837b64/), or by email at [mh@h00pz.co](mailto:mh@h00pz.co) for anything about this blog, or [mhooper@redhat.com](mailto:mhooper@redhat.com) for work.
