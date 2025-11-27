#!/usr/bin/env python3
"""
LOGOS ENGINE - Integrity Verification System (Autoimmune)

"Prove all things; hold fast that which is good." - 1 Thessalonians 5:21

This module provides:
1. SHA-256 checksum verification for all Scripture data
2. Corruption detection
3. Tampering alerts
4. Self-healing from known-good sources (when possible)

The Word must be preserved uncorrupted.
"""

import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# =============================================================================
# KNOWN-GOOD CHECKSUMS
# Generated: November 27, 2025
# These are the authoritative checksums for verified Scripture data
# Multiple witnesses can verify these hashes independently
# =============================================================================

CHECKSUMS = {
    # CORE SCRIPTURE - KJV Bible
    "data/kjv.json": {
        "sha256": "384c9155024d2b3a865c3d4a28db4fec68283e9195abe13e0d468095d346e8e0",
        "size": 5977488,
        "verse_count": 36586,
        "description": "King James Bible - 66 books + Apocrypha"
    },

    # STRONG'S CONCORDANCE - Hebrew/Greek definitions
    "data/strongs.json": {
        "sha256": "d381c2e64a67917388b1c786b8d034f21839f8e17f4dac0763bb89610f4f85a9",
        "size": 2155883,
        "hebrew_count": 8674,
        "greek_count": 5523,
        "description": "Strong's Concordance - Hebrew & Greek definitions"
    },

    # CROSS-REFERENCES - Scripture interconnections
    "data/cross_refs.json": {
        "sha256": "7b0e6f5771418eb81f9345db5e44b5ab42f3b332c1d94917b3ca4913b753cf9f",
        "size": 53965992,
        "description": "Cross-reference connections (2.5M+ links)"
    },

    # APOCRYPHA (1611 KJV)
    "data/apocrypha_1_esdras.json": {
        "sha256": "dd73204504a7dddfebf830f243545057552d01568200be4ec86ba556469c43b6",
        "size": 88969
    },
    "data/apocrypha_1_maccabees.json": {
        "sha256": "376ba2a1dfa146c182d5bab772294c9452deb005c094e971a5e23dc942660393",
        "size": 178711
    },
    "data/apocrypha_2_esdras.json": {
        "sha256": "d2c112d79c9701e4d0bd4a3d300db23e6c87fb89fc09c392eaec91877118f0f5",
        "size": 156704
    },
    "data/apocrypha_2_maccabees.json": {
        "sha256": "7f8de1726ef6d68ec00245dd90b970d979e2de3a1e3958cb1253719b97eb8fd3",
        "size": 121594
    },
    "data/apocrypha_baruch.json": {
        "sha256": "7f02f30cde4df06f575b3f61bfd318e48252f91981363ffd7ccaf2dada50876f",
        "size": 25747
    },
    "data/apocrypha_bel_and_the_dragon.json": {
        "sha256": "aa9ef8d3afea93fe068c9470272791a6f1c7ebdbdb6f6629b1daff36d60f3c4f",
        "size": 8058
    },
    "data/apocrypha_judith.json": {
        "sha256": "35501832d5a8baac1dec1a16491c764cb646cbccd78a917158407b0f1d5853ca",
        "size": 77954
    },
    "data/apocrypha_prayer_of_azariah.json": {
        "sha256": "ae5fc4b41119d91c2564517d52f969fb8d73f79d6b9a572435b03894c35fcd5e",
        "size": 3124
    },
    "data/apocrypha_prayer_of_manasseh.json": {
        "sha256": "d7949f7c04d0c4b829516d1cb6edec26992d512c017fccda568a3a2ac99e5cf4",
        "size": 3125
    },
    "data/apocrypha_sirach.json": {
        "sha256": "00a5f9d640578ee6fc8d5eca1eb0b56ac09b0d5a9d457440b94e2b5da5ca7860",
        "size": 228137
    },
    "data/apocrypha_structure.json": {
        "sha256": "1abef268bfea741345da586af19ddebe0362a63361e94ae02159b2bf4d25b5ca",
        "size": 1778
    },
    "data/apocrypha_susanna.json": {
        "sha256": "5683beff523200dcb6775bc916c935e90a61c9c058f8666eb28d584a0f70e449",
        "size": 11298
    },
    "data/apocrypha_tobit.json": {
        "sha256": "a7662647066861a7a864a6792b1a906381e2ef42336918e0ed00f4a3e19747ee",
        "size": 49647
    },
    "data/apocrypha_wisdom_of_solomon.json": {
        "sha256": "ebfd8ec27c766b8f86f3d34fda4a70c76a4e25d2e10f5552202dd4fd34b06d31",
        "size": 82875
    },
}

