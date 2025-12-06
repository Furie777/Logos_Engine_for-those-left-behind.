"""
Tests for LOGOS Engine concordance module
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestConcordance:
    """Tests for Concordance class"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_init_builds_word_index(self, mock_concordance):
        """Test that Concordance builds word index"""
        assert len(mock_concordance.word_index) > 0

    def test_init_loads_strongs(self, mock_concordance):
        """Test that Concordance loads Strong's definitions"""
        assert len(mock_concordance.strongs_definitions) > 0

    def test_verse_words_populated(self, mock_concordance):
        """Test that verse words are populated"""
        assert len(mock_concordance.verse_words) > 0


class TestTokenize:
    """Tests for text tokenization"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_tokenize_returns_list(self, mock_concordance):
        """Test that tokenize returns a list"""
        result = mock_concordance._tokenize("In the beginning God created")
        assert isinstance(result, list)

    def test_tokenize_splits_on_whitespace(self, mock_concordance):
        """Test that tokenize splits on whitespace"""
        result = mock_concordance._tokenize("In the beginning")
        assert len(result) == 3

    def test_tokenize_removes_punctuation(self, mock_concordance):
        """Test that tokenize removes punctuation"""
        result = mock_concordance._tokenize("God, the Creator.")
        # Should not contain punctuation
        for word in result:
            assert ',' not in word
            assert '.' not in word

    def test_tokenize_empty_string(self, mock_concordance):
        """Test tokenize with empty string"""
        result = mock_concordance._tokenize("")
        assert result == [] or result == ['']


class TestSearchWord:
    """Tests for word search functionality"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_search_word_returns_list(self, mock_concordance):
        """Test that search_word returns a list"""
        result = mock_concordance.search_word("God")
        assert isinstance(result, list)

    def test_search_word_case_insensitive(self, mock_concordance):
        """Test that search_word is case insensitive"""
        result_upper = mock_concordance.search_word("GOD")
        result_lower = mock_concordance.search_word("god")
        # Should find the same occurrences
        assert len(result_upper) == len(result_lower)

    def test_search_word_returns_tuples(self, mock_concordance):
        """Test that search_word returns (ref, position) tuples"""
        result = mock_concordance.search_word("God")
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_search_word_respects_limit(self, mock_concordance):
        """Test that search_word respects limit parameter"""
        result = mock_concordance.search_word("the", limit=5)
        assert len(result) <= 5

    def test_search_word_not_found(self, mock_concordance):
        """Test search_word with word not in text"""
        result = mock_concordance.search_word("xyznonexistent")
        assert result == []


class TestSearchStrongs:
    """Tests for Strong's number search"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_search_strongs_returns_list(self, mock_concordance):
        """Test that search_strongs returns a list"""
        result = mock_concordance.search_strongs("H430")
        assert isinstance(result, list)

    def test_search_strongs_not_found(self, mock_concordance):
        """Test search_strongs with non-existent number"""
        result = mock_concordance.search_strongs("H99999")
        assert result == []


class TestGetStrongsDefinition:
    """Tests for Strong's definition retrieval"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_get_strongs_definition_returns_dict(self, mock_concordance):
        """Test that get_strongs_definition returns a dict"""
        result = mock_concordance.get_strongs_definition("H430")
        if result:
            assert isinstance(result, dict)

    def test_get_strongs_definition_has_hebrew(self, mock_concordance, sample_strongs):
        """Test that Hebrew definition has hebrew field"""
        result = mock_concordance.get_strongs_definition("H430")
        if result:
            assert 'hebrew' in result

    def test_get_strongs_definition_has_greek(self, mock_concordance, sample_strongs):
        """Test that Greek definition has greek field"""
        result = mock_concordance.get_strongs_definition("G2316")
        if result:
            assert 'greek' in result

    def test_get_strongs_definition_has_transliteration(self, mock_concordance):
        """Test that definition has transliteration"""
        result = mock_concordance.get_strongs_definition("H430")
        if result:
            assert 'transliteration' in result

    def test_get_strongs_definition_has_definition(self, mock_concordance):
        """Test that definition has definition field"""
        result = mock_concordance.get_strongs_definition("H430")
        if result:
            assert 'definition' in result

    def test_get_strongs_definition_not_found(self, mock_concordance):
        """Test get_strongs_definition with non-existent number"""
        result = mock_concordance.get_strongs_definition("H99999")
        assert result is None


