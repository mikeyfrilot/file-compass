"""
File Compass Gateway - MCP Server for Semantic File Search

A semantic search gateway for files on your workstation.
Uses HNSW indexing with nomic-embed-text embeddings.

Usage:
    python gateway.py              # Start MCP server
    python gateway.py --index      # Build index for F:/AI
    python gateway.py --test       # Run test queries
"""

import asyncio
import argparse
import logging
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path

# MCP imports
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("FastMCP not installed. Install with: pip install mcp", file=sys.stderr)
    raise

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from file_compass.indexer import FileIndex, SearchResult, get_index
from file_compass.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("file-compass")

# Global state
_index: Optional[FileIndex] = None
_index_lock = asyncio.Lock()


async def get_index_instance() -> FileIndex:
    """Get or initialize the file index."""
    global _index

    if _index is not None:
        return _index

    async with _index_lock:
        if _index is not None:
            return _index

        _index = FileIndex()
        # Load existing index if available
        if _index.index_path.exists():
            _index._get_index()  # Load HNSW
            _index._get_conn()   # Load SQLite

        return _index


# =============================================================================
# MCP TOOLS
# =============================================================================

@mcp.tool()
async def file_search(
    query: str,
    top_k: int = 10,
    file_types: Optional[str] = None,
    directory: Optional[str] = None,
    git_only: bool = False,
    min_relevance: float = 0.3
) -> Dict[str, Any]:
    """
    Search for files using semantic search.

    Finds files and code chunks that match your query conceptually,
    not just by keywords. Great for finding:
    - Code that implements specific functionality
    - Files related to a topic or concept
    - Functions, classes, or sections by description

    Args:
        query: Natural language description of what you're looking for
               Examples: "training loop", "database connection", "error handling"
        top_k: Maximum number of results (1-50, default 10)
        file_types: Comma-separated file types (e.g., "python,markdown")
        directory: Only search within this directory path
        git_only: Only return git-tracked files
        min_relevance: Minimum relevance score (0-1, default 0.3)

    Returns:
        Matching files and chunks with paths, line numbers, and previews
    """
    index = await get_index_instance()

    # Check if index exists
    status = index.get_status()
    if status["files_indexed"] == 0:
        return {
            "error": "No files indexed yet",
            "hint": "Run: python -m file_compass.cli index -d \"F:/AI\""
        }

    # Parse file_types
    types_list = None
    if file_types:
        types_list = [t.strip() for t in file_types.split(",")]

    # Clamp top_k
    top_k = max(1, min(50, top_k))

    # Search
    results = await index.search(
        query=query,
        top_k=top_k,
        file_types=types_list,
        directory=directory,
        git_only=git_only,
        min_relevance=min_relevance
    )

    # Format results
    matches = []
    for r in results:
        matches.append({
            "path": r.path,
            "relative_path": r.relative_path,
            "file_type": r.file_type,
            "chunk_type": r.chunk_type,
            "chunk_name": r.chunk_name,
            "lines": f"{r.line_start}-{r.line_end}",
            "relevance": round(r.relevance, 3),
            "preview": r.preview[:200] + "..." if len(r.preview) > 200 else r.preview,
            "git_tracked": r.git_tracked
        })

    return {
        "query": query,
        "results": matches,
        "count": len(matches),
        "total_indexed": status["files_indexed"],
        "hint": f"Found {len(matches)} results. Use Read tool to view full content."
    }


