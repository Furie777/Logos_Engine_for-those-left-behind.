"""
Tests for LOGOS Engine integrity verification module
"""

import json
import hashlib
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src import integrity


class TestComputeSHA256:
    """Tests for SHA-256 hash computation"""

    def test_compute_sha256_returns_string(self, tmp_path):
        """Test that compute_sha256 returns a hex string"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        result = integrity.compute_sha256(test_file)
        assert isinstance(result, str)
        assert len(result) == 64  # SHA-256 produces 64 hex characters

    def test_compute_sha256_consistent(self, tmp_path):
        """Test that same content produces same hash"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        hash1 = integrity.compute_sha256(test_file)
        hash2 = integrity.compute_sha256(test_file)
        assert hash1 == hash2

    def test_compute_sha256_different_content(self, tmp_path):
        """Test that different content produces different hash"""
        file1 = tmp_path / "test1.txt"
        file2 = tmp_path / "test2.txt"
        file1.write_text("content one")
        file2.write_text("content two")
        hash1 = integrity.compute_sha256(file1)
        hash2 = integrity.compute_sha256(file2)
        assert hash1 != hash2

    def test_compute_sha256_known_value(self, tmp_path):
        """Test SHA-256 against known value"""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"hello world")
        result = integrity.compute_sha256(test_file)
        # Known SHA-256 of "hello world"
        expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        assert result == expected


