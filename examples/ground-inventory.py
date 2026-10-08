#!/usr/bin/env python3
"""ground_inventory.py — FML-36: AAP dynamic inventory from the ground work-query.

A thin (stdlib-only) Ansible inventory SCRIPT — not a plugin (deviation from
ADR-009's wording, KISS: the store already did needs-work AND fresh filtering,
so the client needs zero keyed_groups/compose/caching helpers). AAP runs it as
an SCM inventory source (source_path = this file in a synced git project).

It GETs the ground freshness-gated work-query and reshapes the targets into an
Ansible inventory. The store is the grounded source: the hosts returned are
EXACTLY those the store observed as needing work AND can currently vouch for
(fresh). AAP acts on observed state, never desired state (ADR-009).

    --list   -> the full inventory JSON with _meta.hostvars (one call)
    --host X -> {} (all vars are already in _meta; kept for script compat)

Environment (non-secret; the work-query is an unauthenticated read):
    GROUND_API_BASE     default https://ground.apps.darkpool.h00pz.co
                        (the public Route — AAP is off-cluster; do NOT use the
                        in-cluster Service name)
    GROUND_WORK_PREDICATE  default "cert"
    GROUND_WORK_FRESH      default "on"  (surgical; "off" = brute force)
    GROUND_API_TIMEOUT     default 15 (seconds)
    GROUND_TLS_INSECURE    default "0"  ("1" disables TLS verify — the Route
                        serves a real Let's Encrypt cert, so leave verification ON)

Groups produced:
    <predicate>_work            every returned host (e.g. cert_work)
    <predicate>_<status>        per derived status (e.g. cert_expired, cert_expiring)
Each host is named by its fqdn (the work-query target `name`), which is what the
renewal play loops over. Per-host vars carry the observed facts + provenance.
"""
import json
import os
import ssl
import sys
import urllib.request

DEFAULT_BASE = "https://ground.apps.darkpool.h00pz.co"


def _cfg():
    return {
        "base": os.environ.get("GROUND_API_BASE", DEFAULT_BASE).rstrip("/"),
        "predicate": os.environ.get("GROUND_WORK_PREDICATE", "cert"),
        "fresh": os.environ.get("GROUND_WORK_FRESH", "on"),
        "timeout": float(os.environ.get("GROUND_API_TIMEOUT", "15")),
        "insecure": os.environ.get("GROUND_TLS_INSECURE", "0") == "1",
    }


def _fetch_work(cfg):
    url = "%s/api/work?predicate=%s&fresh=%s" % (
        cfg["base"], cfg["predicate"], cfg["fresh"])
    ctx = ssl._create_unverified_context() if cfg["insecure"] else None
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=cfg["timeout"], context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _empty_inventory():
    return {"_meta": {"hostvars": {}}, "all": {"children": ["ungrouped"]},
            "ungrouped": {"hosts": []}}


def build_inventory(work, predicate):
    """Reshape a work-query response into Ansible inventory JSON.

    Host = the target's fqdn (`name`). Groups: <predicate>_work (all) and
    <predicate>_<status>. _meta.hostvars carries observed facts + provenance so
    AAP need never call --host.
    """
    inv = _empty_inventory()
    hostvars = inv["_meta"]["hostvars"]
    work_group = "%s_work" % predicate
    inv[work_group] = {"hosts": []}
    all_children = inv["all"]["children"]
    if work_group not in all_children:
        all_children.append(work_group)

    for t in work.get("targets", []):
        fqdn = t.get("name")
        if not fqdn:
            continue
        inv[work_group]["hosts"].append(fqdn)
        status = t.get("status") or "unknown"
        status_group = "%s_%s" % (predicate, status)
        if status_group not in inv:
            inv[status_group] = {"hosts": []}
            if status_group not in all_children:
                all_children.append(status_group)
        inv[status_group]["hosts"].append(fqdn)

        hv = {
            "ansible_host": fqdn,
            "ground_predicate": predicate,
            "ground_record_id": t.get("id"),
            "ground_status": status,
            "ground_fresh": t.get("fresh"),
            "ground_deployed_to": t.get("deployed_to"),
            # the source of truth for freshness/threshold rides along so the
            # play (and the operator) can see WHY this host is in the set.
            "ground_threshold_days": work.get("threshold_days"),
        }
        # cert_deploy_roles is consumed by deploy_certs.yml UNPREFIXED (it read
        # the same var name from the NetBox nb_inventory compose); surface it
        # verbatim so the deploy play is a drop-in against the ground feed.
        if "cert_deploy_roles" in t:
            hv["cert_deploy_roles"] = t.get("cert_deploy_roles") or []
        # carry every remaining scalar work-query field as ground_<field>.
        for k, v in t.items():
            if k in ("name", "id", "status", "fresh", "deployed_to",
                     "cert_deploy_roles"):
                continue
            hv["ground_%s" % k] = v
        hostvars[fqdn] = hv

    for g in (work_group,) + tuple(k for k in inv if k.startswith(predicate + "_") and k != work_group):
        inv[g]["hosts"].sort()
    return inv


def main(argv):
    cfg = _cfg()
    if len(argv) >= 2 and argv[1] == "--host":
        # all vars live in _meta.hostvars; nothing per-host to add.
        print(json.dumps({}))
        return 0
    # default action is --list (AAP always calls --list first).
    try:
        work = _fetch_work(cfg)
    except Exception as exc:  # a fetch failure must not silently yield hosts.
        sys.stderr.write("ground_inventory: work-query fetch failed: %s\n" % exc)
        # emit an empty-but-valid inventory so AAP records zero targets (an
        # honest empty feed), never a crash that leaves a stale inventory.
        print(json.dumps(_empty_inventory()))
        return 1
    inv = build_inventory(work, cfg["predicate"])
    print(json.dumps(inv, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
