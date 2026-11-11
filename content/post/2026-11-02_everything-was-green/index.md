---
title: "Everything Was Green"
slug: everything-was-green
date: 2026-11-02
draft: false
description: "I couldn't log into my own cluster, and every operator swore it was healthy. The one that wasn't had been dead for ten days, quietly letting a certificate reach an expiry it was the operator's whole job to prevent."
tags:
  - openshift
  - observability
  - aiops
  - infrastructure
  - guardrails
categories:
  - OpenShift and AI
image: everything-was-green.png
---

I tried to log into the Darkpool console and the page started flashing. Login screen, then the dashboard for a quarter of a second, then back to the login screen, over and over, fast enough that it looked like a strobe. I did the thing you do. I cleared cookies, I tried a different browser, I blamed the browser. Then I did the slightly more serious thing and told the agent on the box to delete the console pods, because a console that loops is a console problem, and rolling the pods is free.

It was not a console problem. The console came back on fresh pods and looped exactly the same way, which is the cluster's polite way of telling you that you are looking at the wrong layer.

So I went and read the logs, and the first surprise was that the login was *working*.

## OAuth succeeds, then the token is garbage

The console log said `oauth success, redirecting`, and then, a few milliseconds later, it said it couldn't get the list of API groups because `the server has asked for the client to provide credentials`. Those two lines are not supposed to sit next to each other. The first one means the whole OAuth dance finished, the identity provider was happy, a token was minted and handed back. The second one means that when the console turned around and used that freshly minted token against the API server, the API server treated it like a stranger off the street.

The API server's own log was blunter. `invalid bearer token`. It had been handed a token it had just caused to be issued, and it rejected it.

A token that is valid at issue and invalid one hop later is not a token problem, it is a *validation* problem, and in OpenShift that distinction has an address. When you hand the kube-apiserver an OAuth bearer token, it does not verify the token by itself. It turns around and asks the OAuth API server "is this real, and who is it," and it authenticates *that* question with a client certificate of its own. If the API server can't make that call, it can't answer the question, and a token it can't vouch for is a token it rejects. Every time. For everyone.

So I read the OAuth API server's log, and there it was, the same line thousands of times:

```
x509: certificate has expired or is not yet valid:
current time 2026-11-02T...Z is after 2026-10-31T12:20:07Z
```

## A certificate that expired on schedule

The certificate the kube-apiserver uses to ask that question is called `webhook-authenticator`. Its subject is `system:serviceaccount:openshift-oauth-apiserver:openshift-authenticator`, which is a long way of saying "the thing allowed to ask the OAuth server who a token belongs to." It expired on October 31st at 12:20:07 in the afternoon, UTC, and it is now November 2nd. It worked yesterday, the way everything works right up until a date it was always going to hit.

That is the part worth sitting with. This was not a crash, a bad deploy, a cosmic ray, or a config I fat-fingered. The outage had a timestamp, and the timestamp was set a month before the outage happened. Somewhere around the end of September a certificate was minted with thirty-ish days of life in it, and the clock started, and on October 31st at 12:20:07 the clock ran out, and a few hours of grace later nobody could log in. The failure was scheduled. I just wasn't the one who scheduled it.

Certificates like this are not supposed to be a thing a human thinks about, and that is the entire point of them. They rotate. Something notices one is getting old, mints a fresh one, and swaps it in with weeks to spare, and you never learn the certificate exists because you never have to. The machinery that does that noticing, for this particular certificate, is the `kube-apiserver-operator`.

## The thing that rotates the keys had been dead for ten days

I looked at the operator. It was in `CrashLoopBackOff`. It had restarted something north of two thousand times, and the kubelet had logged the back-off event roughly sixty-nine thousand times over *ten days*. This thing had not run successfully since before the certificate it was responsible for had even started looking old.

The crash itself was almost funny:

```
F cmd.go:182] open /var/run/secrets/kubernetes.io/serviceaccount/token: permission denied
```

The operator could not read its own identity. Every pod in the cluster gets a service-account token projected into it at a known path, and this is how a pod proves to the API server that it is who it says it is. The operator's copy of that file, on one node, had become unreadable to the operator. It would start, reach for its own name, be told it wasn't allowed to have it, and die. Start, reach, die, sixty-nine thousand times, for ten days, on a node called `logan`.

