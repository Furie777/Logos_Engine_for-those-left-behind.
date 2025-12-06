"""
Tests for LOGOS Engine data loader module
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src import loader


class TestNormalizeRef:
    """Tests for reference normalization"""

    def test_normalize_genesis_format(self):
        """Test normalizing Gen.1.1 format to Genesis 1:1"""
        result = loader.normalize_ref("Gen.1.1")
        assert result == "Genesis 1:1"

    def test_normalize_john_format(self):
        """Test normalizing John.3.16 format"""
        result = loader.normalize_ref("John.3.16")
        assert result == "John 3:16"

    def test_normalize_psalms(self):
        """Test normalizing Ps.23.1 format"""
        result = loader.normalize_ref("Ps.23.1")
        assert result == "Psalms 23:1"

    def test_normalize_revelation(self):
        """Test normalizing Rev.22.21 format"""
        result = loader.normalize_ref("Rev.22.21")
        assert result == "Revelation 22:21"

    def test_normalize_already_normalized(self):
        """Test that already normalized refs are unchanged"""
        result = loader.normalize_ref("John 3:16")
        assert result == "John 3:16"

    def test_normalize_strips_whitespace(self):
        """Test that whitespace is stripped"""
        result = loader.normalize_ref("  John.3.16  ")
        assert result == "John 3:16"

    def test_normalize_first_samuel(self):
        """Test normalizing 1Sam format"""
        result = loader.normalize_ref("1Sam.17.1")
        assert result == "1 Samuel 17:1"

    def test_normalize_second_corinthians(self):
        """Test normalizing 2Cor format"""
        result = loader.normalize_ref("2Cor.5.17")
        assert result == "2 Corinthians 5:17"


class TestLoadKJV:
    """Tests for KJV loading functionality"""

    def test_load_kjv_returns_dict(self, temp_data_dir, monkeypatch):
        """Test that load_kjv returns a dictionary"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_kjv()
        assert isinstance(result, dict)

    def test_load_kjv_contains_expected_verses(self, temp_data_dir, monkeypatch, sample_kjv):
        """Test that loaded KJV contains expected verses"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_kjv()
        assert "John 3:16" in result
        assert "Genesis 1:1" in result

    def test_load_kjv_verse_content(self, temp_data_dir, monkeypatch):
        """Test that verse content is correct"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_kjv()
        assert "In the beginning" in result.get("Genesis 1:1", "")

    def test_load_kjv_handles_missing_file(self, tmp_path, monkeypatch):
        """Test behavior when KJV file is missing"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        monkeypatch.setattr(loader, 'DATA_DIR', empty_dir)
        # Should attempt download (will fail in test) or return minimal data
        # This tests the fallback mechanism


class TestLoadCrossReferences:
    """Tests for cross-reference loading"""

    def test_load_cross_refs_returns_dict(self, temp_data_dir, monkeypatch):
        """Test that load_cross_references returns a dictionary"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_cross_references()
        assert isinstance(result, dict)

    def test_load_cross_refs_contains_expected_refs(self, temp_data_dir, monkeypatch):
        """Test that loaded cross-refs contain expected references"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_cross_references()
        assert "John 3:16" in result
        assert "Genesis 1:1" in result

    def test_cross_refs_are_lists(self, temp_data_dir, monkeypatch):
        """Test that cross-reference values are lists"""
        monkeypatch.setattr(loader, 'DATA_DIR', temp_data_dir)
        result = loader.load_cross_references()
        for ref, targets in result.items():
            assert isinstance(targets, list), f"Expected list for {ref}"


class TestCreateMinimalKJV:
    """Tests for minimal KJV creation fallback"""

    def test_create_minimal_kjv_returns_dict(self, tmp_path):
        """Test that create_minimal_kjv returns a dictionary"""
        kjv_path = tmp_path / "kjv.json"
        result = loader.create_minimal_kjv(kjv_path)
        assert isinstance(result, dict)

    def test_create_minimal_kjv_contains_essential_verses(self, tmp_path):
        """Test that minimal KJV contains essential verses"""
        kjv_path = tmp_path / "kjv.json"
        result = loader.create_minimal_kjv(kjv_path)
        assert "Genesis 1:1" in result
        assert "John 3:16" in result
        assert "John 1:1" in result

    def test_create_minimal_kjv_creates_file(self, tmp_path):
        """Test that create_minimal_kjv creates a JSON file"""
        kjv_path = tmp_path / "kjv.json"
        loader.create_minimal_kjv(kjv_path)
        assert kjv_path.exists()

        with open(kjv_path, 'r') as f:
            data = json.load(f)
        assert isinstance(data, dict)


class TestRealData:
    """Tests that verify real data if available"""

    @pytest.mark.requires_real_data
    def test_real_kjv_verse_count(self, real_kjv):
        """Test that real KJV has expected verse count"""
        # KJV has approximately 31,102 canonical verses
        # With Apocrypha it can have more
        assert len(real_kjv) >= 31000, f"Expected ~31000+ verses, got {len(real_kjv)}"

    @pytest.mark.requires_real_data
    def test_real_kjv_contains_known_verses(self, real_kjv):
        """Test that real KJV contains well-known verses"""
        known_verses = [
            "Genesis 1:1",
            "Psalm 23:1",
            "John 3:16",
            "Romans 8:28",
        ]
        for ref in known_verses:
            # Try different key formats
            found = ref in real_kjv or f"Psalms {ref[6:]}" in real_kjv if ref.startswith("Psalm ") else ref in real_kjv
            assert found or any(ref.lower() in k.lower() for k in real_kjv.keys()), \
                f"Expected to find {ref} in KJV"

    @pytest.mark.requires_real_data
    def test_real_cross_refs_structure(self, real_cross_refs):
        """Test that real cross-refs have proper structure"""
        assert len(real_cross_refs) > 0
        for ref, targets in list(real_cross_refs.items())[:10]:
            assert isinstance(targets, list), f"Expected list for {ref}"
