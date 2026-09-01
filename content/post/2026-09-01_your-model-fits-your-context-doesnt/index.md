---
title: "Your Model Fits. Your Context Doesn't."
slug: your-model-fits-your-context-doesnt
date: 2026-09-01
draft: false
description: "Advertised context is a model capability. In production it's an infrastructure budget you spend on memory, latency, and concurrency out of one finite card."
tags:
  - context-engineering
  - gpu
  - model-serving
  - openshift
  - slm
categories:
  - OpenShift and AI
image: your-model-fits-your-context-doesnt.png
---

The [last post](/p/how-big-is-a-model-really/) ended on a result that should have made me happy and instead made me suspicious: a 12B Gemma carrying more than two hundred thousand tokens of context on about 10 GB of a 24 GB card. My first instinct was to celebrate all that headroom and go fill it. My second, better instinct was to ask a question I'd been skipping for months. Not "how much context can this model hold," which I now had a generous answer to, but "how much context does my application actually need." Those turn out to be very different numbers, and the gap between them is where a surprising amount of GPU money goes to die.

This is the second post in the OpenShift-and-AI series, and it's about the thing that ambushed me after I'd solved the residency problem. Your model fits. Your context, once the application is done stuffing things into it, might not, and even when it does fit it can cost you more than you bargained for. Advertised context is sold as a model capability. In production it's an infrastructure budget, and you spend it whether you meant to or not.

## Maximum Context Is Not Useful Context

Here's where I'd been fooling myself. I wanted big context because I assumed my documents were big. When I actually measured the source material, they weren't. A typical short macro note ran about 2,100 to 2,700 tokens. Even a long analyst deep-dive came in around 11,500 to 14,000 tokens. A 14K document is not a long-context problem. A 32K model swallows it without noticing.

So where did the demand for 100K-plus context come from? Not the source. The *system*. The moment my application started doing its job, it wanted to put the document in front of the model alongside the relevant thesis history, the supporting and contradicting evidence, prior observations, the instructions, the schema, and enough reserved room for the model to actually answer. A 14K source becomes a 50K or 100K request once the surrounding system adds everything it thinks the model ought to know. Source length and application context length are not the same number, and it's the second one that sizes your GPU.

That splits "context window" into three things people say interchangeably and shouldn't. There's the **maximum** context, the number the model or runtime claims. There's the **sustainable** context, how much your serving config can actually carry without wrecking memory, latency, or concurrency. And there's the **useful** context, how much information you should actually put in front of the model, which is a different and usually smaller number again. The advertised max is a ceiling. What you can serve is a budget. What you should send is an architecture decision.

## Context Has a Bill

Every token of context you spend shows up on three separate invoices, and memory is only the first.

**Memory** is the one the last post covered: the KV cache grows with context length, and it grows again with every concurrent request, because each live sequence carries its own attention state. It's worth seeing that first invoice across models, on the one card that actually sets the limit. These are all GPU VRAM footprints on a 24 GB RTX 3090 (host RAM on the 64 GB nodes was never the binding resource, so it isn't the story). The `max-num-seqs` column is how many requests the server will handle at once, and it matters because those concurrent sequences compete with context for the same KV-cache memory:

| Model | Context | max-num-seqs | GPU VRAM | % of the 3090 |
| --- | ---: | ---: | ---: | ---: |
| Qwen3-14B (FP8) | 32K | 2 | ~21.0 GB | 88% |
| Qwen3-8B (FP8, YaRN) | 128K | 2 | ~21.3–21.6 GB | 89–90% |
| Gemma 4 12B (Q4-QAT) | 128K | 1 | ~9.7 GB | 40% |
| Gemma 4 12B (Q4-QAT) | 222K | 1 | ~10.2 GB | 43% |
| Gemma 4 26B (Q4_K_M) | 84K | 1 | ~19.25 GB | 80% |

Read the two ends of that. A 14B at a mere 32K and an 8B stretched to 128K both nearly fill the card, while a 12B runs past two hundred thousand tokens on less than half of it. Same 24 GB, wildly different amounts of context bought, and the parameter count pointing exactly the wrong way.

The 26B is the row that shows the other half of the lever. Its 84K is a fixed KV pool, and `max-num-seqs` decides how it gets shared: at two sequences each request gets about 42K, and to hand a single request the full 84K I dropped it to one sequence. The measured part is the satisfying bit. At that 84K pool the card reads about 19.25 GB of its 24, roughly 5 GB of headroom, and moving context around inside the pool costs almost nothing, because for this model the weights (around 15 GB) dominate and the KV cache is small: raising the per-request window from 32K to 42K moved VRAM by about a third of a gigabyte. That's the opposite shape from the Qwen rows above, where a smaller model was brushing the ceiling on a fatter KV footprint. Same card, and how big the context bill runs depends entirely on which model is spending it. That's the argument in the table: the model fits, and everything you care about, how much context and how many callers, is a negotiation over the one card's memory.