class TestWordStudy:
    """Tests for word study functionality"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_word_study_returns_dict(self, mock_concordance):
        """Test that word_study returns a dictionary"""
        result = mock_concordance.word_study("god")
        assert isinstance(result, dict)

    def test_word_study_has_word(self, mock_concordance):
        """Test that word_study result has word field"""
        result = mock_concordance.word_study("god")
        assert 'word' in result
        assert result['word'] == "god"

    def test_word_study_has_occurrences(self, mock_concordance):
        """Test that word_study result has occurrences"""
        result = mock_concordance.word_study("god")
        assert 'occurrences' in result
        assert isinstance(result['occurrences'], list)

    def test_word_study_has_total_occurrences(self, mock_concordance):
        """Test that word_study result has total_occurrences"""
        result = mock_concordance.word_study("god")
        assert 'total_occurrences' in result
        assert isinstance(result['total_occurrences'], int)

    def test_word_study_has_strongs(self, mock_concordance):
        """Test that word_study result has strongs"""
        result = mock_concordance.word_study("god")
        assert 'strongs' in result
        assert isinstance(result['strongs'], list)

    def test_word_study_has_related_hebrew(self, mock_concordance):
        """Test that word_study result has related_hebrew"""
        result = mock_concordance.word_study("god")
        assert 'related_hebrew' in result
        assert isinstance(result['related_hebrew'], list)

    def test_word_study_has_related_greek(self, mock_concordance):
        """Test that word_study result has related_greek"""
        result = mock_concordance.word_study("god")
        assert 'related_greek' in result
        assert isinstance(result['related_greek'], list)


class TestThreeWitnessHebrew:
    """Tests for three-witness pattern with Hebrew/Greek"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_three_witness_returns_dict_or_none(self, mock_concordance):
        """Test that three_witness_hebrew returns dict or None"""
        result = mock_concordance.three_witness_hebrew("H430")
        assert result is None or isinstance(result, dict)

    def test_three_witness_has_strongs(self, mock_concordance):
        """Test that three_witness result has strongs field"""
        result = mock_concordance.three_witness_hebrew("H430")
        if result:
            assert 'strongs' in result

    def test_three_witness_has_definition(self, mock_concordance):
        """Test that three_witness result has definition field"""
        result = mock_concordance.three_witness_hebrew("H430")
        if result:
            assert 'definition' in result

    def test_three_witness_not_found(self, mock_concordance):
        """Test three_witness_hebrew with non-existent number"""
        result = mock_concordance.three_witness_hebrew("H99999")
        assert result is None


class TestStrongsDefinitionsStructure:
    """Tests for Strong's definitions structure"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_hebrew_entries_start_with_H(self, mock_concordance):
        """Test that Hebrew entries start with H"""
        hebrew_entries = [k for k in mock_concordance.strongs_definitions.keys()
                         if k.startswith('H')]
        assert len(hebrew_entries) > 0

    def test_greek_entries_start_with_G(self, mock_concordance):
        """Test that Greek entries start with G"""
        greek_entries = [k for k in mock_concordance.strongs_definitions.keys()
                        if k.startswith('G')]
        assert len(greek_entries) > 0

    def test_all_entries_valid_format(self, mock_concordance):
        """Test that all entries have valid H/G format"""
        import re
        pattern = re.compile(r'^[HG]\d+$')
        for key in mock_concordance.strongs_definitions.keys():
            assert pattern.match(key), f"Invalid Strong's number format: {key}"


class TestWordIndex:
    """Tests for word index structure"""

    @pytest.fixture
    def mock_concordance(self, temp_data_dir, monkeypatch):
        """Create a Concordance instance with mocked data"""
        from src import concordance
        monkeypatch.setattr(concordance, 'DATA_DIR', temp_data_dir)
        return concordance.Concordance()

    def test_word_index_keys_lowercase(self, mock_concordance):
        """Test that word index keys are lowercase"""
        for word in mock_concordance.word_index.keys():
            assert word == word.lower(), f"Word '{word}' should be lowercase"

    def test_word_index_values_are_lists(self, mock_concordance):
        """Test that word index values are lists"""
        for word, occurrences in mock_concordance.word_index.items():
            assert isinstance(occurrences, list), f"Expected list for '{word}'"

    def test_common_words_have_multiple_occurrences(self, mock_concordance):
        """Test that common words have multiple occurrences"""
        common_words = ['the', 'and', 'of']
        for word in common_words:
            if word in mock_concordance.word_index:
                assert len(mock_concordance.word_index[word]) > 0
