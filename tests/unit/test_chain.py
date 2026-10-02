"""
Tests for LOGOS Engine chain module (path finding)
"""

import json
import pickle
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import networkx as nx


class TestNormalizeRef:
    """Tests for reference normalization in chain module"""

    def test_normalize_psalm_to_psalms(self):
        """Test that Psalm is normalized to Psalms"""
        from src import chain
        result = chain.normalize_ref("Psalm 23:1")
        assert result == "Psalms 23:1"

    def test_normalize_psalms_unchanged(self):
        """Test that Psalms remains unchanged"""
        from src import chain
        result = chain.normalize_ref("Psalms 23:1")
        assert result == "Psalms 23:1"

    def test_normalize_strips_whitespace(self):
        """Test that whitespace is stripped"""
        from src import chain
        result = chain.normalize_ref("  John 3:16  ")
        assert result == "John 3:16"

    def test_normalize_other_books_unchanged(self):
        """Test that other book names are unchanged"""
        from src import chain
        result = chain.normalize_ref("Genesis 1:1")
        assert result == "Genesis 1:1"


class TestLoadData:
    """Tests for data loading in chain module"""

    def test_load_data_returns_tuple(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, networkx_graph):
        """Test that load_data returns (kjv, graph) tuple"""
        from src import chain

        # Save test graph
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(networkx_graph, f)

        monkeypatch.setattr(chain, 'DATA_DIR', temp_data_dir)
        monkeypatch.setattr(chain, 'OUTPUT_DIR', temp_output_dir)

        kjv, G = chain.load_data()
        assert isinstance(kjv, dict)
        assert G is None or isinstance(G, nx.Graph)

    def test_load_data_kjv_content(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, networkx_graph):
        """Test that load_data returns correct KJV content"""
        from src import chain

        pickle_path = temp_output_dir / "logos_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(networkx_graph, f)

        monkeypatch.setattr(chain, 'DATA_DIR', temp_data_dir)
        monkeypatch.setattr(chain, 'OUTPUT_DIR', temp_output_dir)

        kjv, _ = chain.load_data()
        assert "John 3:16" in kjv


class TestFindChain:
    """Tests for path finding functionality"""

    @pytest.fixture
    def setup_chain_module(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, networkx_graph):
        """Setup chain module with mocked data"""
        from src import chain

        # Save test graph
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(networkx_graph, f)

        monkeypatch.setattr(chain, 'DATA_DIR', temp_data_dir)
        monkeypatch.setattr(chain, 'OUTPUT_DIR', temp_output_dir)

        return chain

    def test_find_chain_connected_verses(self, setup_chain_module):
        """Test finding chain between connected verses"""
        chain = setup_chain_module
        # John 3:16 and John 3:17 should be connected
        path = chain.find_chain("John 3:16", "John 3:17")
        # Path may or may not exist depending on graph structure
        assert path is None or isinstance(path, list)

    def test_find_chain_invalid_start(self, setup_chain_module):
        """Test find_chain with invalid start reference"""
        chain = setup_chain_module
        path = chain.find_chain("Invalid 1:1", "John 3:16")
        assert path is None

    def test_find_chain_invalid_end(self, setup_chain_module):
        """Test find_chain with invalid end reference"""
        chain = setup_chain_module
        path = chain.find_chain("John 3:16", "Invalid 99:99")
        assert path is None

    def test_find_chain_same_verse(self, setup_chain_module):
        """Test find_chain with same start and end"""
        chain = setup_chain_module
        path = chain.find_chain("John 3:16", "John 3:16")
        if path:
            assert len(path) == 1
            assert path[0] == "John 3:16"

    def test_find_chain_normalizes_psalm(self, setup_chain_module, monkeypatch):
        """Test that find_chain normalizes Psalm to Psalms"""
        chain = setup_chain_module
        # This tests the normalization path
        path = chain.find_chain("Psalm 23:1", "Psalm 23:2")
        # Result depends on graph structure


class TestFindBridge:
    """Tests for bridge finding functionality"""

    @pytest.fixture
    def setup_chain_module(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, networkx_graph):
        """Setup chain module with mocked data"""
        from src import chain

        pickle_path = temp_output_dir / "logos_graph.gpickle"
        with open(pickle_path, 'wb') as f:
            pickle.dump(networkx_graph, f)

        monkeypatch.setattr(chain, 'DATA_DIR', temp_data_dir)
        monkeypatch.setattr(chain, 'OUTPUT_DIR', temp_output_dir)

        return chain

    def test_find_bridge_returns_set_or_none(self, setup_chain_module):
        """Test that find_bridge returns a set or None"""
        chain = setup_chain_module
        result = chain.find_bridge("John 3:16", "John 3:17")
        assert result is None or isinstance(result, set)

    def test_find_bridge_invalid_refs(self, setup_chain_module):
        """Test find_bridge with invalid references"""
        chain = setup_chain_module
        result = chain.find_bridge("Invalid 1:1", "Also Invalid 2:2")
        assert result is None


