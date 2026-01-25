# P0 — Add minimal navigation quickstart

**Labels:** `docs`, `P0`

## Summary

Developers need a copy-paste example that works in under 30 seconds.

## Problem

Without a quickstart:
- Evaluation time is too high
- Concepts remain abstract
- Users bounce to alternatives

## Acceptance Criteria

- [ ] Copy-paste indexing + search example
- [ ] No configuration required (sensible defaults)
- [ ] Linked to examples directory for more
- [ ] Prerequisites clearly stated

## Suggested Structure

```markdown
## Quickstart

### Install
pip install file-compass

### Index a repository
file-compass index .

### Search
file-compass search "database connection"

### What you get
[show sample output]
```

## Notes

The quickstart should:
- Work on any repository
- Complete in <5 seconds
- Show meaningful results
- Demonstrate the output format