I want to be precise about the blast radius, because it was small and specific and that is the interesting part. It was not the node. Nothing else on `logan` had this problem. It was one stuck projected-token mount on one pod that had been alive for a hundred and twenty-two days, long enough for whatever refreshes those mounts to have gone wrong once and never recovered for that one pod. The fix, once I understood it, was embarrassingly cheap. I deleted the pod. It rescheduled onto `deadpool`, read its own name without complaint, and came up healthy on the first try with zero restarts.

## A dead operator is the one component that can't report itself

Here is the part I got wrong, and it is not the part where I rolled the console pods. That was a cheap wrong guess and it cost me a minute.

The part I got wrong is that I trusted the color. When this started, I ran `oc get co`, the list of every cluster operator and its health, and it was a wall of green. Authentication: available, not degraded. Kube-apiserver: available, not degraded. Thirty-odd operators all calmly reporting that they were fine, while I sat there unable to log in. I half-believed them. I spent real minutes looking at the OAuth routers and the identity provider and the ingress path, at everything *except* the caretaker, because the caretaker's own line on the status board was green.

But that status is not an observation. It is an *assertion*, and the operator is the one asserting it. The green next to `kube-apiserver-operator` did not mean "I checked, and I am healthy." It meant "the last time I was alive enough to speak, I said I was fine." A process that is crash-looping does not get to the part of its loop where it updates its own status. It dies at `open token: permission denied`, long before it reaches "and here is my current health." So the last word it managed to say just stands there, indefinitely, looking exactly like a fresh answer. The board was not lying. It was quoting a dead man.

I've written this same lesson before from the other side of the stack. A while back I spent weeks convinced [the model was flaky](/p/the-model-was-fine/), because my agents kept coming back empty, and the truth was that I was killing the GPU myself and the dashboard was cheerfully green the whole time because nothing was wired to notice. Same shape. The thing that was broken was upstream of the thing that reports, so the report had nothing to report and said so by saying nothing. Green is the absence of a complaint. It is not the presence of health, and the day those two come apart is the day you find out which one your monitoring actually measures.

This is the write-path problem again, and I keep [finding it everywhere](/p/everything-is-a-write-path/). Writing down "I am healthy" is easy and an operator does it constantly. *Reading* whether a token actually validates, end to end, through the real path a user takes, is the hard half, and it is the half I did not have. The cluster could assert its health all day. Nobody, including me, was checking it against the world.

## What it cost, and what's still open

The repair, once the operator was alive, was almost anticlimactic. I deleted the expired `webhook-authenticator` secret, and the now-healthy operator did the thing it had been unable to do for ten days. It minted a fresh certificate, signed by the current signer, good through the middle of the month. Then it rolled the kube-apiserver across all three masters, `blade`, `deadpool`, and `logan`, one at a time, revision 50 to revision 51, each one picking up the new certificate as it came back. When the last one landed I read the logs again, and the `certificate has expired` lines had stopped, and the `invalid bearer token` lines had stopped, and I could log in. The whole thing, from flashing screen to fixed, was about an hour, and most of that hour was me learning the shape of a problem that took four commands to undo.

Three things are still wrong, and I'd rather write them down than let the green board tell me they're fine.

The first is that I still don't know *why* that one mount broke on `logan`. I know it was isolated, I know rescheduling dodged it, and I know that if the operator ever lands back on `logan` and hits the same bug, it dies again and the certificates quietly stop rotating again, and I don't find out until the next expiry detonates on its pre-scheduled date. Dodging a bug is not the same as understanding it, and I've only done the first.

The second is that the fresh certificate is good until the middle of November, which is close. Rotation is healthy again, so in theory it renews itself well before then and I never think about it. In theory is exactly the state this certificate was in last month.

The third is the one that actually matters, and it is not about certificates at all. I had no alarm on the one failure mode that mathematically guarantees a silent outage, which is the watcher itself going dark. Everything downstream of a dead operator looks fine until it suddenly, scheduledly, doesn't. The alert I need is not "is the certificate expiring," it is "has the thing that renews the certificate said anything at all in the last hour," and a crash-looping operator is precisely the component that cannot raise that alarm on its own behalf. Somebody outside the loop has to watch for the silence. I'm going to go be that somebody, and until I've built it, I'm choosing to not trust the color green.
