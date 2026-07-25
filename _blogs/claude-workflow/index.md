---
layout: blog_collection
title: "A Claude Code setup for fast building and research"
description: "How I configured Claude Code for both web/app development and ML research: a small global CLAUDE.md, path-scoped rules for two work modes, on-demand skills, deterministic hooks, and an anti-drift system that keeps documentation honest."
collection_id: claude-workflow
display_chapters: false
---

# A Claude Code setup for fast building and research
*By [Coen van den Elsen](https://coenvde.github.io/)*

---

### Why am I writing this?

I use Claude Code daily, across very different kinds of work: ML research (PyTorch, uv, zarr, SLURM clusters) and web apps (TypeScript, pnpm, Supabase, iOS via Capacitor). For a long time my setup was the default one: a growing instruction file, permissions approved ad hoc, and knowledge about my projects living only in my head or in stale READMEs.

This post describes the setup I landed on after deliberately auditing and rebuilding the whole thing. The goal is fast iteration without losing reproducibility, and an agent that gets *more* useful over time instead of drifting. Everything here is plain files you can copy: no products, no magic. All of it is on GitHub in [CoenvdE/claude-code-setup](https://github.com/CoenvdE/claude-code-setup) (rules, skills, hooks, an example CLAUDE.md and settings), and the research side has its own repo at [CoenvdE/research-template](https://github.com/CoenvdE/research-template).

The core insight that shaped all of it: **context is expensive and advisory, execution is cheap and guaranteed.** Instructions in a CLAUDE.md are read every session and followed most of the time. A hook is executed by the harness every time, no exceptions. Knowing which mechanism to use for which job is most of the game.

### The mental model: RAM vs disk

Claude Code loads your global `~/.claude/CLAUDE.md` into every single session. That makes it precious: every line spends context tokens on every task, related or not. So I treat CLAUDE.md as RAM and everything else as disk that gets paged in on demand:

- **CLAUDE.md** (~60 lines): who I am, how my code is organized, my two work modes, a few hard working-style rules. Nothing that only matters sometimes.
- **Rules** (`~/.claude/rules/`): conventions that load only when relevant files are touched.
- **Skills** (`~/.claude/skills/`): multi-step procedures that load only when invoked or matched.
- **Hooks**: shell scripts the harness runs at fixed lifecycle events, for rules that must *always* hold.

The docs recommend keeping CLAUDE.md under 200 lines. Mine is a third of that, and adherence is noticeably better than when it was long.

### Two work modes, path-scoped

My research and web work want opposite conventions (uv vs pnpm, pytest vs lint+build, DATASETS.md vs DATABASE.md). Instead of one file full of "if Python then..., if TypeScript then...", I keep two rule files with `paths:` frontmatter:

```markdown
---
paths:
  - "**/*.py"
  - "**/*.ipynb"
  - "**/pyproject.toml"
---
# Python research conventions
- Environments & deps: use uv. Don't use bare pip or conda...
- Deep-learning training: prefer PyTorch Lightning + LightningCLI with YAML configs...
```

The rule loads only when Claude reads a matching file. My CLAUDE.md carries a two-line summary of both modes plus one hard rule: never carry conventions across modes (no npm advice in a Python repo, ever). One caveat worth knowing: path-scoped rules trigger on *read*, not write, so a brand-new project may not load them until a file exists. The CLAUDE.md summary covers that gap. Both rule files are in the repo: [python-research.md](https://github.com/CoenvdE/claude-code-setup/blob/master/rules/python-research.md) and [web-app.md](https://github.com/CoenvdE/claude-code-setup/blob/master/rules/web-app.md).

### Skills: procedures, loaded on demand

Skills are folders with a `SKILL.md` whose description tells Claude when to invoke them. Mine, roughly in order of how much they earn (each links to its copyable source in [the repo](https://github.com/CoenvdE/claude-code-setup/tree/master/skills)):

- **[`karpathy-guidelines`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/karpathy-guidelines/SKILL.md)**: behavioral guardrails for every line of code the agent writes. More on this one below, because it might be the highest-leverage file in the whole setup.
- **[`new-research-project`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/new-research-project/SKILL.md)**: instantiates my [research template](https://github.com/CoenvdE/research-template) for a new project, or retrofits its guardrails into an existing repo. This one gets its own blog post.
- **[`anti-drift-setup`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/anti-drift-setup/SKILL.md)**: installs the documentation anti-drift system into a repo (below).
- **[`dataset-overview`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/dataset-overview/SKILL.md) / [`database-overview`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/database-overview/SKILL.md)**: maintain a living `docs/DATASETS.md` (research) or schema doc (web) by inspecting the *real* data, never guessing.
- **[`close`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/close/SKILL.md)**: end-of-session ritual: propose a commit, append to a SESSION_LOG, print a session rename.
- **[`commit`](https://github.com/CoenvdE/claude-code-setup/blob/master/commands/commit.md)**: drafts one Conventional Commits message from the actual staged diff and always asks before committing.

The rule I hold myself to: skills live globally in `~/.claude/skills/` and are available everywhere automatically. A skill only gets *copied into* a repo when the point is sharing it with collaborators through git.

### The karpathy-guidelines deserve special mention

Most of the pieces in this post shape *what* the agent works on. This skill shapes *how it writes code*, which makes it the one that fires on nearly every task, in both of my work modes. It distills Andrej Karpathy's observations on where LLM coding goes wrong into four enforced habits:

1. **Think before coding**: surface assumptions and ambiguities instead of silently picking an interpretation; push back when a simpler approach exists.
2. **Simplicity first**: minimum code that solves the problem. No speculative flexibility, no abstractions for single-use code, no error handling for impossible scenarios.
3. **Surgical changes**: touch only what the request requires, match existing style, clean up your own orphans and nobody else's.
4. **Goal-driven execution**: transform vague tasks into verifiable goals ("fix the bug" becomes "write a test that reproduces it, then make it pass") so the agent can loop independently against real success criteria.

If you copy one skill from my setup, copy this one. It is the difference between an agent that produces impressive-looking diffs and one that produces mergeable ones.

### Hooks: when "please always" becomes "always"

I have a writing rule: no em dashes, anywhere. It lived in CLAUDE.md and was violated regularly, because context is advisory. Now it is a 40-line PostToolUse hook ([no-dashes.sh](https://github.com/CoenvdE/claude-code-setup/blob/master/hooks/no-dashes.sh)): after every file write or edit, a script greps `.md` and `.tex` files for the forbidden patterns and, on a hit, feeds a correction straight back to the model, which fixes it immediately. It has already caught Claude mid-session, including while writing the very repo this post links to.

That is the general principle: anything phrased as "always do X" or "never do Y" that can be checked mechanically should be a hook, not a sentence. Sentences drift; scripts do not.

### The anti-drift system

The most valuable piece of the whole setup. The problem: docs describe code, code changes, docs rot, and then the agent confidently acts on stale information, which is worse than no docs at all.

The fix is three small parts, per repo:

1. **A knowledge map** (`.claude/knowledge-map.json`): a list of `{match, doc, nudge}` entries connecting file paths to the docs that describe them. Usually the paths are code (migrations pointing at a schema skill, data loaders pointing at a datasets doc), but any path works: my maps also watch eval outputs (nudging an experiment-log entry) and even Claude's own memory folder (more on that in the memory section).
2. **A drift hook**: after every write/edit, a shell script checks the edited path against the map. On a match it injects a one-line nudge into the session ("migration changed: update the schema skill"). On no match it emits nothing, costing zero tokens. Crucially, the nudge lands in the session that *just made the change*, which has all the context needed to update the doc correctly right now.
3. **An audit script**: each documented skill carries `sources:` (which code it describes) and `last_validated:` frontmatter. A deterministic shell script compares those against git history and flags docs whose sources changed after their last validation.

No LLM calls anywhere in the machinery. The agent only spends tokens when something actually drifted.

#### One firing, end to end

Here is what a single drift-catch actually looks like. The repo's map contains this entry:

```json
{
  "match": "src/data/",
  "doc": "docs/DATASETS.md",
  "nudge": "Data-loading code changed: check docs/DATASETS.md still matches (variables, shapes, preprocessing)."
}
```

1. I ask Claude to add a new variable to the data pipeline. It edits `src/data/era5.py`.
2. The harness runs the hook after that edit, piping it a JSON payload containing the edited file path. The hook (plain bash + jq) tests the path against every `match` regex in the map. `src/data/era5.py` matches `src/data/`.
3. The hook prints the nudge, which the harness injects into the session as extra context. Claude, still holding everything about the change it just made, opens `docs/DATASETS.md`, updates the variable list with the dims and dtype it just implemented, and bumps the doc's `last_validated` date to today.
4. Weeks later I run the audit script. For each documented skill it compares the `sources:` paths against git history. If some other data change slipped past the nudge, that doc shows up flagged as `src-changed`, and I revalidate it.

Steps 2 and 3 cost nothing when nothing matches, which is almost always. The whole system only speaks up at the moment a doc probably became wrong, to the one agent best placed to fix it.

### Memory: how it works, and how it rots

Claude Code has two complementary memories, and it pays to keep them straight. CLAUDE.md and skills are what *you* curate and commit. **Auto memory** is what Claude writes for itself: as it works, it saves learnings (build quirks, your corrections, debugging insights) as plain markdown files, without you asking.

The mechanics are worth knowing. Memory lives per project, in `~/.claude/projects/<project>/memory/`, where `<project>` is derived from the git repository, so all worktrees and subdirectories of one repo share one memory. A `MEMORY.md` index (its first ~200 lines) is loaded into every session; detailed topic files load on demand when relevant. Everything is plain markdown you can read, edit, or delete, and the `/memory` command opens it directly. When you see "Saved 2 memories" in the interface, this is what's happening.

Useful, but it has three failure modes that nothing in the default setup guards against:

1. **Stale facts.** A memory records what was true when it was written. Code moves on; the memory doesn't. Unlike committed docs, nothing ever revalidates it, and a confidently recalled stale fact is worse than no memory at all.
2. **The blended bucket.** The project key comes from where you *launch* the session. Start Claude from a parent folder holding ten unrelated repos and all ten share one memory: web-app learnings surface during thesis work and vice versa.
3. **The private silo.** Memory is machine-local and personal. A learning that the whole team (or your future self on another machine) needs will sit in a local file forever unless something actively moves it out.

My setup addresses each one:

- **Against staleness**: a memory-hygiene rule in CLAUDE.md says only *confirmed, final* facts get persisted, never speculative ideas or abandoned approaches, so the memory pool starts cleaner. This governs memory automatically, with no extra wiring, because memories are written *by Claude itself* mid-session, and CLAUDE.md is in its context at exactly that moment: the writer of memory is the reader of the rule. The durable tier for facts that must stay true is not memory but committed docs and skills, which the anti-drift system actively revalidates. Memory is the scratch tier; docs are the audited tier.
- **Against the blended bucket**: the launch-in-the-repo habit (below) gives every repo its own correctly scoped memory.
- **Against the silo**: the drift map's bridge entry. The drift hook exists for code-to-docs sync, but its mechanism is generic: it fires after *every* file write and matches the written path against regexes. A memory save is an ordinary file write, so one map entry whose regex matches the memory directory (instead of a code path) catches it and fires a nudge: "if this fact is shareable and non-secret, promote it to CLAUDE.md or a skill." Private learnings become versioned team knowledge deliberately, not never.

#### Memory drifts too, so plan for it

Docs are not the only thing that rots; the memory pool itself drifts. A fact can be genuinely *final* in one session ("tests need a local Redis") and superseded three weeks later ("we mocked Redis, they don't anymore"). Since memory sits below the anti-drift system's radar of committed files, it needs its own counters, and they exist:

- **Update, don't duplicate.** Claude's own memory instructions tell it to check for an existing memory covering a fact before saving, to edit that file when the fact changed, and to delete memories that turned out wrong. When a session establishes something that contradicts a stored memory, the expected outcome is a corrected file, not two conflicting ones. Recent Claude Code versions also stamp each memory with a `modified` timestamp, so recalled facts carry their age.
- **A periodic consolidation pass.** Update-on-conflict only works when the conflict gets noticed, so every so often I run a consolidate-memory pass over a project: merge near-duplicates, fix or delete stale facts, prune the index. It is the memory-tier analog of the docs audit script: the deliberate sweep that catches what the automatic behavior missed.
- **Manual audit via `/memory`.** Everything is plain markdown; the `/memory` command lists every memory file and opens it in your editor. When a "Recalled 2 memories" moment surfaces something that feels off, the fix is thirty seconds of reading and deleting.
- **Promotion out of the drift zone.** The most important counter is structural: facts that must *stay* true don't belong in memory at all. The silo nudge above pushes them up into CLAUDE.md or a skill, where the anti-drift system actively revalidates them. Memory drift is tolerable precisely because memory is the scratch tier.

### Permissions hygiene

Two lessons from auditing my own settings, both embarrassing and both common:

1. **One-off approvals accumulate.** Every "yes, don't ask again" on a specific command saves that exact string to your allowlist forever. I had ~35 entries like `cp <one specific png> <one specific destination>` that could never match again. Now: plain "yes" for one-offs, "don't ask again" only for genuinely generic commands.
2. **Broad allows are a real risk.** I found `Bash(ssh:*)` in my global settings: any ssh, to any host, running any remote command, without a prompt. A confused or prompt-injected session could have executed commands on the university cluster silently. Deny-list your secrets too: my settings block reads of `.env`, ssh keys, and cloud credentials outright.

### Version-control your setup

`~/.claude` is now a git repo (config only: CLAUDE.md, rules, skills, hooks, settings; runtime state is gitignored). The whole tracked setup is ~130 KB. It gets history, diffs, and an off-machine backup, and it makes the setup portable to a new machine in one clone. If your agent config is infrastructure, treat it like infrastructure.

### Habits that tie it together

- **Start sessions inside the repo you are working on**, not in a parent folder. Project CLAUDE.md, rules, settings, and per-repo memory all attach to the launch directory; one shared session at the root gives every unrelated project one blended memory.
- **A workspace CLAUDE.md marks what's mine vs reference.** My thesis workspace holds ~30 third-party clones next to my own repos. A ten-line CLAUDE.md declares the clones read-only, so no agent ever "fixes" code inside GraphCast.
- **`/close` at the end of a session** keeps a human-readable log of what happened, independent of any chat history.

### Takeaways

If I could only keep three pieces: the tiny CLAUDE.md (RAM discipline), the anti-drift system (docs that stay true), and hooks for hard rules (guaranteed, not hoped). Everything else is refinement.

Everything described here is copyable from [CoenvdE/claude-code-setup](https://github.com/CoenvdE/claude-code-setup), including an example CLAUDE.md and settings file to start from. The companion post shows what this looks like when it meets an actual research codebase: [a solid research template](/blogs/research-template/index/), with its code at [CoenvdE/research-template](https://github.com/CoenvdE/research-template).
