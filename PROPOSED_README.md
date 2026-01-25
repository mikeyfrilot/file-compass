# File Compass

Deterministic file-system navigation and inspection tools for large repositories.

File Compass helps humans and agents answer one question reliably:

**"Where is the relevant code, and why?"**

---

## What problem does this solve?

As repositories grow, navigation becomes expensive:

- thousands of files across nested directories
- unclear ownership and boundaries
- search results without context
- slow or unsafe recursive scanning
- poor signal-to-noise for agents

File Compass provides **structured navigation**.

---

## Core capabilities

- Directory and file indexing
- Context-aware search
- Deterministic traversal
- Relevance scoring
- Structured file summaries
- Machine-readable navigation output

File Compass does not modify files — it inspects and explains them.

---

## Quick start

```bash
pip install file-compass
file-compass index .
file-compass search "authentication"
```

(Commands illustrative — see repo for exact CLI.)

---

## Typical workflows

- Navigate unfamiliar codebases
- Provide agents with safe file context
- Identify relevant modules quickly
- Generate structured repository maps
- Reduce blind recursive scanning

---

## When to use File Compass

- Large monorepos
- Agent-based code understanding
- Retrieval-augmented generation
- Tool-assisted debugging
- Documentation discovery

## When not to use it

- Small single-module projects
- One-off grep usage
- Manual browsing in IDEs

---

## Design goals

- **Deterministic traversal**
- **Explicit file boundaries**
- **Safe-by-default scanning**
- **Predictable output ordering**
- **Low memory overhead**

---

## Project status

**Stable**

Search heuristics may evolve; core traversal APIs are stable.

---

## Ecosystem

Part of the [MCP Tool Shop](https://github.com/mcp-tool-shop) ecosystem.

Works especially well with:

- **Tool Compass** (tool discovery)
- **Tool Scan** (static inspection)
- **Dev Brain** (orchestration)
- **Context Window Manager** (context shaping)

---

## License

MIT
