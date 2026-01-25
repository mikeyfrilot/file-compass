# P1 — Document search ranking and filtering

**Labels:** `docs`, `P1`

## Summary

Users need to understand how search results are ranked and how to filter them.

## Problem

Without ranking documentation:
- Results feel arbitrary
- Filtering is trial-and-error
- Trust in the tool is lower

## Acceptance Criteria

- [ ] Explain relevance scoring algorithm (high-level)
- [ ] Document available filters and limits
- [ ] Clarify deterministic ordering guarantees
- [ ] Show filter examples

## Suggested Content

### Relevance Scoring

Explain factors:
- Filename match weight
- Path depth penalty
- Content match density
- File type boosting

### Filtering Options

```bash
file-compass search "auth" --type py --limit 10 --exclude tests/
```

### Deterministic Ordering

Explain: same query + same index = same results, always.

## Location

`docs/search.md`
