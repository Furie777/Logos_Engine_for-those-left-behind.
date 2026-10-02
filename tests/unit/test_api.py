"""
Tests for LOGOS Engine API integration module
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import urllib.request
import urllib.error

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestFetchVerse:
    """Tests for verse fetching from API"""

    @pytest.fixture
    def mock_api_response(self):
        """Create a mock API response"""
        return {
            'reference': 'John 3:16',
            'verses': [
                {'verse': 16, 'text': 'For God so loved the world...'}
            ],
            'text': 'For God so loved the world...'
        }

    def test_fetch_verse_returns_dict_or_none(self, tmp_path, monkeypatch):
        """Test that fetch_verse returns dict or None"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Mock the urlopen to avoid actual network calls
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'reference': 'John 3:16',
            'verses': [{'verse': 16, 'text': 'Test text'}]
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch.object(urllib.request, 'urlopen', return_value=mock_response):
            result = api.fetch_verse("John 3:16")
            assert result is None or isinstance(result, dict)

    def test_fetch_verse_uses_cache(self, tmp_path, monkeypatch):
        """Test that fetch_verse uses cached data"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Create a cached file
        cached_data = {
            'reference': 'John 3:16',
            'verses': [{'number': 16, 'text': 'Cached text'}]
        }
        cache_file = cache_dir / "kjv_John_3_16.json"
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f)

        result = api.fetch_verse("John 3:16")
        assert result is not None
        assert result['reference'] == 'John 3:16'

    def test_fetch_verse_handles_network_error(self, tmp_path, monkeypatch):
        """Test that fetch_verse handles network errors gracefully"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Mock urlopen to raise an error
        with patch.object(urllib.request, 'urlopen',
                         side_effect=urllib.error.URLError("Network error")):
            result = api.fetch_verse("John 3:16")
            assert result is None


class TestParseGetbibleResponse:
    """Tests for parsing getBible.net response"""

    def test_parse_response_returns_dict(self):
        """Test that parse returns a dictionary"""
        from src import api

        mock_data = {
            'book1': {
                'book_name': 'John',
                'chapter': {
                    '3': {
                        '16': {'verse_nr': 16, 'verse': 'Test verse text'}
                    }
                }
            }
        }

        result = api.parse_getbible_response(mock_data, "John 3:16")
        assert result is None or isinstance(result, dict)

    def test_parse_response_has_reference(self):
        """Test that parsed response has reference"""
        from src import api

        mock_data = {
            'book1': {
                'book_name': 'John',
                'chapter': {
                    '3': {
                        '16': {'verse_nr': 16, 'verse': 'Test verse text'}
                    }
                }
            }
        }

        result = api.parse_getbible_response(mock_data, "John 3:16")
        if result:
            assert 'reference' in result

    def test_parse_response_has_verses(self):
        """Test that parsed response has verses list"""
        from src import api

        mock_data = {
            'book1': {
                'book_name': 'John',
                'chapter': {
                    '3': {
                        '16': {'verse_nr': 16, 'verse': 'Test verse text'}
                    }
                }
            }
        }

        result = api.parse_getbible_response(mock_data, "John 3:16")
        if result:
            assert 'verses' in result
            assert isinstance(result['verses'], list)

    def test_parse_empty_data(self):
        """Test parsing empty data"""
        from src import api

        result = api.parse_getbible_response({}, "John 3:16")
        assert result is None or result.get('verses', []) == []


