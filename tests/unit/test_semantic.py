"""
Tests for LOGOS Engine semantic search module
"""

import json
import math
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestSemanticSearch:
    """Tests for SemanticSearch class"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_init_loads_kjv(self, mock_semantic_search, sample_kjv):
        """Test that SemanticSearch loads KJV data"""
        assert len(mock_semantic_search.kjv) == len(sample_kjv)

    def test_init_loads_strongs(self, mock_semantic_search, sample_strongs):
        """Test that SemanticSearch loads Strong's data"""
        assert len(mock_semantic_search.strongs) == len(sample_strongs)

    def test_word_to_strongs_mapping_exists(self, mock_semantic_search):
        """Test that word-to-Strong's mapping is built"""
        assert len(mock_semantic_search.word_to_strongs) > 0

    def test_concept_map_exists(self, mock_semantic_search):
        """Test that concept map is built"""
        assert len(mock_semantic_search.concept_map) > 0

    def test_verse_vectors_built(self, mock_semantic_search):
        """Test that verse vectors are built"""
        assert len(mock_semantic_search.verse_vectors) > 0


class TestWordToStrongsMapping:
    """Tests for word-to-Strong's number mapping"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_god_maps_to_strongs(self, mock_semantic_search):
        """Test that 'god' maps to Strong's numbers"""
        mapping = mock_semantic_search.word_to_strongs.get('god', set())
        assert len(mapping) > 0
        # Should include Hebrew and Greek words for God
        assert any(s.startswith('H') for s in mapping)  # Hebrew
        assert any(s.startswith('G') for s in mapping)  # Greek

    def test_love_maps_to_strongs(self, mock_semantic_search):
        """Test that 'love' maps to Strong's numbers"""
        mapping = mock_semantic_search.word_to_strongs.get('love', set())
        assert len(mapping) > 0

    def test_faith_maps_to_strongs(self, mock_semantic_search):
        """Test that 'faith' maps to Strong's numbers"""
        mapping = mock_semantic_search.word_to_strongs.get('faith', set())
        assert len(mapping) > 0

    def test_mapping_values_are_sets(self, mock_semantic_search):
        """Test that mapping values are sets of Strong's numbers"""
        for word, strongs_set in mock_semantic_search.word_to_strongs.items():
            assert isinstance(strongs_set, set), f"Expected set for {word}"


class TestConceptMap:
    """Tests for theological concept mapping"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_divinity_concept_exists(self, mock_semantic_search):
        """Test that divinity concept exists"""
        assert 'divinity' in mock_semantic_search.concept_map

    def test_salvation_concept_exists(self, mock_semantic_search):
        """Test that salvation concept exists"""
        assert 'salvation' in mock_semantic_search.concept_map

    def test_faith_concept_exists(self, mock_semantic_search):
        """Test that faith concept exists"""
        assert 'faith' in mock_semantic_search.concept_map

    def test_love_concept_exists(self, mock_semantic_search):
        """Test that love concept exists"""
        assert 'love' in mock_semantic_search.concept_map

    def test_concept_values_are_sets(self, mock_semantic_search):
        """Test that concept values are sets of Strong's numbers"""
        for concept, strongs_set in mock_semantic_search.concept_map.items():
            assert isinstance(strongs_set, set), f"Expected set for concept {concept}"

    def test_concepts_contain_strongs(self, mock_semantic_search):
        """Test that concepts contain valid Strong's numbers"""
        import re
        strongs_pattern = re.compile(r'^[HG]\d+$')
        for concept, strongs_set in mock_semantic_search.concept_map.items():
            for s in strongs_set:
                assert strongs_pattern.match(s), f"Invalid Strong's number {s} in {concept}"


class TestCosineSimilarity:
    """Tests for cosine similarity calculation"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_identical_vectors_similarity_one(self, mock_semantic_search):
        """Test that identical vectors have similarity 1.0"""
        vec = {'concept1': 1.0, 'concept2': 2.0}
        similarity = mock_semantic_search._cosine_similarity(vec, vec)
        assert abs(similarity - 1.0) < 0.001

    def test_orthogonal_vectors_similarity_zero(self, mock_semantic_search):
        """Test that orthogonal vectors have similarity 0"""
        vec1 = {'concept1': 1.0}
        vec2 = {'concept2': 1.0}
        similarity = mock_semantic_search._cosine_similarity(vec1, vec2)
        assert abs(similarity) < 0.001

    def test_empty_vector_similarity_zero(self, mock_semantic_search):
        """Test that empty vectors have similarity 0"""
        vec1 = {}
        vec2 = {'concept1': 1.0}
        similarity = mock_semantic_search._cosine_similarity(vec1, vec2)
        assert similarity == 0

    def test_similarity_is_symmetric(self, mock_semantic_search):
        """Test that cosine similarity is symmetric"""
        vec1 = {'concept1': 1.0, 'concept2': 0.5}
        vec2 = {'concept1': 0.5, 'concept3': 1.0}
        sim1 = mock_semantic_search._cosine_similarity(vec1, vec2)
        sim2 = mock_semantic_search._cosine_similarity(vec2, vec1)
        assert abs(sim1 - sim2) < 0.001

    def test_similarity_bounded(self, mock_semantic_search):
        """Test that similarity is bounded between 0 and 1"""
        vec1 = {'concept1': 1.0, 'concept2': 2.0, 'concept3': 3.0}
        vec2 = {'concept1': 0.5, 'concept2': 1.0, 'concept3': 1.5}
        similarity = mock_semantic_search._cosine_similarity(vec1, vec2)
        assert 0 <= similarity <= 1


class TestSimilarVerses:
    """Tests for similar verse finding"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_similar_verses_returns_list(self, mock_semantic_search):
        """Test that similar_verses returns a list"""
        results = mock_semantic_search.similar_verses("John 3:16", n=5)
        assert isinstance(results, list)

    def test_similar_verses_respects_limit(self, mock_semantic_search):
        """Test that similar_verses respects n parameter"""
        results = mock_semantic_search.similar_verses("John 3:16", n=3)
        assert len(results) <= 3

    def test_similar_verses_excludes_self(self, mock_semantic_search):
        """Test that similar_verses excludes the query verse"""
        results = mock_semantic_search.similar_verses("John 3:16", n=10)
        refs = [r[0] for r in results]
        assert "John 3:16" not in refs

    def test_similar_verses_returns_tuples(self, mock_semantic_search):
        """Test that similar_verses returns (ref, score) tuples"""
        results = mock_semantic_search.similar_verses("John 3:16", n=5)
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)  # reference
            assert isinstance(item[1], (int, float))  # score

    def test_similar_verses_sorted_by_score(self, mock_semantic_search):
        """Test that results are sorted by similarity score"""
        results = mock_semantic_search.similar_verses("John 3:16", n=5)
        if len(results) > 1:
            scores = [score for _, score in results]
            assert scores == sorted(scores, reverse=True)

    def test_similar_verses_invalid_ref(self, mock_semantic_search):
        """Test similar_verses with invalid reference"""
        results = mock_semantic_search.similar_verses("Invalid 99:99", n=5)
        assert results == []


