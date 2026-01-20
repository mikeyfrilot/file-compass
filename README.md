# File Compass

Semantic file search for AI workstations using HNSW vector indexing and local embeddings.

## Features

- **Semantic Search**: Find files by describing what you're looking for, not just keywords
- **AST-Aware Chunking**: Intelligently splits Python files by functions and classes
- **Local Embeddings**: Uses Ollama with nomic-embed-text (no API keys needed)
- **Fast Search**: HNSW indexing for sub-second queries across thousands of files
- **Git-Aware**: Optionally filter to only git-tracked files
- **MCP Server**: Integrates with Claude Code and other MCP clients

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) with `nomic-embed-text` model

## Installation

```bash
# Clone the repository
git clone https://github.com/mikeyfrilot/file-compass.git
cd file-compass

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Pull the embedding model
ollama pull nomic-embed-text
```

## Quick Start

### 1. Build the Index

```bash
# Index a directory
file-compass index -d "C:/Projects"

# Index multiple directories
file-compass index -d "C:/Projects" "D:/Code"
```

### 2. Search Files

```bash
# Semantic search
file-compass search "database connection handling"

# Filter by file type
file-compass search "training loop" --types python

# Git-tracked files only
file-compass search "API endpoints" --git-only
```

### 3. Check Status

```bash
file-compass status
```

## MCP Server

File Compass includes an MCP server for integration with Claude Code and other AI assistants.

### Available Tools

| Tool | Description |
|------|-------------|
| `file_search` | Semantic search for files and code |
| `file_preview` | Get content from a specific file |
| `file_index_status` | Check index statistics |
| `file_index_scan` | Build or rebuild the index |

### Claude Code Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "file-compass": {
      "command": "python",
      "args": ["-m", "file_compass.gateway"],
      "cwd": "C:/path/to/file-compass"
    }
  }
}
```

## Configuration

Configuration is managed via environment variables or the `FileCompassConfig` class:

| Variable | Default | Description |
|----------|---------|-------------|
| `FILE_COMPASS_DIRECTORIES` | `F:/AI` | Comma-separated directories to index |
| `FILE_COMPASS_OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `FILE_COMPASS_EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model name |

## How It Works

1. **Scanning**: Discovers files matching configured extensions, respecting `.gitignore`
2. **Chunking**: Splits files into semantic pieces:
   - Python: AST-aware (functions, classes, modules)
   - Markdown: Heading-based sections
   - Other: Sliding window with overlap
3. **Embedding**: Generates 768-dim vectors via Ollama's nomic-embed-text
4. **Indexing**: Stores vectors in HNSW index, metadata in SQLite
5. **Search**: Embeds query, finds nearest neighbors, returns ranked results

## Project Structure

```
file-compass/
├── file_compass/
│   ├── __init__.py      # Package init, default paths
│   ├── config.py        # Configuration management
│   ├── embedder.py      # Ollama embedding client
│   ├── scanner.py       # File discovery
│   ├── chunker.py       # Smart file chunking
│   ├── indexer.py       # HNSW + SQLite index
│   ├── gateway.py       # MCP server
│   └── cli.py           # Command-line interface
├── pyproject.toml
├── README.md
└── LICENSE
```

## Performance

- **Index Size**: ~1KB per chunk (embedding + metadata)
- **Search Latency**: <100ms for 10K+ chunks
- **Embedding Speed**: ~3-4 seconds per chunk (sequential, local)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Ollama](https://ollama.com/) for local LLM inference
- [hnswlib](https://github.com/nmslib/hnswlib) for fast vector search
- [nomic-embed-text](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) for embeddings