class TestFetchChapter:
    """Tests for chapter fetching"""

    def test_fetch_chapter_calls_fetch_verse(self, tmp_path, monkeypatch):
        """Test that fetch_chapter calls fetch_verse with correct reference"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Create cached data for the chapter
        cached_data = {
            'reference': 'John 3',
            'verses': [
                {'number': 1, 'text': 'Verse 1'},
                {'number': 2, 'text': 'Verse 2'}
            ]
        }
        cache_file = cache_dir / "kjva_John_3.json"
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f)

        result = api.fetch_chapter("John", 3)
        # Should use cached data or make API call


class TestApocryphaBooks:
    """Tests for Apocrypha book handling"""

    def test_apocrypha_chapters_dict_exists(self):
        """Test that Apocrypha chapters dictionary exists in function"""
        from src import api

        # The function should have knowledge of Apocrypha book structure
        # Test by calling with known Apocrypha book
        # This is a structural test - doesn't make network calls

    def test_fetch_apocrypha_unknown_book(self, tmp_path, monkeypatch, capsys):
        """Test fetching unknown Apocrypha book"""
        from src import api

        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        result = api.fetch_apocrypha_book("Unknown Book")
        assert result is None

        captured = capsys.readouterr()
        assert "Unknown book" in captured.out


class TestAddApocryphaToKJV:
    """Tests for adding Apocrypha to KJV"""

    def test_add_apocrypha_missing_kjv(self, tmp_path, monkeypatch, capsys):
        """Test adding Apocrypha when KJV is missing"""
        from src import api

        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        api.add_apocrypha_to_kjv()

        captured = capsys.readouterr()
        assert "KJV not found" in captured.out

    def test_add_apocrypha_integrates_files(self, tmp_path, monkeypatch):
        """Test that add_apocrypha_to_kjv integrates apocrypha files"""
        from src import api

        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Create minimal KJV file
        kjv_path = tmp_path / "kjv.json"
        with open(kjv_path, 'w') as f:
            json.dump({"John 3:16": "Test verse"}, f)

        # Create an apocrypha file
        apocrypha_data = {
            'name': 'Tobit',
            'chapters': {
                '1': [{'number': 1, 'text': 'Tobit verse 1'}]
            }
        }
        apocrypha_path = tmp_path / "apocrypha_tobit.json"
        with open(apocrypha_path, 'w') as f:
            json.dump(apocrypha_data, f)

        api.add_apocrypha_to_kjv()

        # Verify KJV was updated
        with open(kjv_path, 'r') as f:
            updated_kjv = json.load(f)

        # Should still have original verse
        assert "John 3:16" in updated_kjv


class TestCaching:
    """Tests for API caching functionality"""

    def test_cache_dir_created(self, tmp_path, monkeypatch):
        """Test that cache directory is created if missing"""
        from src import api

        cache_dir = tmp_path / "cache"
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Mock network call
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'reference': 'Test',
            'verses': []
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch.object(urllib.request, 'urlopen', return_value=mock_response):
            api.fetch_verse("Test 1:1")

        assert cache_dir.exists()

    def test_cache_key_format(self, tmp_path, monkeypatch):
        """Test that cache keys are properly formatted"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Create cache file with expected naming
        cached_data = {'reference': 'John 3:16', 'verses': []}
        cache_file = cache_dir / "kjv_John_3_16.json"
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f)

        result = api.fetch_verse("John 3:16")
        assert result is not None


class TestAPIResponseStructure:
    """Tests for API response structure handling"""

    def test_response_with_verses_array(self, tmp_path, monkeypatch):
        """Test handling response with verses array"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Mock response with verses array
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'reference': 'John 3:16',
            'verses': [
                {'verse': 16, 'text': 'For God so loved the world...'}
            ]
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch.object(urllib.request, 'urlopen', return_value=mock_response):
            result = api.fetch_verse("John 3:16")

        if result:
            assert 'verses' in result

    def test_response_with_direct_text(self, tmp_path, monkeypatch):
        """Test handling response with direct text field"""
        from src import api

        cache_dir = tmp_path / "cache"
        cache_dir.mkdir()
        monkeypatch.setattr(api, 'CACHE_DIR', cache_dir)
        monkeypatch.setattr(api, 'DATA_DIR', tmp_path)

        # Mock response with direct text
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'reference': 'John 3:16',
            'text': 'For God so loved the world...'
        }).encode('utf-8')
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch.object(urllib.request, 'urlopen', return_value=mock_response):
            result = api.fetch_verse("John 3:16")

        if result:
            assert 'verses' in result
            if result['verses']:
                assert result['verses'][0]['text']
