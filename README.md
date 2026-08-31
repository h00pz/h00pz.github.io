# The Rambling Thoughts of h00pz

Source for **[h00pz.github.io](https://h00pz.github.io/)** — a running essay series on how to actually build AI applications: bounding model inference inside real architecture instead of handing the whole system to an agent.

The argument runs on two real systems I build in the open:

- **PortfolioOS (pOS)** — a self-hosted financial system: market intelligence, research, portfolio construction, and ongoing maintenance, built around small, self-hosted models.
- **Atlas** — a personal-knowledge system built on the same principles.

The through-line: the model is a bounded component, not the architecture. Small models for sovereignty, explicit seams, persistent state the system owns, deterministic code around the probabilistic part, and failure treated as a first-class outcome.

## The series

Posts are grouped into three arcs (the site's categories):

- **Small Model Systems** — the foundational rules: stop building agents and start building systems, the model is not your architecture, seams, state, small-model boundaries.
- **AI Coding Scar Tissue** — what AI-assisted coding actually cost me, and the discipline (spec → plan → code, earned guardrails, a harness that enforces it) that got the time back.
- **AI Systems Engineering** — deep technical dives into pOS internals: the agent runtime, the deterministic sandwich, the model router, and the self-evolving Brain.

## `examples/`

Real artifacts referenced from the posts, linked as new-tab GitHub blob links rather than rendered pages: architecture specs and plans, the HASF and HADH documents, a prompt ConfigMap, and two full weekend-brief PDFs. If a post points at a file, it lives here.

## Build locally

Requires **Git**, **Go**, and **Hugo extended** ([install guide](https://gohugo.io/installation/)). The [Stack theme](https://github.com/CaiJimmy/hugo-theme-stack) loads as a Hugo module.

```bash
hugo server        # local preview at http://localhost:1313
hugo --gc --minify # production build into public/
```

Configuration lives in `config/_default/`. Posts are in `content/post/`, one page-bundle directory per post (`YYYY-MM-DD_slug/index.md` plus its cover image).

## Deploy

Pushing to `main` builds and deploys to GitHub Pages via GitHub Actions (`.github/workflows/`). No manual step.

## Colophon

Built with [Hugo](https://gohugo.io/) and the [Stack theme](https://github.com/CaiJimmy/hugo-theme-stack). Words and systems by h00pz. The posts are opinions from building real things, and they get revised when the things teach me something new.