And if you're looking at that 12B sitting on 43 percent of the card at 222K and wondering why I didn't just keep climbing, that's exactly the right question, and it's the rest of this section. Memory stopped being the thing that runs out first. There's a stack of free VRAM there, and I don't spend it, because the next two invoices come due long before the gigabytes do.

**Latency** is the one that ambushes you even when memory says yes. Take the Gemma numbers from last time: it decoded at a healthy 65 to 86 tokens a second, but a 144K-token prefill, the work of reading the context before generating a single new token, took about 49.6 seconds. Prefill and decode are different latency domains. A model with great decode throughput can still feel glacial when every request opens by chewing through a hundred thousand tokens of context. Even when the card has the memory, the clock may not have the patience.

**Concurrency** is the one benchmarks hide, because I ran mine, correctly, at a parallelism of one to find the model's true behavior. But "one 144K request works" does not imply "ten 144K requests work." Ten of them mean ten live KV caches competing for the same VRAM, and the honest serving question stops being "does this checkpoint fit on a 24 GB card" and becomes "at the context lengths my application actually uses, how many concurrent requests can this model sustain on this hardware before latency or memory falls over." That's a far more useful question, and a much less flattering one.

This is why context stopped being "whatever fits" in my system and became a budget with line items. If the runtime allows 160K and I reserve 16K for the model's visible output, the input window is really about 144K. Take out instructions, system state, schemas, and retrieved authoritative material, and the source document gets whatever's left. Advertised context is a ceiling. Application context is an allocation problem, and pretending otherwise is how one rambling request eats the whole card. Every one of those numbers is individually reasonable, and it's the way they compose that decides whether the deployment holds, which is the same [locally-sensible, globally-wrong](/p/context-windows-are-not-architecture/) shape I keep running into, now measured in gigabytes.

## Capacity Is Not Comprehension

There's a failure this whole argument could accidentally imply, and I want to shut it down, because it's the most expensive misconception of all: that a bigger context window means better understanding. It doesn't, and I have the scar to prove it. In the same Qwen-versus-Gemma evaluation, [the Gold Trap](/p/the-gold-trap-small-models-are-not-interchangeable/), one model ingested a document perfectly, extracted every fact correctly, and then led with a stale recommendation because it missed the single sentence that superseded everything above it. It received 100 percent of the tokens. It understood which ones governed the others exactly not at all.

So there are two axes hiding inside "context," and infrastructure only owns one. There's context *capacity*, can the model physically receive the information, which is a memory-and-serving problem I can throw a bigger card or a better engine at. And there's context *competence*, can the model correctly reason about authority, supersession, and significance across everything it received, which no amount of VRAM will buy me. Everything in these two posts is about the first axis. The second one is judgment, and it stays exactly as hard as it was, which is the honest reason a human is still in the loop at all.

## Where OpenShift Enters

Line up what Darkpool actually converged on and it isn't "pick the biggest model that fits." It's models matched to jobs by capability and memory behavior: a 26B Gemma as the sovereign adjudicator where nuance and judgment matter, a 12B Gemma as the high-context compiler that turns big inputs into structured artifacts, and a utility card that cold-loads the smaller specialists, extraction, embeddings, speech, and vision, on demand. Different kinds of work, different residency profiles, different points on the capacity-and-competence tradeoff.

And the moment you have several models and a finite fleet of cards, model selection has quietly turned into resource scheduling. Which model lives on which node. Which ones are latency-sensitive enough to stay resident and which can be warm-loaded on demand, so a utility node can keep an embedding model always-on while rotating a vision or transcription model in only when something needs it. GPU memory stops being a static capacity number and becomes a schedulable resource over time. Model placement is workload placement. Residency, affinity, startup time, throughput, isolation, and utilization are all suddenly platform questions, and none of them are things a transformer knows anything about.

That's the handoff. I started this whole exercise asking which model I could fit on a GPU. I ended it asking which combination of models, contexts, runtimes, and workloads I could operate on a cluster, and that is not a model-selection problem anymore. It's a platform problem, which is the entire reason this runs on OpenShift and not on a laptop under my desk. The hard part of that platform problem, the queues and the backpressure and the GPU deadlocks and the out-of-memory kills that happen when several of these models fight over three cards, is the subject of the posts after this one. These first two only had to make one point between them, and it took a cluster to learn it: your model fitting in VRAM tells you almost nothing about whether your application fits in VRAM.
