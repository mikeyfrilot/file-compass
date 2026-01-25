# Media Assets Guidance

## Recommended Visuals

File Compass is best demonstrated through terminal recordings, not static screenshots.

### Priority assets to create:

1. **Repository Tree Overview**
   - Show indexed structure
   - Highlight key directories
   - Demonstrate depth control

2. **Before/After Navigation Example**
   - "grep -r" noise vs File Compass results
   - Side-by-side comparison
   - Emphasize signal-to-noise improvement

3. **Search Relevance Ranking**
   - Query → ranked results
   - Show scoring in action
   - Demonstrate filtering

## Format Recommendations

| Format | Use Case |
|--------|----------|
| GIF | Terminal demos (5-8 seconds, looped) |
| SVG | Architecture diagrams |
| asciinema | Longer terminal recordings with copy-paste support |

## Recording Tips

- Use a clean terminal theme (dark background, readable font)
- Keep demos under 8 seconds for GIFs
- Show the command being typed, then results
- Pause briefly on results so viewers can read

## Tools

Recommended recording tools:
- [asciinema](https://asciinema.org) — terminal recording with replay
- [terminalizer](https://github.com/faressoft/terminalizer) — terminal to GIF
- [vhs](https://github.com/charmbracelet/vhs) — scripted terminal recordings

## Why Terminal Demos

Users evaluating File Compass want to see:
- How fast results appear
- How output is structured
- How much noise is removed

Terminal GIFs communicate this better than prose.
