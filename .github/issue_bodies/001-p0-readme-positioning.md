# P0 — Clarify File Compass positioning and value

**Labels:** `docs`, `marketing`, `P0`

## Summary

The README needs to clearly communicate why File Compass exists alongside grep/ripgrep.

## Problem

Developers will ask: "Why not just use ripgrep?"

The README must answer this immediately.

## Acceptance Criteria

- [ ] README answers "why not grep or ripgrep?"
- [ ] Clear explanation of deterministic navigation
- [ ] Example included on first screen (above the fold)
- [ ] Value proposition in first 2 sentences

## Key Differentiators to Highlight

1. **Structured output** — machine-readable, not just text
2. **Deterministic ordering** — same query = same results
3. **Relevance scoring** — ranked results, not just matches
4. **Safe traversal** — respects boundaries, avoids dangerous paths
5. **Agent-friendly** — designed for LLM consumption

## Context

See `PROPOSED_README.md` in the safe overlay package for reference positioning.
