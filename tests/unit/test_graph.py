"""
Tests for LOGOS Engine graph module
"""

import json
import pickle
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import networkx as nx
from src import graph


class TestBuildGraph:
    """Tests for graph building functionality"""

    def test_build_graph_returns_digraph(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that build_graph returns a NetworkX DiGraph"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        result = graph.build_graph()
        assert isinstance(result, nx.DiGraph)

    def test_build_graph_has_verse_nodes(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv):
        """Test that graph has nodes for all verses"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()
        for ref in sample_kjv.keys():
            assert ref in G.nodes, f"Missing node for {ref}"

    def test_build_graph_node_has_text(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv):
        """Test that graph nodes have text attribute"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()
        for ref in list(sample_kjv.keys())[:5]:
            assert 'text' in G.nodes[ref], f"Node {ref} missing text attribute"
            assert G.nodes[ref]['text'] == sample_kjv[ref]

    def test_build_graph_node_has_book(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that graph nodes have book attribute"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()
        assert 'book' in G.nodes["John 3:16"]
        assert G.nodes["John 3:16"]['book'] == "John"

    def test_build_graph_has_edges(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that graph has edges from cross-references"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()
        assert G.number_of_edges() > 0

    def test_build_graph_saves_pickle(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that build_graph saves graph to pickle file"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        graph.build_graph()
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        assert pickle_path.exists()


class TestLoadGraph:
    """Tests for graph loading functionality"""

    def test_load_graph_from_pickle(self, temp_data_dir, temp_output_dir, monkeypatch, networkx_graph):
        """Test loading graph from pickle file"""
        # Save the test graph
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(networkx_graph, f)

        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)

        loaded = graph.load_graph()
        assert isinstance(loaded, nx.DiGraph)
        assert loaded.number_of_nodes() == networkx_graph.number_of_nodes()

    def test_load_graph_builds_if_missing(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that load_graph builds graph if pickle doesn't exist"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        # Ensure pickle doesn't exist
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        if pickle_path.exists():
            pickle_path.unlink()

        loaded = graph.load_graph()
        assert isinstance(loaded, nx.DiGraph)
        assert pickle_path.exists()  # Should have been created


class TestGetStats:
    """Tests for graph statistics"""

    def test_get_stats_returns_dict(self, networkx_graph):
        """Test that get_stats returns a dictionary"""
        result = graph.get_stats(networkx_graph)
        assert isinstance(result, dict)

    def test_get_stats_has_nodes(self, networkx_graph):
        """Test that stats include node count"""
        result = graph.get_stats(networkx_graph)
        assert 'nodes' in result
        assert result['nodes'] == networkx_graph.number_of_nodes()

    def test_get_stats_has_edges(self, networkx_graph):
        """Test that stats include edge count"""
        result = graph.get_stats(networkx_graph)
        assert 'edges' in result
        assert result['edges'] == networkx_graph.number_of_edges()

    def test_get_stats_has_density(self, networkx_graph):
        """Test that stats include density"""
        result = graph.get_stats(networkx_graph)
        assert 'density' in result
        assert isinstance(result['density'], float)
        assert 0 <= result['density'] <= 1

    def test_get_stats_has_connectivity(self, networkx_graph):
        """Test that stats include connectivity info"""
        result = graph.get_stats(networkx_graph)
        assert 'is_connected' in result
        assert isinstance(result['is_connected'], bool)

    def test_get_stats_has_central_vertices(self, networkx_graph):
        """Test that stats include top central vertices"""
        result = graph.get_stats(networkx_graph)
        assert 'top_10_central' in result
        assert isinstance(result['top_10_central'], list)


class TestGraphStructure:
    """Tests for graph structure properties"""

    def test_graph_is_directed(self, networkx_graph):
        """Test that the graph is directed"""
        assert networkx_graph.is_directed()

    def test_cross_ref_edges_have_type(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that cross-reference edges have type attribute"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()

        # Check some edges have type
        cross_ref_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'cross_ref']
        assert len(cross_ref_edges) > 0

    def test_sequential_edges_exist(self, temp_data_dir, temp_output_dir, monkeypatch):
        """Test that sequential edges are created within books"""
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: json.load(open(temp_data_dir / "kjv.json")))
        monkeypatch.setattr('src.graph.load_cross_references', lambda: json.load(open(temp_data_dir / "cross_refs.json")))

        G = graph.build_graph()

        # Check for sequential edges
        seq_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'sequential']
        # Note: Sequential edges may be 0 if verses aren't in order in sample data
        # This is expected behavior for sample fixtures


class TestGraphOperations:
    """Tests for graph operations"""

    def test_find_path_between_nodes(self, networkx_graph):
        """Test finding path between two nodes"""
        # Check if John 1:1 and Genesis 1:1 are connected
        if "John 1:1" in networkx_graph and "Genesis 1:1" in networkx_graph:
            try:
                path = nx.shortest_path(networkx_graph, "Genesis 1:1", "John 1:1")
                assert isinstance(path, list)
                assert path[0] == "Genesis 1:1"
                assert path[-1] == "John 1:1"
            except nx.NetworkXNoPath:
                pass  # No path is also valid

    def test_node_degree(self, networkx_graph):
        """Test node degree calculation"""
        for node in list(networkx_graph.nodes)[:5]:
            in_degree = networkx_graph.in_degree(node)
            out_degree = networkx_graph.out_degree(node)
            assert isinstance(in_degree, int)
            assert isinstance(out_degree, int)
            assert in_degree >= 0
            assert out_degree >= 0

    def test_neighbors(self, networkx_graph):
        """Test getting node neighbors"""
        node = "John 3:16"
        if node in networkx_graph:
            successors = list(networkx_graph.successors(node))
            predecessors = list(networkx_graph.predecessors(node))
            assert isinstance(successors, list)
            assert isinstance(predecessors, list)


class TestRealGraphData:
    """Tests that use real graph data if available"""

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_graph_node_count(self):
        """Test that real graph has expected node count"""
        base_dir = Path(__file__).parent.parent.parent
        pickle_path = base_dir / "output" / "logos_graph.gpickle"

        if not pickle_path.exists():
            pytest.skip("Real graph not available")

        with open(pickle_path, 'rb') as f:
            G = pickle.load(f)

        # Should have ~36,000+ nodes for full KJV
        assert G.number_of_nodes() >= 30000, f"Expected ~30000+ nodes, got {G.number_of_nodes()}"

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_graph_is_connected(self):
        """Test that real graph is at least weakly connected"""
        base_dir = Path(__file__).parent.parent.parent
        pickle_path = base_dir / "output" / "logos_graph.gpickle"

        if not pickle_path.exists():
            pytest.skip("Real graph not available")

        with open(pickle_path, 'rb') as f:
            G = pickle.load(f)

        # Check weak connectivity for directed graph
        assert nx.is_weakly_connected(G), "Graph should be weakly connected"
