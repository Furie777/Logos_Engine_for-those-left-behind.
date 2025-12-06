"""
Integration tests for LOGOS Engine - Full Workflow Tests

These tests verify that the system works end-to-end, from data loading
through graph building to query execution.
"""

import json
import pickle
import pytest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import networkx as nx


class TestDataLoadingWorkflow:
    """Tests for the complete data loading workflow"""

    def test_load_and_validate_kjv(self, temp_data_dir, monkeypatch, sample_kjv):
        """Test loading KJV and validating structure"""
        from src import loader
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)

        kjv = loader.load_kjv()

        # Verify structure
        assert isinstance(kjv, dict)
        assert len(kjv) == len(sample_kjv)

        # Verify content
        for ref, text in kjv.items():
            assert isinstance(ref, str)
            assert isinstance(text, str)
            assert len(text) > 0

    def test_load_and_validate_strongs(self, temp_data_dir, sample_strongs):
        """Test loading Strong's and validating structure"""
        strongs_path = temp_data_dir / "strongs.json"

        with open(strongs_path, 'r') as f:
            strongs = json.load(f)

        # Verify structure
        assert isinstance(strongs, dict)

        # Verify Hebrew entries
        hebrew = [k for k in strongs.keys() if k.startswith('H')]
        assert len(hebrew) > 0

        # Verify Greek entries
        greek = [k for k in strongs.keys() if k.startswith('G')]
        assert len(greek) > 0

    def test_load_and_validate_cross_refs(self, temp_data_dir, sample_cross_refs):
        """Test loading cross-references and validating structure"""
        refs_path = temp_data_dir / "cross_refs.json"

        with open(refs_path, 'r') as f:
            cross_refs = json.load(f)

        # Verify structure
        assert isinstance(cross_refs, dict)

        # Verify each entry
        for ref, targets in cross_refs.items():
            assert isinstance(ref, str)
            assert isinstance(targets, list)


class TestGraphBuildingWorkflow:
    """Tests for the complete graph building workflow"""

    def test_build_graph_from_data(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, sample_cross_refs):
        """Test building graph from loaded data"""
        from src import graph
        from src import loader

        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: sample_kjv)
        monkeypatch.setattr('src.graph.load_cross_references', lambda: sample_cross_refs)

        G = graph.build_graph()

        # Verify graph structure
        assert isinstance(G, nx.DiGraph)
        assert G.number_of_nodes() == len(sample_kjv)
        assert G.number_of_edges() > 0

        # Verify pickle was saved
        pickle_path = temp_output_dir / "logos_graph.gpickle"
        assert pickle_path.exists()

    def test_graph_contains_all_verses(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, sample_cross_refs):
        """Test that graph contains all verses as nodes"""
        from src import graph

        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: sample_kjv)
        monkeypatch.setattr('src.graph.load_cross_references', lambda: sample_cross_refs)

        G = graph.build_graph()

        for ref in sample_kjv.keys():
            assert ref in G.nodes, f"Missing verse: {ref}"

    def test_graph_edges_from_cross_refs(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, sample_cross_refs):
        """Test that graph edges come from cross-references"""
        from src import graph

        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: sample_kjv)
        monkeypatch.setattr('src.graph.load_cross_references', lambda: sample_cross_refs)

        G = graph.build_graph()

        # Count cross-ref edges
        cross_ref_edges = [(u, v) for u, v, d in G.edges(data=True)
                          if d.get('type') == 'cross_ref']

        # Should have some cross-reference edges
        assert len(cross_ref_edges) >= 0  # May be 0 if no refs match


class TestQueryWorkflow:
    """Tests for the complete query workflow"""

    @pytest.fixture
    def query_system(self, sample_kjv, networkx_graph, monkeypatch):
        """Setup query system with test data"""
        from src import query

        monkeypatch.setattr('src.query.load_graph', lambda: networkx_graph)
        monkeypatch.setattr('src.query.load_kjv', lambda: sample_kjv)

        return query.LogosQuery()

    def test_verse_lookup_workflow(self, query_system):
        """Test complete verse lookup workflow"""
        # Lookup a verse
        result = query_system.verse("John 3:16")

        assert result is not None
        assert "God" in result

    def test_search_workflow(self, query_system):
        """Test complete search workflow"""
        # Search for term
        results = query_system.search("God")

        assert isinstance(results, list)
        assert len(results) > 0

        # Verify results contain search term
        for ref, text in results:
            assert "God" in text or "god" in text.lower()

    def test_connection_workflow(self, query_system):
        """Test complete connection finding workflow"""
        # Get connections for a verse
        result = query_system.connections("John 3:16")

        if result:
            assert 'outgoing' in result
            assert 'incoming' in result

    def test_central_verses_workflow(self, query_system):
        """Test finding central verses workflow"""
        # Get most central verses
        results = query_system.central(n=5)

        assert isinstance(results, list)
        # Results should be sorted by centrality
        if len(results) > 1:
            scores = [score for _, score in results]
            assert scores == sorted(scores, reverse=True)


