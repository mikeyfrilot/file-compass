"""
Performance benchmarks for file-compass operations.

Establishes baseline metrics for regression detection and performance monitoring.
Tests measure actual wall-clock time for critical operations.
"""

import tempfile
from pathlib import Path

import pytest

from file_compass.chunker import FileChunker
from file_compass.scanner import FileScanner
from file_compass.quick_index import QuickIndex


# Performance grade thresholds (in seconds)
GRADES = {
    "EXCELLENT": 0.010,      # < 10ms
    "GOOD": 0.050,            # < 50ms
    "FAIR": 0.100,            # < 100ms
    "POOR": 1.000,            # < 1s
}


def get_performance_grade(elapsed_time):
    """Determine performance grade based on elapsed time."""
    if elapsed_time < GRADES["EXCELLENT"]:
        return "EXCELLENT"
    elif elapsed_time < GRADES["GOOD"]:
        return "GOOD"
    elif elapsed_time < GRADES["FAIR"]:
        return "FAIR"
    else:
        return "POOR"


class TestScannerPerformance:
    """Benchmarks for file scanning operations."""

    @pytest.mark.benchmark
    def test_scan_100_files(self, benchmark):
        """Benchmark: Scanning 100 files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create 100 small Python files
            for i in range(100):
                file_path = tmpdir_path / f"module_{i}.py"
                file_path.write_text(f"def func_{i}():\n    pass\n")
            
            scanner = FileScanner([tmpdir])
            
            def scan_op():
                return list(scanner.scan_all())
            
            result = benchmark(scan_op)
            assert len(result) == 100
    
    @pytest.mark.benchmark
    def test_scan_1000_files(self, benchmark):
        """Benchmark: Scanning 1000 files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create 1000 small files
            for i in range(1000):
                file_path = tmpdir_path / f"file_{i:04d}.py"
                file_path.write_text(f"# File {i}\npass\n")
            
            scanner = FileScanner([tmpdir])
            
            def scan_op():
                return list(scanner.scan_all())
            
            result = benchmark(scan_op)
            assert len(result) == 1000


class TestChunkingPerformance:
    """Benchmarks for file chunking."""

    @pytest.mark.benchmark
    def test_chunking_small_file(self, benchmark):
        """Benchmark: Chunking a small Python file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            test_file = tmpdir_path / "test.py"
            
            code = """
def function1():
    '''Docstring'''
    return 42

class MyClass:
    def method(self):
        pass

def function2(x, y):
    return x + y
"""
            test_file.write_text(code)
            chunker = FileChunker()
            
            def chunk_op():
                return chunker.chunk_file(test_file)
            
            result = benchmark(chunk_op)
            assert len(result) >= 1

    @pytest.mark.benchmark
    def test_chunking_medium_file(self, benchmark):
        """Benchmark: Chunking a 500-line Python file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            test_file = tmpdir_path / "large.py"
            
            lines = ["# Generated test file\n"]
            for i in range(50):
                lines.append(f"""
def function_{i}(arg1, arg2):
    '''Function {i} docstring'''
    return arg1 + arg2

class Class_{i}:
    def method_a(self):
        pass
    
    def method_b(self, x):
        return x * 2
""")
            code = "".join(lines)
            test_file.write_text(code)
            chunker = FileChunker()
            
            def chunk_op():
                return chunker.chunk_file(test_file)
            
            result = benchmark(chunk_op)
            assert len(result) > 0


class TestQuickIndexPerformance:
    """Benchmarks for quick index operations."""

    @pytest.mark.benchmark
    def test_quick_index_build_100_files(self, benchmark):
        """Benchmark: Building quick index on 100 files."""
        import asyncio
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create 100 small Python files
            for i in range(100):
                (tmpdir_path / f"module_{i}.py").write_text(f"def function_{i}():\n    pass\n")
            
            def build_op():
                quick_index = QuickIndex()
                asyncio.run(quick_index.build_quick_index([tmpdir]))
                return quick_index
            
            result = benchmark(build_op)
            assert result is not None

    @pytest.mark.benchmark
    def test_quick_index_search_100(self, benchmark):
        """Benchmark: Quick search with 100 files indexed."""
        import asyncio
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create 100 small Python files
            for i in range(100):
                (tmpdir_path / f"module_{i}.py").write_text(f"def function_{i}():\n    pass\n")
            
            quick_index = QuickIndex()
            asyncio.run(quick_index.build_quick_index([tmpdir]))
            
            def search_op():
                return quick_index.search("function", 10)
            
            result = benchmark(search_op)
            assert isinstance(result, list)


class TestImportPerformance:
    """Benchmarks for module import times."""

    @pytest.mark.benchmark
    def test_file_compass_import(self, benchmark):
        """Benchmark: file_compass package import."""
        import sys
        
        # Remove from cache if present
        modules_to_remove = [m for m in sys.modules if m.startswith('file_compass')]
        for m in modules_to_remove:
            del sys.modules[m]
        
        def import_op():
            import file_compass
            return file_compass
        
        benchmark(import_op)

    @pytest.mark.benchmark
    def test_scanner_import(self, benchmark):
        """Benchmark: Scanner module import."""
        import sys
        
        modules_to_remove = [m for m in sys.modules if 'scanner' in m or 'file_compass' in m]
        for m in modules_to_remove:
            del sys.modules[m]
        
        def import_op():
            from file_compass.scanner import FileScanner
            return FileScanner
        
        benchmark(import_op)

    @pytest.mark.benchmark
    def test_quick_index_import(self, benchmark):
        """Benchmark: Quick index module import."""
        import sys
        
        modules_to_remove = [m for m in sys.modules if 'quick_index' in m or 'file_compass' in m]
        for m in modules_to_remove:
            del sys.modules[m]
        
        def import_op():
            from file_compass.quick_index import QuickIndex
            return QuickIndex
        
        benchmark(import_op)