# Files that may change (rebuilt from source data)
REGENERABLE_FILES = {
    "data/strongs_complete.json": {
        "source": "Rebuilt from HebrewStrong.xml + strongsgreek.xml",
        "command": "python parse_strongs_xml.py"
    },
    "output/logos_graph.gpickle": {
        "source": "Rebuilt from kjv.json + cross_refs.json",
        "command": "python logos.py build"
    }
}


def compute_sha256(filepath):
    """Compute SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_size(filepath):
    """Get file size in bytes"""
    return Path(filepath).stat().st_size


def verify_file(filepath, expected, verbose=True):
    """
    Verify a single file against expected checksum

    Returns:
        dict with 'status', 'message', 'details'
    """
    base_dir = Path(__file__).parent.parent
    full_path = base_dir / filepath

    result = {
        'file': filepath,
        'status': 'UNKNOWN',
        'message': '',
        'details': {}
    }

    # Check existence
    if not full_path.exists():
        result['status'] = 'MISSING'
        result['message'] = f"File not found: {filepath}"
        return result

    # Check size
    actual_size = get_file_size(full_path)
    expected_size = expected.get('size', 0)

    if expected_size and actual_size != expected_size:
        result['status'] = 'SIZE_MISMATCH'
        result['message'] = f"Size mismatch: expected {expected_size:,}, got {actual_size:,}"
        result['details']['expected_size'] = expected_size
        result['details']['actual_size'] = actual_size
        return result

    # Check SHA-256
    actual_hash = compute_sha256(full_path)
    expected_hash = expected.get('sha256', '')

    if actual_hash != expected_hash:
        result['status'] = 'CORRUPTED'
        result['message'] = "SHA-256 MISMATCH - File may be corrupted or tampered"
        result['details']['expected_sha256'] = expected_hash
        result['details']['actual_sha256'] = actual_hash
        return result

    # Additional content verification for KJV
    if filepath == "data/kjv.json":
        try:
            with open(full_path, 'r') as f:
                kjv = json.load(f)
            actual_verses = len(kjv)
            expected_verses = expected.get('verse_count', 0)
            if expected_verses and actual_verses != expected_verses:
                result['status'] = 'CONTENT_MISMATCH'
                result['message'] = f"Verse count mismatch: expected {expected_verses}, got {actual_verses}"
                result['details']['expected_verses'] = expected_verses
                result['details']['actual_verses'] = actual_verses
                return result
        except json.JSONDecodeError:
            result['status'] = 'PARSE_ERROR'
            result['message'] = "JSON parse error - file may be corrupted"
            return result

    # Additional verification for Strong's
    if filepath == "data/strongs.json":
        try:
            with open(full_path, 'r') as f:
                strongs = json.load(f)
            hebrew = sum(1 for k in strongs if k.startswith('H'))
            greek = sum(1 for k in strongs if k.startswith('G'))

            expected_hebrew = expected.get('hebrew_count', 0)
            expected_greek = expected.get('greek_count', 0)

            if expected_hebrew and hebrew != expected_hebrew:
                result['status'] = 'CONTENT_MISMATCH'
                result['message'] = f"Hebrew count mismatch: expected {expected_hebrew}, got {hebrew}"
                return result

            if expected_greek and greek != expected_greek:
                result['status'] = 'CONTENT_MISMATCH'
                result['message'] = f"Greek count mismatch: expected {expected_greek}, got {greek}"
                return result
        except json.JSONDecodeError:
            result['status'] = 'PARSE_ERROR'
            result['message'] = "JSON parse error - file may be corrupted"
            return result

    # All checks passed
    result['status'] = 'VERIFIED'
    result['message'] = "Integrity verified"
    result['details']['sha256'] = actual_hash
    result['details']['size'] = actual_size

    return result


def verify_all(verbose=True):
    """
    Verify all Scripture data files

    Returns:
        dict with overall status and per-file results
    """
    print("\n" + "=" * 60)
    print("LOGOS ENGINE - INTEGRITY VERIFICATION")
    print('"Prove all things; hold fast that which is good."')
    print("                           - 1 Thessalonians 5:21")
    print("=" * 60 + "\n")

    results = {
        'timestamp': datetime.now().isoformat(),
        'overall': 'PASS',
        'verified': 0,
        'failed': 0,
        'missing': 0,
        'files': {}
    }

    # Verify critical files
    critical_files = ["data/kjv.json", "data/strongs.json", "data/cross_refs.json"]

    for filepath, expected in CHECKSUMS.items():
        result = verify_file(filepath, expected, verbose)
        results['files'][filepath] = result

        # Print status
        status = result['status']
        if status == 'VERIFIED':
            results['verified'] += 1
            if verbose:
                print(f"  [PASS] {filepath}")
        elif status == 'MISSING':
            results['missing'] += 1
            results['overall'] = 'FAIL'
            print(f"  [MISSING] {filepath}")
            print(f"            {result['message']}")
        else:
            results['failed'] += 1
            results['overall'] = 'FAIL'
            print(f"  [FAIL] {filepath}")
            print(f"         Status: {status}")
            print(f"         {result['message']}")
            if filepath in critical_files:
                print(f"         *** CRITICAL FILE - Scripture integrity compromised ***")

    # Summary
    print("\n" + "-" * 60)
    print("VERIFICATION SUMMARY")
    print("-" * 60)
    print(f"  Verified:  {results['verified']}")
    print(f"  Failed:    {results['failed']}")
    print(f"  Missing:   {results['missing']}")
    print(f"  Total:     {len(CHECKSUMS)}")
    print()

    if results['overall'] == 'PASS':
        print("  STATUS: ALL FILES VERIFIED")
        print("  The Word is preserved.")
    else:
        print("  STATUS: VERIFICATION FAILED")
        print("  Some files may be corrupted or tampered.")
        print()
        print("  RECOMMENDED ACTIONS:")
        print("  1. Compare checksums with another trusted copy")
        print("  2. Re-download from authoritative source")
        print("  3. See docs/RECOVERY.md for restoration procedures")

    print("=" * 60 + "\n")

    return results


def quick_verify():
    """
    Quick integrity check of critical files only
    Used at startup to detect obvious corruption
    """
    critical = ["data/kjv.json", "data/strongs.json"]
    base_dir = Path(__file__).parent.parent

    for filepath in critical:
        full_path = base_dir / filepath
        if not full_path.exists():
            return False, f"Critical file missing: {filepath}"

        expected = CHECKSUMS.get(filepath)
        if expected:
            actual_hash = compute_sha256(full_path)
            if actual_hash != expected['sha256']:
                return False, f"Integrity check failed: {filepath}"

    return True, "Critical files verified"


def generate_checksums():
    """
    Generate fresh checksums for all data files
    Use this when creating new authoritative checksums
    """
    print("Generating fresh checksums...")
    base_dir = Path(__file__).parent.parent

    new_checksums = {}

    for filepath in CHECKSUMS.keys():
        full_path = base_dir / filepath
        if full_path.exists():
            sha256 = compute_sha256(full_path)
            size = get_file_size(full_path)
            new_checksums[filepath] = {
                'sha256': sha256,
                'size': size
            }
            print(f"  {filepath}: {sha256[:16]}...")

    return new_checksums


def diagnose(filepath):
    """
    Detailed diagnosis of a specific file
    """
    base_dir = Path(__file__).parent.parent
    full_path = base_dir / filepath

    print(f"\n=== DIAGNOSIS: {filepath} ===\n")

    if not full_path.exists():
        print("Status: FILE NOT FOUND")
        print(f"Expected location: {full_path}")
        return

    # File exists - gather info
    actual_size = get_file_size(full_path)
    actual_hash = compute_sha256(full_path)

    print(f"Location: {full_path}")
    print(f"Size: {actual_size:,} bytes")
    print(f"SHA-256: {actual_hash}")
    print()

    # Compare with expected
    expected = CHECKSUMS.get(filepath, {})

    if expected:
        print("Expected values:")
        print(f"  Size: {expected.get('size', 'N/A'):,}")
        print(f"  SHA-256: {expected.get('sha256', 'N/A')}")
        print()

        if actual_hash == expected.get('sha256'):
            print("RESULT: File matches expected checksum")
        else:
            print("RESULT: CHECKSUM MISMATCH")
            print()
            print("Possible causes:")
            print("  1. File was modified or updated")
            print("  2. File corruption during storage/transfer")
            print("  3. Malicious tampering")
            print()
            print("Recommended action:")
            print("  - Verify with another trusted copy")
            print("  - Re-download from authoritative source")
    else:
        print("Note: No expected checksum on record for this file")
        print("This file may be regenerable from source data")

        if filepath in REGENERABLE_FILES:
            info = REGENERABLE_FILES[filepath]
            print(f"\nThis file can be regenerated:")
            print(f"  Source: {info['source']}")
            print(f"  Command: {info['command']}")


def repl():
    """Interactive integrity verification REPL"""
    print("\n=== LOGOS INTEGRITY VERIFIER ===")
    print("Commands: verify, check <file>, diagnose <file>, checksums, quit")
    print()

    while True:
        try:
            cmd = input("INTEGRITY> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShalom.")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command in ('quit', 'exit'):
            print("Shalom.")
            break

        elif command == 'verify':
            verify_all()

        elif command == 'check':
            if arg in CHECKSUMS:
                result = verify_file(arg, CHECKSUMS[arg])
                print(f"\n{arg}: {result['status']}")
                print(f"  {result['message']}")
            else:
                print(f"Unknown file: {arg}")
                print("Known files:")
                for f in sorted(CHECKSUMS.keys()):
                    print(f"  {f}")

        elif command == 'diagnose':
            if arg:
                diagnose(arg)
            else:
                print("Usage: diagnose <filepath>")

        elif command == 'checksums':
            print("\nKnown checksums:")
            for filepath, info in sorted(CHECKSUMS.items()):
                print(f"\n{filepath}:")
                print(f"  SHA-256: {info['sha256']}")
                print(f"  Size: {info['size']:,} bytes")

        elif command == 'help':
            print("\nCommands:")
            print("  verify           - Verify all files")
            print("  check <file>     - Check specific file")
            print("  diagnose <file>  - Detailed diagnosis")
            print("  checksums        - List all checksums")
            print("  quit             - Exit")

        else:
            print(f"Unknown: {command}. Type 'help'")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'verify':
            verify_all()
        elif sys.argv[1] == 'generate':
            generate_checksums()
        elif sys.argv[1] == 'diagnose' and len(sys.argv) > 2:
            diagnose(sys.argv[2])
        else:
            print("Usage: python integrity.py [verify|generate|diagnose <file>]")
    else:
        repl()