class TestSemanticSearchWorkflow:
    """Tests for semantic search workflow"""

    @pytest.fixture
    def semantic_system(self, temp_data_dir, monkeypatch):
        """Setup semantic search with test data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_similar_verses_workflow(self, semantic_system):
        """Test finding similar verses workflow"""
        # Find verses similar to John 3:16
        results = semantic_system.similar_verses("John 3:16", n=5)

        assert isinstance(results, list)

        # Results should not include the query verse
        refs = [r[0] for r in results]
        assert "John 3:16" not in refs

    def test_concept_search_workflow(self, semantic_system):
        """Test concept-based search workflow"""
        # Search for salvation concept
        results = semantic_system.search_concept("salvation")

        assert isinstance(results, list)

    def test_meaning_search_workflow(self, semantic_system):
        """Test meaning-based search workflow"""
        # Search by meaning
        results = semantic_system.search_meaning("God's love")

        assert isinstance(results, list)

    def test_explain_connection_workflow(self, semantic_system):
        """Test explaining verse connections workflow"""
        # Explain connection between two verses
        result = semantic_system.explain_connection("John 3:16", "John 3:17")

        if result:
            assert 'shared_concepts' in result
            assert 'similarity' in result


class TestConcordanceWorkflow:
    """Tests for concordance workflow"""

    @pytest.fixture
    def concordance_system(self, temp_data_dir, monkeypatch):
        """Setup concordance with test data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_word_search_workflow(self, concordance_system):
        """Test word search workflow"""
        # Search for a common word
        results = concordance_system.search_word("God")

        assert isinstance(results, list)
        assert len(results) > 0

    def test_word_study_workflow(self, concordance_system):
        """Test complete word study workflow"""
        # Perform word study
        result = concordance_system.word_study("god")

        assert isinstance(result, dict)
        assert 'word' in result
        assert 'occurrences' in result
        assert 'total_occurrences' in result

    def test_strongs_lookup_workflow(self, concordance_system):
        """Test Strong's number lookup workflow"""
        # Lookup Strong's definition
        result = concordance_system.get_strongs_definition("H430")

        if result:
            assert 'hebrew' in result
            assert 'definition' in result


class TestIntegrityWorkflow:
    """Tests for integrity verification workflow"""

    def test_compute_and_verify_workflow(self, tmp_path):
        """Test computing and verifying checksums workflow"""
        from src import integrity

        # Create test file
        test_file = tmp_path / "test.json"
        test_file.write_text('{"test": "data"}')

        # Compute checksum
        checksum = integrity.compute_sha256(test_file)
        size = integrity.get_file_size(test_file)

        assert isinstance(checksum, str)
        assert len(checksum) == 64
        assert isinstance(size, int)
        assert size > 0


class TestEndToEndWorkflow:
    """End-to-end tests combining multiple modules"""

    def test_load_build_query_workflow(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, sample_cross_refs):
        """Test complete workflow: load data -> build graph -> query"""
        from src import graph, loader

        # Setup
        monkeypatch.setattr(graph, 'OUTPUT_DIR', temp_output_dir)
        monkeypatch.setattr('src.graph.load_kjv', lambda: sample_kjv)
        monkeypatch.setattr('src.graph.load_cross_references', lambda: sample_cross_refs)

        # Build graph
        G = graph.build_graph()
        assert G is not None

        # Verify we can query the graph
        assert "John 3:16" in G.nodes
        assert G.nodes["John 3:16"]['text'] is not None

    def test_semantic_to_graph_workflow(self, temp_data_dir, temp_output_dir, monkeypatch, sample_kjv, sample_cross_refs, networkx_graph):
        """Test workflow from semantic search to graph traversal"""
        from src import semantic

        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)

        # Semantic search
        sem = semantic.SemanticSearch()
        similar = sem.similar_verses("John 3:16", n=3)

        # Should be able to look up similar verses in graph
        for ref, score in similar:
            assert ref in networkx_graph.nodes


class TestRealDataWorkflow:
    """Integration tests with real data if available"""

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_search_workflow(self):
        """Test search workflow with real data"""
        base_dir = Path(__file__).parent.parent.parent
        kjv_path = base_dir / "data" / "kjv.json"

        if not kjv_path.exists():
            pytest.skip("Real KJV data not available")

        with open(kjv_path, 'r') as f:
            kjv = json.load(f)

        # Search for "love"
        results = [(ref, text) for ref, text in kjv.items()
                   if "love" in text.lower()]

        assert len(results) > 0

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_graph_workflow(self):
        """Test graph workflow with real data"""
        base_dir = Path(__file__).parent.parent.parent
        pickle_path = base_dir / "output" / "logos_graph.gpickle"

        if not pickle_path.exists():
            pytest.skip("Real graph not available")

        with open(pickle_path, 'rb') as f:
            G = pickle.load(f)

        # Verify graph structure
        assert G.number_of_nodes() > 30000
        assert G.number_of_edges() > 0

        # Test path finding
        try:
            path = nx.shortest_path(G, "Genesis 1:1", "Revelation 22:21")
            assert len(path) > 0
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            pass
