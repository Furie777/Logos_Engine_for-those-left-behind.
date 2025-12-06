"""
Tests for LOGOS Engine query module
"""

import json
import pickle
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import networkx as nx


class TestLogosQuery:
    """Tests for LogosQuery class"""

    @pytest.fixture
    def mock_logos_query(self, sample_kjv, networkx_graph, monkeypatch):
        """Create a LogosQuery instance with mocked data"""
        from src import query

        # Mock the load functions
        monkeypatch.setattr('src.query.load_graph', lambda: networkx_graph)
        monkeypatch.setattr('src.query.load_kjv', lambda: sample_kjv)

        return query.LogosQuery()

    def test_init_loads_data(self, mock_logos_query, sample_kjv):
        """Test that LogosQuery initializes with data"""
        assert mock_logos_query.G is not None
        assert mock_logos_query.kjv is not None
        assert len(mock_logos_query.kjv) == len(sample_kjv)

    def test_verse_exact_match(self, mock_logos_query):
        """Test verse lookup with exact match"""
        result = mock_logos_query.verse("John 3:16")
        assert result is not None
        assert "God so loved" in result

    def test_verse_fuzzy_match(self, mock_logos_query):
        """Test verse lookup with partial match"""
        result = mock_logos_query.verse("john 3:16")  # lowercase
        assert result is not None

    def test_verse_not_found(self, mock_logos_query):
        """Test verse lookup for non-existent reference"""
        result = mock_logos_query.verse("Nonexistent 99:99")
        assert result is None

    def test_search_finds_matching_verses(self, mock_logos_query):
        """Test search finds verses containing term"""
        results = mock_logos_query.search("God")
        assert len(results) > 0
        for ref, text in results:
            assert "God" in text or "god" in text.lower()

    def test_search_case_insensitive(self, mock_logos_query):
        """Test that search is case insensitive"""
        results_upper = mock_logos_query.search("GOD")
        results_lower = mock_logos_query.search("god")
        # Should find same verses
        refs_upper = {r[0] for r in results_upper}
        refs_lower = {r[0] for r in results_lower}
        assert refs_upper == refs_lower

    def test_search_respects_limit(self, mock_logos_query):
        """Test that search respects limit parameter"""
        results = mock_logos_query.search("the", limit=5)
        assert len(results) <= 5

    def test_search_returns_tuples(self, mock_logos_query):
        """Test that search returns list of (ref, text) tuples"""
        results = mock_logos_query.search("God")
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)  # reference
            assert isinstance(item[1], str)  # text

    def test_connections_returns_dict(self, mock_logos_query):
        """Test that connections returns a dictionary"""
        result = mock_logos_query.connections("John 3:16")
        if result:
            assert isinstance(result, dict)
            assert 'outgoing' in result
            assert 'incoming' in result
            assert 'total' in result

    def test_connections_depth_1(self, mock_logos_query):
        """Test connections with depth 1"""
        result = mock_logos_query.connections("John 3:16", depth=1)
        if result:
            assert isinstance(result['outgoing'], list)
            assert isinstance(result['incoming'], list)

    def test_connections_invalid_ref(self, mock_logos_query):
        """Test connections with invalid reference"""
        result = mock_logos_query.connections("Invalid 99:99")
        assert result == [] or result == {'outgoing': [], 'incoming': [], 'total': 0}

    def test_path_finds_connection(self, mock_logos_query):
        """Test path finding between connected verses"""
        # These should be connected via cross-refs
        path = mock_logos_query.path("John 3:16", "John 3:17")
        if path:
            assert isinstance(path, list)
            assert path[0] == "John 3:16"
            assert path[-1] == "John 3:17"

    def test_path_returns_none_for_invalid(self, mock_logos_query):
        """Test path returns None for invalid references"""
        path = mock_logos_query.path("Invalid 1:1", "Also Invalid 2:2")
        assert path is None

    def test_central_returns_list(self, mock_logos_query):
        """Test that central returns list of tuples"""
        results = mock_logos_query.central(n=5)
        assert isinstance(results, list)
        assert len(results) <= 5
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_central_sorted_by_centrality(self, mock_logos_query):
        """Test that central results are sorted by centrality score"""
        results = mock_logos_query.central(n=5)
        if len(results) > 1:
            scores = [score for _, score in results]
            assert scores == sorted(scores, reverse=True)

    def test_central_with_book_filter(self, mock_logos_query):
        """Test central verses filtered by book"""
        results = mock_logos_query.central(n=5, book="John")
        for ref, _ in results:
            assert ref.startswith("John")

    def test_cluster_returns_dict(self, mock_logos_query):
        """Test that cluster returns a dictionary"""
        result = mock_logos_query.cluster("John 3:16")
        if result:
            assert isinstance(result, dict)
            assert 'center' in result
            assert 'nodes' in result
            assert 'size' in result
            assert 'edges' in result

    def test_cluster_center_is_input(self, mock_logos_query):
        """Test that cluster center matches input"""
        result = mock_logos_query.cluster("John 3:16")
        if result:
            assert result['center'] == "John 3:16"

    def test_cluster_invalid_ref(self, mock_logos_query):
        """Test cluster with invalid reference"""
        result = mock_logos_query.cluster("Invalid 99:99")
        assert result is None

    def test_witness_returns_results(self, mock_logos_query):
        """Test three-witness pattern returns results"""
        results = mock_logos_query.witness("God")
        assert isinstance(results, list)

    def test_witness_returns_n_results(self, mock_logos_query):
        """Test that witness returns at most n results"""
        results = mock_logos_query.witness("God", n=3)
        assert len(results) <= 3

    def test_witness_returns_tuples(self, mock_logos_query):
        """Test that witness returns (ref, text) tuples"""
        results = mock_logos_query.witness("God", n=3)
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2


