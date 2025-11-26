"""
LOGOS ENGINE - Data Loader
Acquires KJV text and cross-references from public domain sources
"""

import json
import os
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# Public domain KJV sources
KJV_URL = "https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/kjv.json"
# Alternative KJV source
KJV_URL_ALT = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"
# OpenBible cross-references
CROSS_REF_URL = "https://www.openbible.info/labs/cross-references/cross_references.txt"


def download_kjv():
    """Download KJV Bible as JSON"""
    kjv_path = DATA_DIR / "kjv.json"

    if kjv_path.exists():
        print(f"KJV already exists at {kjv_path}")
        return load_kjv()

    print("Downloading KJV from GitHub...")

    # Try primary source first
    for url in [KJV_URL, KJV_URL_ALT]:
        try:
            print(f"Trying: {url[:50]}...")
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
                # Handle BOM
                if raw.startswith(b'\xef\xbb\xbf'):
                    raw = raw[3:]
                data = json.loads(raw.decode('utf-8'))

            # Restructure for our use
            kjv = {}
            verse_count = 0

            # Handle different JSON structures
            if isinstance(data, list):
                # Array of books format
                for book in data:
                    book_name = book.get('name', book.get('abbrev', 'Unknown'))
                    chapters = book.get('chapters', [])

                    for ch_idx, chapter in enumerate(chapters, 1):
                        for v_idx, verse_text in enumerate(chapter, 1):
                            ref = f"{book_name} {ch_idx}:{v_idx}"
                            kjv[ref] = verse_text
                            verse_count += 1
            elif isinstance(data, dict):
                # Object format {book: {chapter: {verse: text}}}
                for book_name, chapters in data.items():
                    if isinstance(chapters, dict):
                        for ch_num, verses in chapters.items():
                            if isinstance(verses, dict):
                                for v_num, text in verses.items():
                                    ref = f"{book_name} {ch_num}:{v_num}"
                                    kjv[ref] = text
                                    verse_count += 1

            if verse_count > 0:
                with open(kjv_path, 'w') as f:
                    json.dump(kjv, f, indent=2)

                print(f"Saved {verse_count} verses to {kjv_path}")
                return kjv

        except Exception as e:
            print(f"Error with {url[:30]}: {e}")
            continue

    print("All sources failed. Creating minimal test data...")
    return create_minimal_kjv(kjv_path)


def create_minimal_kjv(kjv_path):
    """Create minimal KJV data for testing if downloads fail"""
    kjv = {
        "Genesis 1:1": "In the beginning God created the heaven and the earth.",
        "John 1:1": "In the beginning was the Word, and the Word was with God, and the Word was God.",
        "John 3:16": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "Psalm 23:1": "The LORD is my shepherd; I shall not want.",
        "Revelation 22:21": "The grace of our Lord Jesus Christ be with you all. Amen."
    }
    with open(kjv_path, 'w') as f:
        json.dump(kjv, f, indent=2)
    print(f"Created minimal test data ({len(kjv)} verses)")
    return kjv


def load_kjv():
    """Load KJV from local file"""
    kjv_path = DATA_DIR / "kjv.json"

    if not kjv_path.exists():
        return download_kjv()

    with open(kjv_path, 'r') as f:
        return json.load(f)


def download_cross_references():
    """Download cross-references from OpenBible.info"""
    refs_path = DATA_DIR / "cross_refs.json"

    if refs_path.exists():
        print(f"Cross-refs already exist at {refs_path}")
        return load_cross_references()

    print("Downloading cross-references from OpenBible.info...")
    print("(This may take a moment - 340,000+ connections)")

    try:
        # OpenBible format: "From Verse\tTo Verse\tVotes"
        with urllib.request.urlopen(CROSS_REF_URL) as response:
            lines = response.read().decode('utf-8').strip().split('\n')

        cross_refs = {}
        count = 0

        for line in lines[1:]:  # Skip header
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                from_ref = normalize_ref(parts[0])
                to_ref = normalize_ref(parts[1])

                if from_ref not in cross_refs:
                    cross_refs[from_ref] = []
                cross_refs[from_ref].append(to_ref)
                count += 1

        with open(refs_path, 'w') as f:
            json.dump(cross_refs, f, indent=2)

        print(f"Saved {count} cross-references to {refs_path}")
        return cross_refs

    except Exception as e:
        print(f"Error downloading cross-refs: {e}")
        print("Will build basic cross-refs from explicit Scripture quotes")
        return {}


def load_cross_references():
    """Load cross-references from local file"""
    refs_path = DATA_DIR / "cross_refs.json"

    if not refs_path.exists():
        return download_cross_references()

    with open(refs_path, 'r') as f:
        return json.load(f)


def normalize_ref(ref):
    """Normalize Scripture reference to standard format"""
    # Convert "Gen.1.1" to "Genesis 1:1"
    ref = ref.strip()

    abbrev_map = {
        'Gen': 'Genesis', 'Exod': 'Exodus', 'Lev': 'Leviticus',
        'Num': 'Numbers', 'Deut': 'Deuteronomy', 'Josh': 'Joshua',
        'Judg': 'Judges', 'Ruth': 'Ruth', '1Sam': '1 Samuel',
        '2Sam': '2 Samuel', '1Kgs': '1 Kings', '2Kgs': '2 Kings',
        '1Chr': '1 Chronicles', '2Chr': '2 Chronicles', 'Ezra': 'Ezra',
        'Neh': 'Nehemiah', 'Esth': 'Esther', 'Job': 'Job',
        'Ps': 'Psalms', 'Prov': 'Proverbs', 'Eccl': 'Ecclesiastes',
        'Song': 'Song of Solomon', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
        'Lam': 'Lamentations', 'Ezek': 'Ezekiel', 'Dan': 'Daniel',
        'Hos': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos',
        'Obad': 'Obadiah', 'Jonah': 'Jonah', 'Mic': 'Micah',
        'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah',
        'Hag': 'Haggai', 'Zech': 'Zechariah', 'Mal': 'Malachi',
        'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke',
        'John': 'John', 'Acts': 'Acts', 'Rom': 'Romans',
        '1Cor': '1 Corinthians', '2Cor': '2 Corinthians', 'Gal': 'Galatians',
        'Eph': 'Ephesians', 'Phil': 'Philippians', 'Col': 'Colossians',
        '1Thess': '1 Thessalonians', '2Thess': '2 Thessalonians',
        '1Tim': '1 Timothy', '2Tim': '2 Timothy', 'Titus': 'Titus',
        'Phlm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James',
        '1Pet': '1 Peter', '2Pet': '2 Peter', '1John': '1 John',
        '2John': '2 John', '3John': '3 John', 'Jude': 'Jude',
        'Rev': 'Revelation'
    }

    # Handle "Gen.1.1" format
    if '.' in ref:
        parts = ref.split('.')
        if len(parts) >= 3:
            book = abbrev_map.get(parts[0], parts[0])
            return f"{book} {parts[1]}:{parts[2]}"

    return ref


def init_data():
    """Initialize all data files"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=== LOGOS ENGINE DATA INITIALIZATION ===\n")

    kjv = download_kjv()
    if kjv:
        print(f"\nKJV loaded: {len(kjv)} verses")

    refs = download_cross_references()
    if refs:
        total_connections = sum(len(v) for v in refs.values())
        print(f"Cross-refs loaded: {total_connections} connections")

    print("\n=== DATA READY ===")
    return kjv, refs


if __name__ == "__main__":
    init_data()
