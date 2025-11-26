"""
LOGOS ENGINE - Bible API Integration
getBible.net KJVA (1611 KJV with Apocrypha)
"""

import json
import urllib.request
import urllib.parse
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"

# bible-api.com - has KJV with Apocrypha (public, no auth)
API_BASE = "https://bible-api.com"


def fetch_verse(reference, version="kjv"):
    """
    Fetch verse from bible-api.com

    Args:
        reference: "John 3:16" or "Tobit 4:5" or "Wisdom 7:26"
        version: "kjv" (default, includes Apocrypha)

    Returns:
        dict with verse text or None
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Check cache first
    cache_key = f"{version}_{reference.replace(' ', '_').replace(':', '_')}"
    cache_path = CACHE_DIR / f"{cache_key}.json"

    if cache_path.exists():
        with open(cache_path, 'r') as f:
            return json.load(f)

    # Fetch from bible-api.com
    # Format: https://bible-api.com/john%203:16?translation=kjv
    encoded_ref = urllib.parse.quote(reference)
    url = f"{API_BASE}/{encoded_ref}?translation={version}"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LOGOS-Engine/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            # bible-api.com format is simpler
            result = {
                'reference': data.get('reference', reference),
                'verses': []
            }

            for v in data.get('verses', []):
                result['verses'].append({
                    'number': v.get('verse', ''),
                    'text': v.get('text', '').strip()
                })

            # If no verses array, check for direct text
            if not result['verses'] and 'text' in data:
                result['verses'].append({
                    'number': '',
                    'text': data['text'].strip()
                })

            # Cache the result
            if result['verses']:
                with open(cache_path, 'w') as f:
                    json.dump(result, f, indent=2)

            return result

    except Exception as e:
        print(f"API Error: {e}")
        return None


def parse_getbible_response(data, reference):
    """Parse getBible.net JSON response"""
    result = {
        'reference': reference,
        'verses': []
    }

    try:
        for book_data in data.values():
            if isinstance(book_data, dict) and 'chapter' in book_data:
                book_name = book_data.get('book_name', '')
                result['book'] = book_name

                for chapter_data in book_data['chapter'].values():
                    for verse_data in chapter_data.values():
                        if isinstance(verse_data, dict):
                            verse_num = verse_data.get('verse_nr', '')
                            verse_text = verse_data.get('verse', '')
                            result['verses'].append({
                                'number': verse_num,
                                'text': verse_text
                            })

        return result if result['verses'] else None

    except Exception as e:
        print(f"Parse error: {e}")
        return None


def fetch_chapter(book, chapter, version="kjva"):
    """Fetch entire chapter"""
    return fetch_verse(f"{book} {chapter}", version)


def fetch_apocrypha_book(book_name):
    """
    Fetch entire Apocrypha book and cache locally

    Apocrypha books in KJVA:
    - 1 Esdras, 2 Esdras
    - Tobit, Judith
    - Additions to Esther
    - Wisdom of Solomon (Wisdom)
    - Ecclesiasticus (Sirach)
    - Baruch
    - Letter of Jeremiah
    - Prayer of Azariah
    - Susanna
    - Bel and the Dragon
    - Prayer of Manasseh
    - 1 Maccabees, 2 Maccabees
    """
    apocrypha_chapters = {
        '1 Esdras': 9,
        '2 Esdras': 16,
        'Tobit': 14,
        'Judith': 16,
        'Additions to Esther': 6,
        'Wisdom': 19,
        'Wisdom of Solomon': 19,
        'Ecclesiasticus': 51,
        'Sirach': 51,
        'Baruch': 6,
        'Prayer of Azariah': 1,
        'Susanna': 1,
        'Bel and the Dragon': 1,
        'Prayer of Manasseh': 1,
        '1 Maccabees': 16,
        '2 Maccabees': 15
    }

    num_chapters = apocrypha_chapters.get(book_name)
    if not num_chapters:
        print(f"Unknown book: {book_name}")
        print(f"Available: {list(apocrypha_chapters.keys())}")
        return None

    print(f"Fetching {book_name} ({num_chapters} chapters)...")

    book_data = {
        'name': book_name,
        'chapters': {}
    }

    for ch in range(1, num_chapters + 1):
        print(f"  Chapter {ch}...", end=' ', flush=True)
        result = fetch_chapter(book_name, ch)
        if result and result['verses']:
            book_data['chapters'][str(ch)] = result['verses']
            print(f"{len(result['verses'])} verses")
        else:
            print("failed")

    # Save to local file
    safe_name = book_name.replace(' ', '_').lower()
    book_path = DATA_DIR / f"apocrypha_{safe_name}.json"
    with open(book_path, 'w') as f:
        json.dump(book_data, f, indent=2)

    print(f"Saved to {book_path}")
    return book_data


def add_apocrypha_to_kjv():
    """Add all fetched Apocrypha books to main KJV file"""
    kjv_path = DATA_DIR / "kjv.json"

    if not kjv_path.exists():
        print("KJV not found. Run: python logos.py init")
        return

    with open(kjv_path, 'r') as f:
        kjv = json.load(f)

    original_count = len(kjv)

    # Find all apocrypha files
    apocrypha_files = list(DATA_DIR.glob("apocrypha_*.json"))

    for ap_file in apocrypha_files:
        try:
            with open(ap_file, 'r') as f:
                book_data = json.load(f)

            # Skip empty files
            if not book_data:
                continue

            book_name = book_data.get('name', ap_file.stem.replace('apocrypha_', '').replace('_', ' ').title())
            chapters = book_data.get('chapters', {})

            if not chapters:
                continue

            for ch_num, verses in chapters.items():
                for v in verses:
                    verse_num = v.get('verse', v.get('number', ''))
                    verse_text = v.get('text', '')
                    if verse_text:
                        ref = f"{book_name} {ch_num}:{verse_num}"
                        kjv[ref] = verse_text

            print(f"  Added: {book_name}")

        except Exception as e:
            print(f"  Error with {ap_file.name}: {e}")

    # Save updated KJV
    with open(kjv_path, 'w') as f:
        json.dump(kjv, f, indent=2)

    new_count = len(kjv)
    added = new_count - original_count
    print(f"\nAdded {added} Apocrypha verses. Total: {new_count}")


def verse_cli():
    """Command-line verse lookup"""
    import sys
    if len(sys.argv) < 2:
        print("Usage: python api.py <reference>")
        print("Example: python api.py 'John 3:16'")
        print("Example: python api.py 'Tobit 4:5'")
        print("Example: python api.py 'Wisdom 7:26'")
        return

    ref = ' '.join(sys.argv[1:])
    result = fetch_verse(ref)

    if result and result['verses']:
        print(f"\n{result['reference']}:\n")
        for v in result['verses']:
            print(f"  {v['number']}: {v['text']}")
        print()
    else:
        print(f"Could not fetch: {ref}")


if __name__ == "__main__":
    verse_cli()
