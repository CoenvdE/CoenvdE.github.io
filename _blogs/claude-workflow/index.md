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

I use Claude Code every day, for two very different kinds of work. One is ML research, so PyTorch, uv, zarr and SLURM clusters. The other is web and app development, so TypeScript, pnpm, Supabase, and iOS through Capacitor. For a long time I just ran the defaults. My instruction file kept growing, I approved permissions whenever it asked, and everything I knew about my own projects lived in my head or in a README nobody had updated.

This post is the setup I ended up with after sitting down and rebuilding the whole thing on purpose. What I wanted was fast iteration that stays reproducible, and an agent that gets more useful over time instead of slowly drifting away from how my projects actually work. Everything here is plain files you can copy. No products, no magic. All of it is on GitHub in [CoenvdE/claude-code-setup](https://github.com/CoenvdE/claude-code-setup).

One idea shaped all of it. **Written instructions are suggestions that cost tokens. Hooks are rules that cost nothing.** Anything you put in a CLAUDE.md gets loaded into every session, spending context whether or not it is relevant, and Claude follows it most of the time but not always. Anything you put in a hook is executed by the harness, spends nothing until it fires, and cannot be skipped. Most of the skill in setting this up is knowing which of the two a given rule belongs in.

### The mental model: RAM vs disk

Claude Code loads your global `~/.claude/CLAUDE.md` into every single session. That makes it precious, because every line spends tokens on every task whether or not it has anything to do with it. So I treat CLAUDE.md as RAM, and everything else as disk that gets paged in when needed.

- **CLAUDE.md** (~60 lines): who I am, how my code is organized, my two work modes, a few hard rules about how I want to work. Nothing that only matters sometimes.
- **Rules** (`~/.claude/rules/`): conventions that load only when relevant files are touched.
- **Skills** (`~/.claude/skills/`): multi-step procedures that load only when invoked or matched.
- **Subagents** (`~/.claude/agents/`): separate roles with their own context window and tool access.
- **Hooks**: shell scripts the harness runs at fixed lifecycle events, for rules that must always hold.

The docs recommend keeping CLAUDE.md under 200 lines. Mine is a third of that, and Claude follows it noticeably better than it did when the file was long.

### Two work modes, path-scoped

My research and web work want opposite conventions. uv against pnpm, pytest against lint-and-build, a datasets doc against a schema doc. Instead of one file full of "if Python then this, if TypeScript then that", I keep two rule files with `paths:` frontmatter.

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

The rule loads only when Claude reads a matching file. My CLAUDE.md carries a two-line summary of both modes plus one hard rule, which is never to carry conventions across modes. No npm advice in a Python repo, ever. There is one caveat worth knowing about. Path-scoped rules trigger on *read*, not on write, so in a brand-new project they may not load until a matching file exists, and the summary in CLAUDE.md is what covers that gap. Both rule files are in the repo, [python-research.md](https://github.com/CoenvdE/claude-code-setup/blob/master/rules/python-research.md) and [web-app.md](https://github.com/CoenvdE/claude-code-setup/blob/master/rules/web-app.md).

The research rule carries one clause I would put in any setup where an agent writes tests. "Make the tests pass" and "check the code is correct" are different goals that look identical from the outside, and the first one is much easier. So: never weaken a test to reach green. A failing test is a finding to report, not a tolerance to loosen or a skip to add. Expected values come from theory, from a reference implementation, or from a property that must hold, never from recording whatever the code currently outputs. And every new check ships with a planted defect that proves it can fail.

### Skills: procedures, loaded on demand

Skills are folders with a `SKILL.md` whose description tells Claude when to invoke them. Mine, roughly in order of how much they earn, each linking to its copyable source in [the repo](https://github.com/CoenvdE/claude-code-setup/tree/master/skills):

- **[`karpathy-guidelines`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/karpathy-guidelines/SKILL.md)**: behavioral guardrails for every line of code the agent writes. More on this one below, because it might be the highest-leverage file in the whole setup.
- **[`new-research-project`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/new-research-project/SKILL.md)**: scaffolds a new research project from my own project template, or retrofits that template's guardrails into an existing repo.
- **[`anti-drift-setup`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/anti-drift-setup/SKILL.md)**: installs the documentation anti-drift system into a repo, which I get to below.
- **[`dataset-overview`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/dataset-overview/SKILL.md) / [`database-overview`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/database-overview/SKILL.md)**: maintain a living `docs/DATASETS.md` for research, or a schema doc for web, by inspecting the real data instead of guessing.
- **[`claude-setup-audit`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/claude-setup-audit/SKILL.md)**: re-grounds this whole setup against the current official docs. Claude Code ships behavior changes fast, and a config built six months ago encodes assumptions that may not hold anymore. It reports version gaps, changed behavior, size and permission problems, and features I could be using but am not. It proposes, it does not rewrite. Run it by asking, or with `/claude-setup-audit`, ideally right after an update.
- **[`close`](https://github.com/CoenvdE/claude-code-setup/blob/master/skills/close/SKILL.md)**: end-of-session ritual. Propose a commit, append to a session log, print a session rename.
- **[`commit`](https://github.com/CoenvdE/claude-code-setup/blob/master/commands/commit.md)**: drafts one Conventional Commits message from the actual staged diff, and always asks before committing.

The rule I hold myself to is that skills live globally in `~/.claude/skills/` and are available everywhere automatically. A skill only gets copied into a repo when the point is sharing it with collaborators through git.

### The karpathy-guidelines deserve special mention

Most of the pieces in this post shape what the agent works on. This one shapes how it writes code, which is why it fires on nearly every task, in both of my work modes. It distills Andrej Karpathy's observations on where LLM coding goes wrong into four habits:

1. **Think before coding.** Surface assumptions and ambiguities instead of silently picking an interpretation, and push back when a simpler approach exists.
2. **Simplicity first.** Minimum code that solves the problem. No speculative flexibility, no abstractions for single-use code, no error handling for scenarios that cannot happen.
3. **Surgical changes.** Touch only what the request requires, match the existing style, clean up your own orphans and nobody else's.
4. **Goal-driven execution.** Turn a vague task into a verifiable one. "Fix the bug" becomes "write a test that reproduces it, then make it pass", so the agent can loop on its own against real criteria.

If you copy one skill from my setup, copy this one. It is what keeps me from getting diffs that look impressive and then cost me an hour of cleanup.

### Subagents: roles, not just procedures

A skill loads instructions into the session you are already in. A subagent is a separate worker with its own context window, its own tool allowlist, and optionally its own model. That matters in two situations. One is when a job would flood your main context with material you do not want to keep around, like a 40-page PDF or a sweep across a large codebase. The other is when a job should be restricted in what it is allowed to touch.

Two of mine, at opposite ends:

- **[`paper-reader`](https://github.com/CoenvdE/claude-code-setup/blob/master/agents/paper-reader.md)** finds a paper in my local library, reads it in page ranges, and returns a structured brief covering problem, method, results, limitations, and relevance to my work. Read-only tools, and a cheaper model, because summarizing does not need the expensive one. The 40 pages stay in its context and only the brief comes back to mine.
- **[`model-sparring`](https://github.com/CoenvdE/claude-code-setup/blob/master/agents/model-sparring.md)** is a design-review partner for model work. It reads the model code, whatever metrics I have logged, and my experiment ledger, then comes back with correctness findings and ranked proposals, each one carrying the ablation that would settle it. The restrictions are the interesting part. It may write tests and experiment rows, but never the model, the config, or the data. It proposes, I decide. It also starts by checking whether it applies at all, and if you point it at a web app it says so and stops rather than improvising a review of code it was not built for.

The design rule I have converged on is to give an agent the narrowest tool set that still lets it finish, and to say in its prompt exactly which files it may write. The reason is independence. A reviewer that can also change the code ends up reviewing its own work on the next run, and it has an easy way out of any finding, which is to quietly edit the problem away instead of reporting it.

### Hooks: when "please always" becomes "always"

I have a writing rule: no em dashes, anywhere. It lived in CLAUDE.md and got violated regularly, because context is advisory. Now it is a 40-line PostToolUse hook, [no-dashes.sh](https://github.com/CoenvdE/claude-code-setup/blob/master/hooks/no-dashes.sh). After every file write or edit it greps `.md` and `.tex` files for the forbidden patterns, and on a hit it feeds a correction straight back to the model, which fixes it on the spot. It has already caught Claude mid-session, including while writing the very repo this post links to.

The general principle is that anything phrased as "always do X" or "never do Y", when it can be checked mechanically, belongs in a hook rather than in a sentence. I forget my own rules. The script does not.

### The anti-drift system

A valuable piece of the setup, and the one I would rebuild first if I lost it. The problem it solves is that docs describe code, code changes, docs rot, and then the agent acts confidently on stale information, which is worse than having no docs at all.

The fix is three small parts, per repo.

1. **A knowledge map** (`.claude/knowledge-map.json`), a list of `{match, doc, nudge}` entries connecting file paths to the docs that describe them. Usually the paths are code, so migrations pointing at a schema skill, or data loaders pointing at a datasets doc. But any path works. My maps also watch eval outputs, which nudge an experiment-log entry, and even Claude's own memory folder, which I come back to in the memory section. The map is not a one-time config. It starts with a handful of entries and grows as the project does, and the repo's CLAUDE.md carries a line telling Claude to add a mapping whenever a doc starts covering a new area of code.
2. **A drift hook.** After every write or edit, a shell script checks the edited path against the map. On a match it injects a one-line nudge into the session, something like "migration changed, update the schema skill". On no match it emits nothing at all, costing zero tokens. The important part is that the nudge lands in the session that just made the change, which still has all the context needed to update the doc properly.
3. **An audit script.** Each documented skill carries `sources:` frontmatter naming the code it describes, plus a `last_validated:` date. A deterministic shell script compares those against git history and flags any doc whose sources changed after it was last validated.

No LLM calls anywhere in the machinery. The agent only spends tokens when something actually drifted.

#### One firing, end to end

Here is what a single drift-catch looks like. The repo's map contains this entry:

```json
{
  "match": "src/data/",
  "doc": "docs/DATASETS.md",
  "nudge": "Data-loading code changed: check docs/DATASETS.md still matches (variables, shapes, preprocessing)."
}
```

1. I ask Claude to add a new variable to the data pipeline. It edits `src/data/era5.py`.
2. The harness runs the hook after that edit and pipes it a JSON payload containing the edited file path. The hook, which is plain bash and jq, tests that path against every `match` regex in the map. `src/data/era5.py` matches `src/data/`.
3. The hook prints the nudge and the harness injects it into the session as extra context. Claude, still holding everything about the change it just made, opens `docs/DATASETS.md`, updates the variable list with the dims and dtype it just implemented, and bumps the doc's `last_validated` date to today.
4. Weeks later I run the audit script. For each documented skill it compares the `sources:` paths against git history. If some other data change slipped past the nudge, that doc turns up flagged as `src-changed`, and I go revalidate it.

Steps 2 and 3 cost nothing when nothing matches, which is almost always. The system only speaks up when a doc has probably just become wrong, and it speaks to whoever is best placed to fix it right then.

### Memory: how it works, and how it rots

Claude Code has two complementary memories and it pays to keep them straight. CLAUDE.md and skills are what you curate and commit. **Auto memory** is what Claude writes for itself. As it works it saves learnings, things like build quirks, my corrections, and debugging insights, as plain markdown files, without being asked.

The mechanics matter here. Memory lives per project, in `~/.claude/projects/<project>/memory/`, where the project key comes from the git repository, so all worktrees and subdirectories of one repo share a single memory. A `MEMORY.md` index, or at least its first 200 lines, gets loaded into every session, and detailed topic files load on demand when they are relevant. All of it is plain markdown you can read, edit, or delete, and `/memory` opens it directly. When you see "Saved 2 memories" in the interface, this is what just happened.

Useful, but there are three failure modes that nothing in the default setup guards against.

1. **Stale facts.** A memory records what was true when it was written. The code moves on and the memory does not. Unlike a committed doc, nothing ever revalidates it, and a stale fact recalled with confidence is worse than no memory at all.
2. **The blended bucket.** The project key comes from where you launch the session. Start Claude from a parent folder holding ten unrelated repos and all ten share one memory, so web-app learnings surface in the middle of thesis work and the other way round.
3. **The private silo.** Memory is machine-local and personal. A learning the whole team needs, or that future-me on another machine needs, will sit in a local file forever unless something actively moves it out.

My setup addresses each one.

- **Against staleness**, a memory-hygiene rule in CLAUDE.md says only confirmed, final facts get persisted, never speculative ideas or abandoned approaches, so the pool starts cleaner. That governs memory automatically with no extra wiring, because memories are written by Claude itself mid-session, and CLAUDE.md is in its context at exactly that moment. The thing writing the memory is the thing reading the rule. For facts that have to stay true I do not rely on memory at all. Those go into committed docs and skills, where the anti-drift system revalidates them.
- **Against the blended bucket**, the launch-in-the-repo habit further down gives every repo its own correctly scoped memory.
- **Against the silo**, the drift map has a bridge entry. The drift hook exists for code-to-docs sync, but its mechanism is generic. It fires after every file write and matches the path against regexes, and a memory save is an ordinary file write, so one entry pointing its regex at the memory directory catches it and fires a nudge asking whether the fact is shareable and non-secret enough to promote into CLAUDE.md or a skill. Note the division of labor. The regex only detects that a memory was written, content unseen. The shareable-versus-secret judgment is Claude's, guided by criteria carried in the nudge text. And the promotion itself is an ordinary committed edit you see in the diff. Mechanism detects, model judges, human confirms.

#### Memory drifts too, so plan for it

Docs are not the only thing that rots. The memory pool drifts as well. A fact can be genuinely final in one session, say that the build command is `npm run build`, and be quietly wrong three weeks later after the project moves to pnpm. Memory sits below the anti-drift system's radar of committed files, so it needs its own counters.

- **Update, don't duplicate.** Claude's own memory instructions tell it to look for an existing memory covering a fact before saving, to edit that file when the fact has changed, and to delete memories that turned out to be wrong. When a session establishes something contradicting a stored memory, the expected result is one corrected file rather than two conflicting ones. Recent Claude Code versions also stamp each memory with a `modified` timestamp, so a recalled fact carries its age with it.
- **A periodic consolidation pass.** Update-on-conflict only works when the conflict actually gets noticed, so every so often I run `/consolidate-memory` over a project. It merges near-duplicates, fixes or deletes stale facts, and prunes the index. This one ships with Claude Code rather than being something you have to write, which is why it is not in my repo. It does for memory what the audit script does for docs.
- **Manual audit via `/memory`.** Everything is plain markdown. The command lists every memory file and opens it in your editor. When a "Recalled 2 memories" moment surfaces something that feels off, the fix is thirty seconds of reading and deleting.
- **Promotion out of the drift zone.** The most important counter is structural, and to be honest about it, it does not stop memory drift at all. It makes memory drift not matter. Facts that have to stay true do not belong in memory, and the silo nudge pushes them up into CLAUDE.md or a skill, which turns a memory-drift problem into a docs-drift problem, and that is the one the hook and the audit actually solve. The three counters above slow the drift of whatever is left behind. This one moves everything important out of the blast radius.

### Permissions hygiene

Two lessons from auditing my own settings, both embarrassing and both common.

1. **One-off approvals accumulate.** Every "yes, don't ask again" on a specific command saves that exact string to your allowlist forever. I had around 35 entries like `cp <one specific png> <one specific destination>`, none of which could ever match again. Now I answer plain "yes" for one-offs and save "don't ask again" for genuinely generic commands.
2. **Broad allows are a real risk.** I found `Bash(ssh:*)` sitting in my global settings. That is any ssh, to any host, running any remote command, with no prompt. A confused or prompt-injected session could have run commands on the university cluster silently. Deny-list your secrets while you are in there. Mine blocks reads of `.env`, ssh keys, and cloud credentials outright.

### Version-control your setup

`~/.claude` is now a git repo, config only, with all the runtime state gitignored. The whole tracked setup is about 130 KB. It gets history, diffs, an off-machine backup, and it moves to a new machine in a single clone.

### Habits that tie it together

- **Start sessions inside the repo you are working on**, not in a parent folder. Project CLAUDE.md, rules, settings and per-repo memory all attach to the directory you launched from, and one shared session at the root gives every unrelated project a single blended memory.
- **A workspace CLAUDE.md marks what is mine and what is reference.** My thesis workspace holds around 30 third-party clones sitting next to my own repos. A ten-line CLAUDE.md declares the clones read-only, so no agent ever "fixes" something inside GraphCast.
- **`/close` at the end of a session** keeps a human-readable log of what happened, independent of any chat history.

### Closing

Everything described here is copyable from [CoenvdE/claude-code-setup](https://github.com/CoenvdE/claude-code-setup), including an example CLAUDE.md and settings file to start from. You do not have to copy it by hand either. Clone the repo, start a Claude session in it, and ask it to read the README and set the whole thing up in your `~/.claude`. It will ask you the few things only you know, merge into whatever settings you already have rather than overwriting them, and tell you what it changed. Read that diff before you trust it, the same as any other change an agent makes for you.