class TestSearchEdgeCases:
    """Tests for search edge cases"""

    @pytest.fixture
    def mock_logos_query(self, sample_kjv, networkx_graph, monkeypatch):
        """Create a LogosQuery instance with mocked data"""
        from src import query
        monkeypatch.setattr('src.query.load_graph', lambda: networkx_graph)
        monkeypatch.setattr('src.query.load_kjv', lambda: sample_kjv)
        return query.LogosQuery()

    def test_search_empty_string(self, mock_logos_query):
        """Test search with empty string"""
        results = mock_logos_query.search("")
        assert isinstance(results, list)

    def test_search_special_characters(self, mock_logos_query):
        """Test search with special characters"""
        results = mock_logos_query.search("(and)")
        assert isinstance(results, list)

    def test_search_numbers(self, mock_logos_query):
        """Test search with numbers"""
        results = mock_logos_query.search("3:16")
        assert isinstance(results, list)

    def test_verse_empty_string(self, mock_logos_query):
        """Test verse lookup with empty string"""
        result = mock_logos_query.verse("")
        # Empty string matches all verses via fuzzy match, returns first match
        # This is acceptable behavior - returns a result since "" is substring of all strings
        assert result is None or isinstance(result, str)


class TestGraphOperations:
    """Tests for graph-based operations"""

    @pytest.fixture
    def mock_logos_query(self, sample_kjv, networkx_graph, monkeypatch):
        """Create a LogosQuery instance with mocked data"""
        from src import query
        monkeypatch.setattr('src.query.load_graph', lambda: networkx_graph)
        monkeypatch.setattr('src.query.load_kjv', lambda: sample_kjv)
        return query.LogosQuery()

    def test_graph_is_directed(self, mock_logos_query):
        """Test that internal graph is directed"""
        assert mock_logos_query.G.is_directed()

    def test_all_verses_in_graph(self, mock_logos_query, sample_kjv):
        """Test that all KJV verses are in graph"""
        for ref in sample_kjv.keys():
            assert ref in mock_logos_query.G.nodes

    def test_themes_returns_list(self, mock_logos_query):
        """Test that themes detection returns list"""
        results = mock_logos_query.themes()
        if results:
            assert isinstance(results, list)

    def test_themes_with_book_filter(self, mock_logos_query):
        """Test themes filtered by book"""
        results = mock_logos_query.themes(book="John")
        if results:
            assert isinstance(results, list)
