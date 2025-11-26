#!/usr/bin/env python3
"""
Download all 14 Apocrypha books from bible-api.com
"""
import sys
sys.path.insert(0, '.')

from src.api import fetch_verse, DATA_DIR
import json
import time

APOCRYPHA_BOOKS = [
    ("1 Esdras", 9),
    ("2 Esdras", 16),
    ("Tobit", 14),
    ("Judith", 16),
    ("Esther (Greek)", 16),  # Additions to Esther / Rest of Esther
    ("Wisdom of Solomon", 19),
    ("Sirach", 51),  # Ecclesiasticus
    ("Baruch", 5),
    ("Letter of Jeremiah", 1),  # Sometimes Baruch 6
    ("Prayer of Azariah", 1),  # Song of Three Children
    ("Susanna", 1),
    ("Bel and the Dragon", 1),
    ("Prayer of Manasseh", 1),
    ("1 Maccabees", 16),
    ("2 Maccabees", 15),
]

def download_book(name, chapters):
    """Download a single book"""
    print(f"\n{'='*50}")
    print(f"DOWNLOADING: {name} ({chapters} chapters)")
    print('='*50)

    book_data = {
        'name': name,
        'chapters': {},
        'verse_count': 0
    }

    for ch in range(1, chapters + 1):
        print(f"  Chapter {ch}...", end=' ', flush=True)

        # Fetch entire chapter
        ref = f"{name} {ch}"
        result = fetch_verse(ref)

        if result and result['verses']:
            book_data['chapters'][str(ch)] = []
            for v in result['verses']:
                book_data['chapters'][str(ch)].append({
                    'verse': v['number'],
                    'text': v['text']
                })
                book_data['verse_count'] += 1
            print(f"{len(result['verses'])} verses")
        else:
            print("(no data or error)")

        # Be nice to the API
        time.sleep(0.5)

    # Save book
    safe_name = name.replace(' ', '_').replace('(', '').replace(')', '').lower()
    book_path = DATA_DIR / f"apocrypha_{safe_name}.json"
    with open(book_path, 'w') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved: {book_path}")
    print(f"Total verses: {book_data['verse_count']}")

    return book_data['verse_count']


def download_all():
    """Download all Apocrypha books"""
    print("\n" + "="*60)
    print("LOGOS ENGINE - APOCRYPHA DOWNLOAD")
    print("1611 King James Version - 14 Books")
    print("="*60)

    total_verses = 0
    successful = 0

    for name, chapters in APOCRYPHA_BOOKS:
        try:
            verses = download_book(name, chapters)
            total_verses += verses
            if verses > 0:
                successful += 1
        except Exception as e:
            print(f"ERROR downloading {name}: {e}")

    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print(f"Books downloaded: {successful}/{len(APOCRYPHA_BOOKS)}")
    print(f"Total Apocrypha verses: {total_verses}")
    print(f"\nRun 'python3 logos.py merge' to add to main KJV")
    print("="*60)


if __name__ == "__main__":
    download_all()
