---
title: "The Router Translates Nothing"
slug: the-router-translates-nothing
date: 2026-08-05
draft: true
description: "I run my coding agents on Opus and GLM at once, behind one URL, through a proxy that does the single job I needed and refuses every clever job I didn't."
tags:
  - ai
  - architecture
  - systems
  - agents
categories:
  - AI Systems Engineering
image: the-router-translates-nothing.png
---

I run my coding agents on two different models at the same time. The main session, the one that [holds the coordination and the judgment](/p/subagents-cheap-coordination-expensive/), runs on Opus. The bounded subagents that write the code run on GLM, which is cheaper and faster and perfectly good at execution inside a packet. And the tool orchestrating all of it, Claude Code, has no idea any of this is happening. As far as it can tell, it is talking to Anthropic, over one URL, the way it always does.

There's a proxy in the middle making that true, and it is one of my favorite things I've built precisely because it is so aggressively unambitious. It is about two hundred lines. It does the one job I actually needed a router to do and it refuses, on purpose, every clever thing a router is tempted to become. This post is about why refusing was the whole design.

## What a Model Router Wants to Be

Say "model router" to anyone and the ideas start piling up immediately. It should translate between provider APIs so you can hit OpenAI and Anthropic and Google through one interface. It should load-balance across providers, retry on failure, cache identical requests, maybe pick the cheapest model that can handle a given prompt, maybe fall back to a smaller model under load. Every one of those is a real feature that a real product ships, and every one of them has the same property: it puts the router in the hot path of every single token, making decisions, holding state, translating formats. That's a lot of surface for a thing that sits between me and every model call I make.

I wanted none of it. Not because those features are bad, but because I already knew what I needed, and it turned out to be almost nothing.

## What Mine Actually Does

Claude Code points at one base URL. Every request arrives as a native Anthropic Messages call. The router reads the model, looks it up in a table, and forwards the request to one of three places: my Anthropic Max account, my OpenRouter account, or z.ai for the GLM models. It rewrites the model id to whatever that upstream calls it, and it changes nothing else about the body. That's the whole router.

The reason it can get away with changing nothing else is the one fact the entire design rests on: all three upstreams speak native Anthropic. Anthropic obviously does. OpenRouter offers an Anthropic-shaped endpoint. z.ai offers an Anthropic-shaped endpoint that passes thinking blocks and tool use straight through. So there is no translation to do, because everyone already agreed to speak the same protocol. The router isn't a translator. It's a credential-and-host swapper keyed on the model, and once you see it that way the code gets very small.

The routing table is a literal allowlist:

```typescript
const ALIASES = {
  "anthropic/claude-opus-4.8": { route: "anthropic", model: "claude-opus-4-8" },
  "z-ai/glm-4.6":              { route: "zai",       model: "glm-4.6" },
  // ...native ids pass through to the anthropic route too
};
```

And resolving a model against it is exactly as dumb as it should be, which is to say it's a lookup with no cleverness anywhere in it:

```typescript
export function resolve(model: unknown, table: AliasTable): AliasEntry | null {
  if (typeof model !== "string" || model.length === 0) return null;
  return Object.prototype.hasOwnProperty.call(table, model) ? table[model] : null;
}
```

There is no fuzzy matching, no nearest-neighbor, no default. If a model isn't in the table, `resolve` returns null and the request is rejected with a 400 before any upstream is called. This is the same discipline as [the capability grant from the last post](/p/the-agentic-worker/): the set of things you're allowed to reach is an explicit allowlist, and a name that isn't on it doesn't get a helpful guess, it gets a refusal. A router that fuzzy-matches an unknown model to a "close enough" one is a router that will one day route your expensive request somewhere you didn't intend.

## How Claude Code Gets Pointed At It

The integration with Claude Code is four environment variables, set by the launcher that starts every session. It walks up to the nearest `harness.lock`, reads the router URL out of it, and exports:

```bash
export ANTHROPIC_BASE_URL="$ROUTER_URL"
export ANTHROPIC_CUSTOM_HEADERS="x-hadh-router-token: $TOKEN"
export ANTHROPIC_MODEL="anthropic/claude-opus-4.8"       # the main session
export ANTHROPIC_SMALL_FAST_MODEL="z-ai/glm-4.6"          # the background + subagents
```

That's the entire wiring. `ANTHROPIC_BASE_URL` sends every call to the router instead of to Anthropic, the custom header carries the token that gates the proxy, and the two model variables are the whole trick. Claude Code uses `ANTHROPIC_MODEL` for the main session and `ANTHROPIC_SMALL_FAST_MODEL` for its cheap, fast work, so setting the first to an Opus alias and the second to a GLM alias is all it takes to put the coordination on the expensive model and the [bounded execution on the cheap one](/p/subagents-cheap-coordination-expensive/). Claude Code never learns it's addressing a proxy, or that two different providers are answering. It sets two model names and makes ordinary HTTP calls, and the router turns those two names into two accounts.

## The Fifteen Lines That Actually Matter

If the routing is dumb on purpose, the credential handling is where all the care went, because that's the part where a mistake leaks a key. The router touches three different accounts' credentials, and the entire job of the header code is to make sure they never mix. It's a whitelist: a header the router doesn't explicitly copy is dropped, so nothing leaks across a route by accident.