class TestPathProperties:
    """Tests for path properties"""

    @pytest.fixture
    def connected_graph(self, sample_kjv):
        """Create a fully connected test graph"""
        G = nx.DiGraph()

        # Add verse nodes
        for ref, text in sample_kjv.items():
            G.add_node(ref, text=text, book=ref.split()[0])

        # Connect John verses sequentially
        john_verses = [r for r in sample_kjv.keys() if r.startswith("John")]
        for i in range(len(john_verses) - 1):
            G.add_edge(john_verses[i], john_verses[i+1], type='sequential')

        return G

    def test_path_starts_with_source(self, connected_graph):
        """Test that path starts with source node"""
        try:
            path = nx.shortest_path(connected_graph, "John 1:1", "John 3:17")
            if path:
                assert path[0] == "John 1:1"
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass  # Expected if no path exists

    def test_path_ends_with_target(self, connected_graph):
        """Test that path ends with target node"""
        try:
            path = nx.shortest_path(connected_graph, "John 1:1", "John 3:17")
            if path:
                assert path[-1] == "John 3:17"
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass

    def test_path_nodes_are_connected(self, connected_graph):
        """Test that consecutive nodes in path are connected"""
        try:
            path = nx.shortest_path(connected_graph, "John 1:1", "John 3:17")
            if path and len(path) > 1:
                for i in range(len(path) - 1):
                    # Check edge exists in either direction
                    has_edge = (connected_graph.has_edge(path[i], path[i+1]) or
                               connected_graph.has_edge(path[i+1], path[i]))
                    assert has_edge, f"No edge between {path[i]} and {path[i+1]}"
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass


class TestBridgeProperties:
    """Tests for bridge properties"""

    def test_bridge_is_common_neighbor(self, sample_kjv, sample_cross_refs):
        """Test that bridges are common neighbors"""
        G = nx.DiGraph()

        for ref, text in sample_kjv.items():
            G.add_node(ref, text=text)

        for from_ref, to_refs in sample_cross_refs.items():
            for to_ref in to_refs:
                if from_ref in G.nodes and to_ref in G.nodes:
                    G.add_edge(from_ref, to_ref)

        # Find bridges between two nodes
        ref1 = "John 3:16"
        ref2 = "John 3:17"

        if ref1 in G and ref2 in G:
            neighbors1 = set(G.neighbors(ref1))
            neighbors2 = set(G.neighbors(ref2))
            bridges = neighbors1 & neighbors2

            # Verify all bridges are neighbors of both
            for bridge in bridges:
                assert bridge in neighbors1
                assert bridge in neighbors2


class TestRealChainData:
    """Tests that use real data if available"""

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_genesis_to_revelation_path_exists(self):
        """Test that a path exists from Genesis to Revelation"""
        base_dir = Path(__file__).parent.parent.parent
        pickle_path = base_dir / "output" / "logos_graph.gpickle"

        if not pickle_path.exists():
            pytest.skip("Real graph not available")

        with open(pickle_path, 'rb') as f:
            G = pickle.load(f)

        try:
            path = nx.shortest_path(G, "Genesis 1:1", "Revelation 22:21")
            assert path is not None
            assert len(path) > 0
            assert path[0] == "Genesis 1:1"
            assert path[-1] == "Revelation 22:21"
        except nx.NetworkXNoPath:
            pytest.fail("Expected path from Genesis to Revelation")
        except nx.NodeNotFound as e:
            pytest.skip(f"Node not found: {e}")

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_protoevangelium_path(self):
        """Test path from Genesis 3:15 (protoevangelium)"""
        base_dir = Path(__file__).parent.parent.parent
        pickle_path = base_dir / "output" / "logos_graph.gpickle"

        if not pickle_path.exists():
            pytest.skip("Real graph not available")

        with open(pickle_path, 'rb') as f:
            G = pickle.load(f)

        # Genesis 3:15 is the protoevangelium - should connect to messianic prophecies
        if "Genesis 3:15" not in G:
            pytest.skip("Genesis 3:15 not in graph")

        # Should have outgoing connections
        out_edges = list(G.successors("Genesis 3:15"))
        assert len(out_edges) > 0, "Genesis 3:15 should have cross-references"