@mcp.tool()
async def file_preview(
    path: str,
    line_start: Optional[int] = None,
    line_end: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get content preview from a specific file.

    Args:
        path: Full path to the file
        line_start: Starting line number (1-indexed, optional)
        line_end: Ending line number (optional)

    Returns:
        File content for the specified lines
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            return {"error": f"File not found: {path}"}

        content = file_path.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")

        # Apply line range
        if line_start is not None:
            start_idx = max(0, line_start - 1)
            end_idx = line_end if line_end else len(lines)
            lines = lines[start_idx:end_idx]
            line_offset = start_idx + 1
        else:
            line_offset = 1

        # Format with line numbers
        numbered_lines = []
        for i, line in enumerate(lines[:100]):  # Limit to 100 lines
            numbered_lines.append(f"{line_offset + i:4d} | {line}")

        preview = "\n".join(numbered_lines)
        if len(lines) > 100:
            preview += f"\n... ({len(lines) - 100} more lines)"

        return {
            "path": path,
            "lines": f"{line_offset}-{line_offset + len(numbered_lines) - 1}",
            "content": preview,
            "total_lines": len(content.split("\n"))
        }

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def file_index_status() -> Dict[str, Any]:
    """
    Get the current status of the file index.

    Returns:
        Index statistics including file counts, types, and last build time
    """
    index = await get_index_instance()
    status = index.get_status()

    return {
        "files_indexed": status["files_indexed"],
        "chunks_indexed": status["chunks_indexed"],
        "index_size_mb": round(status["index_size_mb"], 2),
        "last_build": status["last_build"],
        "file_types": status["file_types"],
        "hint": "Use file_search() to find files, or file_index_scan() to rebuild"
    }


@mcp.tool()
async def file_index_scan(
    directories: Optional[str] = None,
    force_rebuild: bool = False
) -> Dict[str, Any]:
    """
    Scan directories and build/rebuild the file index.

    This is a long-running operation that:
    1. Scans directories for code files
    2. Chunks files into semantic pieces
    3. Generates embeddings via Ollama
    4. Builds HNSW search index

    Args:
        directories: Comma-separated directory paths (default: F:/AI)
        force_rebuild: If True, rebuilds entire index even if files haven't changed

    Returns:
        Statistics about the indexing process
    """
    index = await get_index_instance()
    config = get_config()

    # Parse directories
    if directories:
        dir_list = [d.strip() for d in directories.split(",")]
    else:
        dir_list = config.directories

    try:
        stats = await index.build_index(
            directories=dir_list,
            show_progress=False  # Can't show progress over MCP
        )

        return {
            "success": True,
            "files_indexed": stats["files_indexed"],
            "chunks_indexed": stats["chunks_indexed"],
            "duration_seconds": round(stats["duration_seconds"], 1),
            "directories": dir_list,
            "hint": "Index built! Use file_search() to find files."
        }

    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "hint": "Make sure Ollama is running with nomic-embed-text model"
        }


# =============================================================================
# CLI COMMANDS
# =============================================================================

async def build_index_cli(directories: List[str]):
    """Build index from CLI."""
    print("Building File Compass index...")
    print("=" * 50)

    index = FileIndex()

    stats = await index.build_index(
        directories=directories,
        show_progress=True
    )

    print("\nIndex built successfully!")
    print(f"  Files: {stats['files_indexed']}")
    print(f"  Chunks: {stats['chunks_indexed']}")
    print(f"  Duration: {stats['duration_seconds']:.1f}s")

    await index.close()


async def run_tests():
    """Run test queries."""
    print("\n" + "=" * 60)
    print("FILE COMPASS - TEST SUITE")
    print("=" * 60)

    index = FileIndex()
    status = index.get_status()

    print(f"\nIndex: {status['files_indexed']} files, {status['chunks_indexed']} chunks")

    test_queries = [
        "embedding generation",
        "file scanner",
        "HNSW index",
        "configuration settings",
        "async function",
    ]

    print("\n" + "-" * 60)
    print("Semantic Search Tests")
    print("-" * 60)

    for query in test_queries:
        results = await index.search(query, top_k=3)

        print(f"\nQuery: '{query}'")
        if results:
            for r in results:
                print(f"  [{r.relevance:.1%}] {r.relative_path}")
                print(f"         {r.chunk_type}: {r.chunk_name or 'unnamed'} (L{r.line_start}-{r.line_end})")
        else:
            print("  No results")

    await index.close()


def main():
    parser = argparse.ArgumentParser(
        description="File Compass - Semantic File Search MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gateway.py              Start MCP server
  python gateway.py --index      Build index for F:/AI
  python gateway.py --test       Run test queries
        """
    )
    parser.add_argument("--index", action="store_true", help="Build search index")
    parser.add_argument("--test", action="store_true", help="Run test queries")
    parser.add_argument("-d", "--directories", nargs="+", help="Directories to index")

    args = parser.parse_args()

    if args.index:
        dirs = args.directories or ["F:/AI"]
        asyncio.run(build_index_cli(dirs))
    elif args.test:
        asyncio.run(run_tests())
    else:
        # Start MCP server
        print("Starting File Compass MCP Server...", file=sys.stderr)
        print("Tools: file_search, file_preview, file_index_status, file_index_scan", file=sys.stderr)
        mcp.run()


if __name__ == "__main__":
    main()