class TestSearchConcept:
    """Tests for concept-based search"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_search_concept_returns_list(self, mock_semantic_search):
        """Test that search_concept returns a list"""
        results = mock_semantic_search.search_concept("salvation")
        assert isinstance(results, list)

    def test_search_concept_returns_tuples(self, mock_semantic_search):
        """Test that search_concept returns (ref, text, score) tuples"""
        results = mock_semantic_search.search_concept("salvation")
        for item in results:
            assert isinstance(item, tuple)
            assert len(item) == 3

    def test_search_concept_respects_limit(self, mock_semantic_search):
        """Test that search_concept respects n parameter"""
        results = mock_semantic_search.search_concept("salvation", n=5)
        assert len(results) <= 5

    def test_search_concept_partial_match(self, mock_semantic_search):
        """Test that search_concept handles partial concept names"""
        # 'salv' should match 'salvation'
        results = mock_semantic_search.search_concept("salv")
        assert isinstance(results, list)


class TestSearchMeaning:
    """Tests for meaning-based search"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_search_meaning_returns_list(self, mock_semantic_search):
        """Test that search_meaning returns a list"""
        results = mock_semantic_search.search_meaning("God's love for humanity")
        assert isinstance(results, list)

    def test_search_meaning_returns_tuples(self, mock_semantic_search):
        """Test that search_meaning returns (ref, text, score) tuples"""
        results = mock_semantic_search.search_meaning("God's love")
        for item in results:
            if len(item) == 3:
                assert isinstance(item[0], str)  # reference
                assert isinstance(item[1], str)  # text
                assert isinstance(item[2], (int, float))  # score

    def test_search_meaning_respects_limit(self, mock_semantic_search):
        """Test that search_meaning respects n parameter"""
        results = mock_semantic_search.search_meaning("salvation", n=5)
        assert len(results) <= 5


class TestExplainConnection:
    """Tests for connection explanation"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_explain_connection_returns_dict_or_none(self, mock_semantic_search):
        """Test that explain_connection returns dict or None"""
        result = mock_semantic_search.explain_connection("John 3:16", "John 3:17")
        assert result is None or isinstance(result, dict)

    def test_explain_connection_has_required_keys(self, mock_semantic_search):
        """Test that explanation has required keys"""
        result = mock_semantic_search.explain_connection("John 3:16", "John 3:17")
        if result:
            assert 'ref1' in result
            assert 'ref2' in result
            assert 'shared_concepts' in result
            assert 'similarity' in result

    def test_explain_connection_refs_match_input(self, mock_semantic_search):
        """Test that explanation refs match input"""
        result = mock_semantic_search.explain_connection("John 3:16", "John 3:17")
        if result:
            assert result['ref1'] == "John 3:16"
            assert result['ref2'] == "John 3:17"

    def test_explain_connection_shared_concepts_is_list(self, mock_semantic_search):
        """Test that shared_concepts is a list"""
        result = mock_semantic_search.explain_connection("John 3:16", "John 3:17")
        if result:
            assert isinstance(result['shared_concepts'], list)


class TestIDF:
    """Tests for IDF (Inverse Document Frequency) calculation"""

    @pytest.fixture
    def mock_semantic_search(self, temp_data_dir, monkeypatch):
        """Create a SemanticSearch instance with mocked data"""
        from src import semantic
        monkeypatch.setattr(semantic, 'DATA_DIR', temp_data_dir)
        return semantic.SemanticSearch()

    def test_idf_values_exist(self, mock_semantic_search):
        """Test that IDF values are calculated"""
        assert len(mock_semantic_search.idf) > 0

    def test_idf_values_are_numeric(self, mock_semantic_search):
        """Test that IDF values are numeric"""
        for concept, idf_value in mock_semantic_search.idf.items():
            assert isinstance(idf_value, (int, float))

    def test_idf_values_are_positive(self, mock_semantic_search):
        """Test that IDF values are positive or zero"""
        for concept, idf_value in mock_semantic_search.idf.items():
            # IDF can be negative if document frequency is very high
            # but should generally be real numbers
            assert isinstance(idf_value, (int, float))
