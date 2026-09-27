# ADR-0001: Reversibility Over Permission

Date: 2026-09-27
Status: Accepted

## Context

Cassian is intended to eventually act autonomously on real files, repositories, and systems — without being prompted for every action. The natural first instinct is to control this through a permissions model: restrict dangerous commands, force flags, and administrative actions, and require review when risk is detected.

That instinct is necessary but not sufficient. Analysis of three representative autonomous tasks showed that none of them require elevated privileges to cause real, irrecoverable harm:

1. **Git management across projects** (auto-backing up unstaged changes, initial scaffolding). Worst case: losing unstaged changes, corrupting commit history, causing merge conflicts.
2. **Cleaning up old `venv`/`node_modules` directories** to reclaim disk space. Worst case: deleting environments still in use, or accidentally removing other essential files.
3. **Reorganizing the Downloads folder** (renaming, sorting, moving files). Worst case: files effectively lost — moved somewhere unknown, not actually deleted but unrecoverable in practice.

In every case, the operation itself is ordinary and fully permitted — plain filesystem writes, plain git commands, no `sudo`, no `--force`. Restricting *access* would not have prevented any of these failures, because the danger was never in the privilege level of the action. It was in the **irreversibility** of an ordinary action performed without a way back.

## Options Considered

1. **Permission/risk-gating model** — restrict high-risk commands, require review when risk is detected.
   - Pros: familiar model, simple to reason about, prevents access-based attacks.
   - Cons: does not address failures caused by ordinary, permitted actions. Would not have prevented any of the three worst-case scenarios above.

2. **Reversibility-by-construction** — every autonomous action must have a pre-recorded, cheap undo path established *before* it executes, regardless of whether the action is "risky."
   - Pros: addresses the actual failure mode observed (ordinary actions causing irrecoverable loss). Shifts the design question from "should I let this happen?" to "have I preserved a way back before I let this happen?" Makes safety a structural property of the system rather than a judgment call made per-action.
   - Cons: requires a different undo mechanism per content type, since not all content can be reversed the same way (see Decision).

## Decision

Cassian's foundational safety principle is **reversibility over permission**. Permission-gating (least privilege, risk detection, human review for genuinely dangerous operations) remains part of the system, but it is not the primary safety mechanism — it is a secondary layer. The primary mechanism is that **no autonomous action is allowed to execute unless a reversal path for it has already been established.**

Reversibility is not implemented as one universal snapshot mechanism. Different content types require different undo strategies, chosen based on whether the content can be cheaply regenerated, is already versioned by an existing tool, or is arbitrary and irreducible:

| Task type | Content nature | Undo mechanism |
|---|---|---|
| `venv` / `node_modules` cleanup | Derived artifact — fully reproducible from a manifest + lockfile + runtime version | **Recipe-based regeneration.** Before deletion, record the manifest path, lockfile hash, and interpreter/runtime version. Undo = reinstall from the recorded recipe. Storage cost is KBs, not GBs. |
| Git operations | Authored, original content (diffs, unstaged changes) | **Native git snapshotting.** Before any operation that could clobber working-tree state, create a stash-commit (or dangling commit) and log its hash. Undo = restore from that hash via stash-apply or cherry-pick. No new mechanism is invented — this automates a capability git already provides. |
| Downloads reorganization | Arbitrary, irreducible content (files with no recipe) | **Action log + managed trash.** Every move/rename is logged with source, destination, and timestamp; undo = replay the log in reverse. Deletion never removes data outright — it moves files into a Cassian-managed trash with a retention window, mirroring how OS-level recycle bins already solve this. |

A more general, content-aware, millisecond snapshotting tool for arbitrary directories (regardless of content type) was considered and explicitly deferred — it is a substantially harder, standalone research problem (bordering on content-addressable storage and copy-on-write filesystem design, e.g. ZFS/btrfs/Nix-style approaches) and is not required to satisfy the three tasks above. It is noted here so the idea isn't lost, and may be revisited as a separate future project.

## Consequences

- Every new autonomous capability added to Cassian in the future must define its own reversal mechanism *before* it is allowed to run unprompted. This is the entry test for granting Cassian any new unsupervised task type — no undo path, no autonomy.
- Permission-gating (danger detection, human review, restricted commands) is retained as a secondary layer for genuinely irreversible real-world actions where no undo mechanism can exist (e.g. sending an email, making a payment, an external API call with side effects). ADR-0002 or later should define how Cassian handles this class of action, where reversibility is not possible even in principle.
- The three mechanisms above are the first concrete implementation targets. The git-safety mechanism is the recommended starting point, since it requires no new invention — only automating a capability git already provides.