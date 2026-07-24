---
layout: blog_collection
title: "A Claude Code setup for fast research iteration"
description: "How I configured Claude Code as a research collaborator: a small global CLAUDE.md, path-scoped rules for two work modes, on-demand skills, deterministic hooks, and an anti-drift system that keeps documentation honest."
collection_id: claude-workflow
display_chapters: false
---

# A Claude Code setup for fast research iteration
*By [Coen van den Elsen](https://coenvde.github.io/)*

---

### Why am I writing this?

I use Claude Code daily, across very different kinds of work: ML research (PyTorch, uv, zarr, SLURM clusters) and web apps (TypeScript, pnpm, Supabase, iOS via Capacitor). For a long time my setup was the default one: a growing instruction file, permissions approved ad hoc, and knowledge about my projects living only in my head or in stale READMEs.

This post describes the setup I landed on after deliberately auditing and rebuilding the whole thing. The goal is fast iteration without losing reproducibility, and an agent that gets *more* useful over time instead of drifting. Everything here is plain files you can copy: no products, no magic.

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

The rule loads only when Claude reads a matching file. My CLAUDE.md carries a two-line summary of both modes plus one hard rule: never carry conventions across modes (no npm advice in a Python repo, ever). One caveat worth knowing: path-scoped rules trigger on *read*, not write, so a brand-new project may not load them until a file exists. The CLAUDE.md summary covers that gap.

### Skills: procedures, loaded on demand

Skills are folders with a `SKILL.md` whose description tells Claude when to invoke them. Mine, roughly in order of how much they earn:

- **`new-research-project`**: instantiates my [research template](https://github.com/CoenvdE/research-template) for a new project, or retrofits its guardrails into an existing repo. This one gets its own blog post.
- **`anti-drift-setup`**: installs the documentation anti-drift system into a repo (below).
- **`dataset-overview` / `database-overview`**: maintain a living `docs/DATASETS.md` (research) or schema doc (web) by inspecting the *real* data, never guessing.
- **`close`**: end-of-session ritual: propose a commit, append to a SESSION_LOG, print a session rename.
- **`commit`**: drafts one Conventional Commits message from the actual staged diff and always asks before committing.
- **`karpathy-guidelines`**: behavioral guardrails against classic LLM coding failure modes (overcomplication, non-surgical edits, silent assumptions).

The rule I hold myself to: skills live globally in `~/.claude/skills/` and are available everywhere automatically. A skill only gets *copied into* a repo when the point is sharing it with collaborators through git.

### Hooks: when "please always" becomes "always"

I have a writing rule: no em dashes, anywhere. It lived in CLAUDE.md and was violated regularly, because context is advisory. Now it is a 40-line PostToolUse hook: after every file write or edit, a script greps `.md` and `.tex` files for the forbidden patterns and, on a hit, feeds a correction straight back to the model, which fixes it immediately.

That is the general principle: anything phrased as "always do X" or "never do Y" that can be checked mechanically should be a hook, not a sentence. Sentences drift; scripts do not.

### The anti-drift system

The most valuable piece of the whole setup. The problem: docs describe code, code changes, docs rot, and then the agent confidently acts on stale information, which is worse than no docs at all.

The fix is three small parts, per repo:

1. **A knowledge map** (`.claude/knowledge-map.json`): a list of `{match, doc, nudge}` entries connecting code paths to the docs that describe them.
2. **A drift hook**: after every write/edit, a shell script checks the edited path against the map. On a match it injects a one-line nudge into the session ("migration changed: update the schema skill"). On no match it emits nothing, costing zero tokens. Crucially, the nudge lands in the session that *just made the change*, which has all the context needed to update the doc correctly right now.
3. **An audit script**: each documented skill carries `sources:` (which code it describes) and `last_validated:` frontmatter. A deterministic shell script compares those against git history and flags docs whose sources changed after their last validation.

No LLM calls anywhere in the machinery. The agent only spends tokens when something actually drifted.

### Memory vs CLAUDE.md

Claude Code has two complementary memories and it pays to keep them straight. Auto memory is what Claude writes for itself: machine-local notes from your corrections. CLAUDE.md and skills are what *you* curate and commit. My drift map includes one entry that bridges them: when a memory file is written, the hook nudges "if this fact is shareable and non-secret, promote it to CLAUDE.md or a skill." Private learnings become team knowledge deliberately, not never.

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

If I could only keep three pieces: the tiny CLAUDE.md (RAM discipline), the anti-drift system (docs that stay true), and hooks for hard rules (guaranteed, not hoped). Everything else is refinement. The companion post shows what this looks like when it meets an actual research codebase: [a research template that is hard to fool](/blogs/research-template/index/).
