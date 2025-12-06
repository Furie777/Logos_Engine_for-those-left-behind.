"""
LOGOS Engine Test Configuration
Pytest fixtures for testing Scripture analysis system
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add src directory to path for imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "src"))

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_kjv():
    """Load sample KJV verses for testing"""
    with open(FIXTURES_DIR / "sample_kjv.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def sample_strongs():
    """Load sample Strong's definitions for testing"""
    with open(FIXTURES_DIR / "sample_strongs.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def sample_cross_refs():
    """Load sample cross-references for testing"""
    with open(FIXTURES_DIR / "sample_cross_refs.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def temp_data_dir(tmp_path, sample_kjv, sample_strongs, sample_cross_refs):
    """
    Create a temporary data directory with sample data files.
    Returns the path to the temporary data directory.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Write sample files
    with open(data_dir / "kjv.json", 'w') as f:
        json.dump(sample_kjv, f)

    with open(data_dir / "strongs.json", 'w') as f:
        json.dump(sample_strongs, f)

    with open(data_dir / "cross_refs.json", 'w') as f:
        json.dump(sample_cross_refs, f)

    return data_dir


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_data_paths(monkeypatch, temp_data_dir, temp_output_dir):
    """
    Monkeypatch the DATA_DIR and OUTPUT_DIR paths in modules
    to use temporary directories for testing.
    """
    # This fixture allows tests to run without modifying actual data
    return {
        'data_dir': temp_data_dir,
        'output_dir': temp_output_dir
    }


@pytest.fixture
def real_kjv():
    """
    Load the real KJV data if available.
    Skip test if not available.
    """
    kjv_path = ROOT_DIR / "data" / "kjv.json"
    if not kjv_path.exists():
        pytest.skip("Real KJV data not available")

    with open(kjv_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def real_strongs():
    """
    Load the real Strong's data if available.
    Skip test if not available.
    """
    strongs_path = ROOT_DIR / "data" / "strongs.json"
    if not strongs_path.exists():
        pytest.skip("Real Strong's data not available")

    with open(strongs_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def real_cross_refs():
    """
    Load the real cross-references if available.
    Skip test if not available.
    """
    refs_path = ROOT_DIR / "data" / "cross_refs.json"
    if not refs_path.exists():
        pytest.skip("Real cross-references not available")

    with open(refs_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def networkx_graph(sample_kjv, sample_cross_refs):
    """Create a NetworkX graph from sample data for testing"""
    import networkx as nx

    G = nx.DiGraph()

    # Add verse nodes
    for ref, text in sample_kjv.items():
        G.add_node(ref, text=text, book=ref.split()[0])

    # Add cross-reference edges
    for from_ref, to_refs in sample_cross_refs.items():
        for to_ref in to_refs:
            if from_ref in G.nodes and to_ref in G.nodes:
                G.add_edge(from_ref, to_ref, type='cross_ref')

    return G


# Test markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "requires_real_data: marks tests that require real data files"
    )
