# AGENTS.md — for any AI working in LOGOS ENGINE

LOGOS ENGINE is an offline King James Bible study system: KJV plus the 1611 Apocrypha, Strong's Hebrew and Greek, cross-references, and semantic search. Built by Furie777. This file is for any AI or coding agent (Claude, Grok, a local model, Copilot) asked to use or change this repo.

## Read first
1. START_HERE.txt: what this is, for a human.
2. README.md: commands and quick start.
3. .claude/CONTEXT.md: earlier working context for AI sessions.
4. docs/INSTALL.md and docs/RECOVERY.md: setup and recovery.

## Run it (no AI needed)
    pip install networkx
    python logos.py verse "John 3:16"
    python logos.py search "grace"
    python logos.py strongs G26

## Rules for any AI here
1. Quote Scripture from the data in this repo, not from memory. Name the verse reference.
2. Counts depend on which graph you build. The cross-reference total in README.md comes from this repo's build scripts. A different source or build gives a different number. Rerun the script before you quote a count.
3. Mark what you checked. Write "checked: <command or file>" next to any claim. Write "not checked" when you didn't check it.
4. Don't change the verse data files. Propose a change on a branch and leave it to the owner.
5. This repo is public. Never add personal names, contact details, or private notes.