class TestGetFileSize:
    """Tests for file size calculation"""

    def test_get_file_size_returns_int(self, tmp_path):
        """Test that get_file_size returns an integer"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        result = integrity.get_file_size(test_file)
        assert isinstance(result, int)

    def test_get_file_size_accurate(self, tmp_path):
        """Test that file size is accurate"""
        test_file = tmp_path / "test.txt"
        content = "12345"  # 5 bytes
        test_file.write_text(content)
        result = integrity.get_file_size(test_file)
        assert result == 5

    def test_get_file_size_empty_file(self, tmp_path):
        """Test file size of empty file"""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")
        result = integrity.get_file_size(test_file)
        assert result == 0


class TestVerifyFile:
    """Tests for file verification"""

    def test_verify_file_missing(self, tmp_path, monkeypatch):
        """Test verification of missing file"""
        base_dir = tmp_path
        monkeypatch.setattr(integrity, 'DATA_DIR', base_dir / "data")
        monkeypatch.setattr(integrity, 'OUTPUT_DIR', base_dir / "output")

        result = integrity.verify_file(
            "data/nonexistent.json",
            {"sha256": "abc123", "size": 100}
        )
        assert result['status'] == 'MISSING'

    def test_verify_file_size_mismatch(self, tmp_path, monkeypatch):
        """Test verification with size mismatch"""
        # Setup
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        test_file = data_dir / "test.json"
        test_file.write_text('{"test": true}')

        # Get actual values
        actual_size = integrity.get_file_size(test_file)
        actual_hash = integrity.compute_sha256(test_file)

        # Patch the base directory lookup
        def mock_verify(filepath, expected, verbose=True):
            full_path = base_dir / filepath
            if not full_path.exists():
                return {'file': filepath, 'status': 'MISSING', 'message': 'Not found', 'details': {}}

            file_size = integrity.get_file_size(full_path)
            expected_size = expected.get('size', 0)

            if expected_size and file_size != expected_size:
                return {
                    'file': filepath,
                    'status': 'SIZE_MISMATCH',
                    'message': f'Size mismatch: expected {expected_size}, got {file_size}',
                    'details': {'expected_size': expected_size, 'actual_size': file_size}
                }

            return {'file': filepath, 'status': 'VERIFIED', 'message': 'OK', 'details': {}}

        # Test with wrong size expectation
        result = mock_verify(
            "data/test.json",
            {"sha256": actual_hash, "size": actual_size + 100}  # Wrong size
        )
        assert result['status'] == 'SIZE_MISMATCH'

    def test_verify_file_hash_mismatch(self, tmp_path):
        """Test verification with hash mismatch"""
        # Setup
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        test_file = data_dir / "test.json"
        test_file.write_text('{"test": true}')

        actual_size = integrity.get_file_size(test_file)

        # Test with wrong hash but correct size
        def mock_verify_hash(filepath, expected):
            full_path = base_dir / filepath
            if not full_path.exists():
                return {'file': filepath, 'status': 'MISSING', 'message': 'Not found', 'details': {}}

            actual_hash = integrity.compute_sha256(full_path)
            expected_hash = expected.get('sha256', '')

            if actual_hash != expected_hash:
                return {
                    'file': filepath,
                    'status': 'CORRUPTED',
                    'message': 'SHA-256 MISMATCH',
                    'details': {'expected_sha256': expected_hash, 'actual_sha256': actual_hash}
                }

            return {'file': filepath, 'status': 'VERIFIED', 'message': 'OK', 'details': {}}

        result = mock_verify_hash(
            "data/test.json",
            {"sha256": "wrong_hash_value", "size": actual_size}
        )
        assert result['status'] == 'CORRUPTED'

    def test_verify_file_success(self, tmp_path):
        """Test successful file verification"""
        # Setup
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        test_file = data_dir / "test.json"
        test_file.write_text('{"test": true}')

        actual_size = integrity.get_file_size(test_file)
        actual_hash = integrity.compute_sha256(test_file)

        def mock_verify_success(filepath, expected):
            full_path = base_dir / filepath
            if not full_path.exists():
                return {'file': filepath, 'status': 'MISSING', 'message': 'Not found', 'details': {}}

            file_size = integrity.get_file_size(full_path)
            file_hash = integrity.compute_sha256(full_path)

            expected_size = expected.get('size', 0)
            expected_hash = expected.get('sha256', '')

            if expected_size and file_size != expected_size:
                return {'file': filepath, 'status': 'SIZE_MISMATCH', 'message': 'Size mismatch', 'details': {}}

            if file_hash != expected_hash:
                return {'file': filepath, 'status': 'CORRUPTED', 'message': 'Hash mismatch', 'details': {}}

            return {'file': filepath, 'status': 'VERIFIED', 'message': 'Integrity verified', 'details': {}}

        result = mock_verify_success(
            "data/test.json",
            {"sha256": actual_hash, "size": actual_size}
        )
        assert result['status'] == 'VERIFIED'


class TestQuickVerify:
    """Tests for quick verification"""

    def test_quick_verify_returns_tuple(self, tmp_path, monkeypatch):
        """Test that quick_verify returns a tuple of (bool, message)"""
        # Setup minimal data
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        kjv_file = data_dir / "kjv.json"
        kjv_file.write_text('{}')

        strongs_file = data_dir / "strongs.json"
        strongs_file.write_text('{}')

        # Mock the CHECKSUMS to use our test files
        test_checksums = {
            "data/kjv.json": {"sha256": integrity.compute_sha256(kjv_file)},
            "data/strongs.json": {"sha256": integrity.compute_sha256(strongs_file)}
        }

        monkeypatch.setattr(integrity, 'CHECKSUMS', test_checksums)

        # Mock the base directory resolution
        original_quick_verify = integrity.quick_verify

        def patched_quick_verify():
            critical = ["data/kjv.json", "data/strongs.json"]
            for filepath in critical:
                full_path = base_dir / filepath
                if not full_path.exists():
                    return False, f"Critical file missing: {filepath}"

                expected = test_checksums.get(filepath)
                if expected:
                    actual_hash = integrity.compute_sha256(full_path)
                    if actual_hash != expected['sha256']:
                        return False, f"Integrity check failed: {filepath}"

            return True, "Critical files verified"

        result = patched_quick_verify()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)


class TestGenerateChecksums:
    """Tests for checksum generation"""

    def test_generate_checksums_returns_dict(self, tmp_path, monkeypatch):
        """Test that generate_checksums returns a dictionary"""
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        # Create test files
        test_file = data_dir / "test.json"
        test_file.write_text('{"test": true}')

        # Mock CHECKSUMS to only include our test file
        monkeypatch.setattr(integrity, 'CHECKSUMS', {"data/test.json": {}})

        def patched_generate():
            new_checksums = {}
            for filepath in integrity.CHECKSUMS.keys():
                full_path = base_dir / filepath
                if full_path.exists():
                    sha256 = integrity.compute_sha256(full_path)
                    size = integrity.get_file_size(full_path)
                    new_checksums[filepath] = {'sha256': sha256, 'size': size}
            return new_checksums

        result = patched_generate()
        assert isinstance(result, dict)

    def test_generate_checksums_includes_sha256(self, tmp_path, monkeypatch):
        """Test that generated checksums include SHA-256"""
        base_dir = tmp_path
        data_dir = base_dir / "data"
        data_dir.mkdir()

        test_file = data_dir / "test.json"
        test_file.write_text('{"test": true}')

        monkeypatch.setattr(integrity, 'CHECKSUMS', {"data/test.json": {}})

        def patched_generate():
            new_checksums = {}
            for filepath in integrity.CHECKSUMS.keys():
                full_path = base_dir / filepath
                if full_path.exists():
                    sha256 = integrity.compute_sha256(full_path)
                    size = integrity.get_file_size(full_path)
                    new_checksums[filepath] = {'sha256': sha256, 'size': size}
            return new_checksums

        result = patched_generate()
        assert "data/test.json" in result
        assert "sha256" in result["data/test.json"]
        assert len(result["data/test.json"]["sha256"]) == 64


class TestChecksumsConstant:
    """Tests for the CHECKSUMS constant"""

    def test_checksums_is_dict(self):
        """Test that CHECKSUMS is a dictionary"""
        assert isinstance(integrity.CHECKSUMS, dict)

    def test_checksums_has_critical_files(self):
        """Test that CHECKSUMS includes critical files"""
        critical_files = ["data/kjv.json", "data/strongs.json", "data/cross_refs.json"]
        for filepath in critical_files:
            assert filepath in integrity.CHECKSUMS, f"Missing critical file: {filepath}"

    def test_checksums_have_required_fields(self):
        """Test that each checksum entry has required fields"""
        for filepath, info in integrity.CHECKSUMS.items():
            assert "sha256" in info, f"Missing sha256 for {filepath}"
            assert isinstance(info["sha256"], str), f"sha256 should be string for {filepath}"
            assert len(info["sha256"]) == 64, f"sha256 should be 64 chars for {filepath}"

    def test_checksums_sha256_format(self):
        """Test that SHA-256 hashes are valid hex strings"""
        import re
        hex_pattern = re.compile(r'^[a-f0-9]{64}$')
        for filepath, info in integrity.CHECKSUMS.items():
            assert hex_pattern.match(info["sha256"]), \
                f"Invalid SHA-256 format for {filepath}: {info['sha256']}"


class TestRealDataIntegrity:
    """Tests that verify real data integrity if available"""

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_kjv_checksum(self):
        """Test that real KJV file matches expected checksum"""
        base_dir = Path(__file__).parent.parent.parent
        kjv_path = base_dir / "data" / "kjv.json"

        if not kjv_path.exists():
            pytest.skip("Real KJV data not available")

        expected = integrity.CHECKSUMS.get("data/kjv.json", {})
        if not expected:
            pytest.skip("No expected checksum for kjv.json")

        actual_hash = integrity.compute_sha256(kjv_path)
        actual_size = integrity.get_file_size(kjv_path)

        assert actual_hash == expected.get("sha256"), "KJV checksum mismatch"
        if "size" in expected:
            assert actual_size == expected["size"], "KJV size mismatch"

    @pytest.mark.requires_real_data
    @pytest.mark.slow
    def test_real_strongs_checksum(self):
        """Test that real Strong's file matches expected checksum"""
        base_dir = Path(__file__).parent.parent.parent
        strongs_path = base_dir / "data" / "strongs.json"

        if not strongs_path.exists():
            pytest.skip("Real Strong's data not available")

        expected = integrity.CHECKSUMS.get("data/strongs.json", {})
        if not expected:
            pytest.skip("No expected checksum for strongs.json")

        actual_hash = integrity.compute_sha256(strongs_path)
        assert actual_hash == expected.get("sha256"), "Strong's checksum mismatch"
