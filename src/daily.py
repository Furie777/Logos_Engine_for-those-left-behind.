#!/usr/bin/env python3
"""
LOGOS ENGINE - Daily Verse Module
Generate a verse for the day based on date (deterministic)

Commands:
    python logos.py daily              # Today's verse
    python logos.py daily 2025-12-25   # Verse for specific date

Same date = same verse. Shareable and reproducible.

Glory to LOGOS.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def load_kjv():
    """Load KJV data"""
    kjv_path = DATA_DIR / "kjv.json"
    if kjv_path.exists():
        with open(kjv_path, 'r') as f:
            return json.load(f)
    return {}


def get_daily_verse(date_str=None):
    """
    Get the verse of the day.

    Uses a hash of the date to deterministically select a verse.
    Same date = same verse, every time, anywhere.
    """
    kjv = load_kjv()
    if not kjv:
        return None, None

    # Use today's date if not specified
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # Create deterministic hash from date
    hash_input = f"LOGOS-{date_str}"
    hash_bytes = hashlib.sha256(hash_input.encode()).digest()
    index = int.from_bytes(hash_bytes[:4], 'big') % len(kjv)

    # Get verse at that index
    refs = list(kjv.keys())
    ref = refs[index]
    text = kjv[ref]

    return ref, text, date_str


def show_daily_verse(date_str=None, with_banner=True):
    """Display the daily verse"""
    result = get_daily_verse(date_str)
    if not result or result[0] is None:
        print("Could not load daily verse.")
        return None

    ref, text, date = result

    if with_banner:
        # Try figlet banner
        try:
            import subprocess
            banner = subprocess.run(
                ['figlet', '-f', 'small', 'Daily Word'],
                capture_output=True, text=True
            ).stdout
            print(banner)
        except:
            print("=" * 50)
            print("         DAILY WORD")
            print("=" * 50)

    print(f"Date: {date}")
    print()
    print(f"{ref}")
    print(f"{text}")
    print()

    return ref


def get_weekly_verses(start_date=None):
    """Get verses for the current week"""
    from datetime import timedelta

    if start_date is None:
        today = datetime.now()
        # Get Monday of this week
        start = today - timedelta(days=today.weekday())
    else:
        start = datetime.strptime(start_date, '%Y-%m-%d')

    verses = []
    for i in range(7):
        date = start + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        ref, text, _ = get_daily_verse(date_str)
        day_name = date.strftime('%A')
        verses.append((day_name, date_str, ref, text))

    return verses


def show_weekly():
    """Show verses for the week"""
    print("\n=== THIS WEEK'S VERSES ===\n")

    verses = get_weekly_verses()
    for day_name, date_str, ref, text in verses:
        print(f"{day_name} ({date_str})")
        print(f"  {ref}")
        print(f"  {text[:80]}...")
        print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'week':
            show_weekly()
        else:
            show_daily_verse(sys.argv[1])
    else:
        show_daily_verse()
