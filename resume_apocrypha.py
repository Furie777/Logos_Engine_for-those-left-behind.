#!/usr/bin/env python3
"""
Resume downloading missing Apocrypha chapters
Run multiple times with breaks between to avoid rate limiting
"""
import sys
sys.path.insert(0, '.')

from src.api import fetch_verse, DATA_DIR
import json
import time

# Missing chapters to download (from rate limiting)
MISSING = {
    "2 Esdras": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "Tobit": [1, 2, 3, 4, 5],
    "Judith": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "Wisdom of Solomon": [14, 15, 16, 17, 18, 19],
    "Sirach": list(range(1, 18)) + list(range(33, 52)),
    "Baruch": [1, 2, 3, 4],
    "1 Maccabees": [10, 11, 12, 13, 14, 15, 16],
    "2 Maccabees": list(range(1, 16)),
}

def resume_download(book_name, chapters, delay=3):
    """Download missing chapters with longer delays"""
    safe_name = book_name.replace(' ', '_').lower()
    book_path = DATA_DIR / f"apocrypha_{safe_name}.json"

    # Load existing data
    if book_path.exists():
        with open(book_path, 'r') as f:
            book_data = json.load(f)
    else:
        book_data = {'name': book_name, 'chapters': {}, 'verse_count': 0}

    print(f"\n{book_name}: {len(chapters)} chapters to fetch")

    for ch in chapters:
        ch_str = str(ch)
        if ch_str in book_data['chapters'] and book_data['chapters'][ch_str]:
            print(f"  Chapter {ch}: already have {len(book_data['chapters'][ch_str])} verses")
            continue

        print(f"  Chapter {ch}...", end=' ', flush=True)

        result = fetch_verse(f"{book_name} {ch}")

        if result and result['verses']:
            book_data['chapters'][ch_str] = []
            for v in result['verses']:
                book_data['chapters'][ch_str].append({
                    'verse': v['number'],
                    'text': v['text']
                })
            print(f"{len(result['verses'])} verses")
        else:
            print("rate limited - try again later")
            # Save what we have and exit
            break

        time.sleep(delay)  # Longer delay

    # Recalculate verse count
    book_data['verse_count'] = sum(len(v) for v in book_data['chapters'].values())

    # Save
    with open(book_path, 'w') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)

    print(f"  Saved: {book_data['verse_count']} verses total")


def main():
    print("="*60)
    print("RESUME APOCRYPHA DOWNLOAD")
    print("Using 5-second delays to avoid rate limiting")
    print("="*60)

    for book, chapters in MISSING.items():
        try:
            resume_download(book, chapters, delay=5)
        except KeyboardInterrupt:
            print("\nStopped. Run again later to continue.")
            break

    print("\nDone! Run 'python3 logos.py merge' to update KJV")


if __name__ == "__main__":
    main()