```typescript
export function buildUpstreamHeaders(route, clientHeaders, config) {
  const h = {};
  for (const name of PROTOCOL_HEADERS) {           // version, beta, content-type, accept
    if (typeof clientHeaders[name] === "string") h[name] = clientHeaders[name];
  }
  if (route === "anthropic") {
    // pass the client's own credential straight through — Max OAuth.
    // the router adds nothing and stores nothing.
    if (clientHeaders["authorization"]) h["authorization"] = clientHeaders["authorization"];
    if (clientHeaders["x-api-key"])     h["x-api-key"]     = clientHeaders["x-api-key"];
  } else if (route === "zai") {
    h["x-api-key"] = config.zaiApiKey;             // drop client auth; inject the router's z.ai key
  } else {
    h["authorization"] = `Bearer ${config.openrouterApiKey}`; // drop client auth; inject the router's OpenRouter key
  }
  return h;
}
```

Read what each branch does with credentials, because that's the security model in one function. On the Anthropic route, the client's own authorization is passed straight through, which means my Anthropic Max OAuth token goes to Anthropic and nowhere else, and the router never stores it, never logs it, never sees a reason to hold it. On the other two routes, the client's credential is dropped entirely and the router injects its own provider key, the one that lives in a Kubernetes Secret and reaches only that provider. And the router's own access token, the one that gates the proxy itself, is never in this list at all, so it's never forwarded to any upstream.

That whitelist is the whole reason I trust a shared proxy with three accounts' credentials. A key for one provider can only ever be attached to that provider's route. My Anthropic OAuth is never held by the thing that talks to z.ai. The blast radius of any one credential is exactly one upstream, enforced by the fact that the code copies headers by name and drops everything it wasn't told to keep.

The proxy is gated too. Every request has to carry the router's access token or it gets a 401 before anything else happens, so the thing isn't an open relay to my paid accounts sitting on a cluster. And the body rewrite is the only change the router makes to the request at all: read the model, swap it for the upstream's id, forward the bytes. Everything else about the request is the client's, untouched.

## Why Dumb Was the Point

Line it all up and the router is a lookup, a header whitelist, a token check, and a one-field body rewrite. That's it. And every feature I listed at the top, the translation and the caching and the load-balancing and the fallback, is a thing I deliberately left out, because each one would have moved the router from the edge of my system into the middle of it. A translator has to understand every message it forwards. A cache has to hold requests and responses. A load-balancer has to track health and make choices. All of them turn a dumb pipe into a stateful, decision-making component sitting in the hot path of every token, which is the last place I want a component that can be wrong.

By refusing all of it, the router stays a thing I can hold in my head and reason about completely. It has one job, credential-isolated routing, and its correctness is checkable by reading a hundred lines. The intelligence isn't in what it does. It's in the two things it refuses to do: guess at a model it doesn't recognize, and let a credential touch a route it wasn't scoped to. Everything else, it gets out of the way of.

## Where the Memory Actually Goes

The router is boring and reliable for one reason above all the others: it doesn't run a single model. It hands every request to a provider who runs the model for me, and that offload is the entire source of its calm. I know exactly how much of the hard part I exported, because I also self-host, and the self-hosted side is where all the memory pain the router doesn't have actually lives.

pOS runs its own inference for the [nuance model the agentic worker leans on](/p/the-agentic-worker/), a twenty-six-billion-parameter Gemma on a GPU in my own cluster, and it has taught me every lesson the cloud router lets me skip. That model server runs a single inference slot, so one long thinking-heavy turn will decode twenty-six thousand tokens over three minutes at a hundred-odd tokens a second, and while it does, every other request queues behind it or trips its own timeout and aborts with a flat `this operation was aborted`. I once set a monitoring sweep to fire every sixty seconds, each sweep making a model call for every position in the book, and the sweeps took longer than a minute to finish, so they overlapped and piled onto that single slot until the model was answering roughly five thousand seven hundred requests with `transport error: fetch failed`. It recovered about twenty seconds after I backed the interval off and the load drained. A rolling update once deadlocked outright because the new pod needed a GPU that wouldn't free until the old pod died, and the old pod wouldn't die until the new one was ready, on a cluster whose one spare GPU sat on a node with too little CPU to take it. And a deploy died silently in the middle of a build, at step thirty-two of fifty, no error in the log, the specific kind of quiet exit that is almost always the kernel reaching in and killing the process because the machine ran out of memory.

Not one of those can happen to the router, because the router holds no model in memory, schedules no GPU, and decodes no tokens. It looks up an alias and copies some headers. Every hard, memory-shaped failure I just listed belongs to whoever runs the model, and for the coding agents I decided, on purpose, that whoever should not be me. That's the real reason the router gets to be two hundred boring lines. It exports the entire difficult half of the job, and the difficult half is precisely the half that runs out of memory.

## What the Boring-ness Is Borrowed From

I want to be honest about where this elegance actually comes from, because it isn't mine. The router translates nothing only because three separate providers decided, independently, to offer an Anthropic-shaped endpoint. That's the load-bearing assumption under the whole design, and I don't control it. The day a model I want lives behind an API that only speaks its own dialect, the credential-and-host swapper stops being enough, and I have to build the exact translation layer I've spent this whole post being smug about avoiding. The boring router works because it's standing on a protocol convergence that happened to hold, and conveniences that depend on other people's choices are conveniences you're renting.

And it is, undeniably, a single point of failure. Every model call I make flows through one small proxy on one cluster, and if it's down, all my agents are down. I've decided that trade is worth it, and the reason is the same as the reason it's boring: the less a component does, the less there is to break at the one spot everything depends on. A hundred lines that look up a model and copy some headers is about the most reliable thing I know how to put in a hot path. If I'd given it all the features it wanted, the single point of failure would still be there, and it would be a great deal harder to trust. I made the thing in the middle boring precisely because it's in the middle. That's not a limitation I settled for. It's the design.
