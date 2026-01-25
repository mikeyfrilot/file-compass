# P2 — Add performance benchmarks and scaling notes

**Labels:** `docs`, `performance`, `P2`

## Summary

Users evaluating File Compass for large projects need performance expectations.

## Problem

Without benchmarks:
- Users can't plan for their repo size
- Performance issues feel like bugs
- Comparisons to alternatives are blind

## Acceptance Criteria

- [ ] Benchmarks for various repo sizes (1k, 10k, 100k files)
- [ ] Memory usage notes
- [ ] Expected runtime ranges for indexing and search
- [ ] Hardware recommendations (if any)

## Suggested Content

### Benchmarks

| Repo Size | Index Time | Search Time | Memory |
|-----------|-----------|-------------|--------|
| 1k files  | ~Xs       | ~Xms        | ~XMB   |
| 10k files | ~Xs       | ~Xms        | ~XMB   |
| 100k files| ~Xs       | ~Xms        | ~XMB   |

(Fill with actual measurements)

### Scaling Notes

- Index size grows linearly with file count
- Search time is sublinear (indexed)
- Memory usage during indexing vs search

### When to Optimize

- If indexing takes >30s, review ignore patterns
- If search takes >100ms, consider index partitioning

## Location

`docs/performance.md`
