# P1 — Add guidance for large repositories

**Labels:** `docs`, `P1`

## Summary

Large monorepos need specific guidance to use File Compass effectively.

## Problem

Without large repo guidance:
- Users hit performance issues
- Index sizes become unwieldy
- Important patterns are missed

## Acceptance Criteria

- [ ] Monorepo recommendations documented
- [ ] Ignore patterns explained (`.compassignore` or similar)
- [ ] Performance tips for 10k+ file repos
- [ ] Incremental indexing guidance (if supported)

## Suggested Content

### Monorepo Strategies

- Index specific directories, not root
- Use ignore patterns aggressively
- Consider multiple focused indexes

### Ignore Patterns

```
# .compassignore
node_modules/
.git/
dist/
*.min.js
```

### Performance Tips

- Exclude generated files
- Exclude vendored dependencies
- Use shallow indexing for exploration

## Location

`docs/large-repos.md`
