#!/usr/bin/env python3
"""
LOGOS ENGINE - Fuzzy Search Module
Interactive verse selection using fzf

Commands:
    python logos.py fzf                # Fuzzy search all verses
    python logos.py fzf grace          # Pre-filter by keyword
    python logos.py pick               # Pick a verse interactively

Requires: fzf (pkg install fzf)

Glory to LOGOS.
"""

import subprocess
import json
from pathlib import Path

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


def fuzzy_search(prefilter=None, preview=True):
    """
    Interactive fuzzy search through all verses.
    Returns selected verse reference.
    """
    kjv = load_kjv()

    if not kjv:
        print("No KJV data found.")
        return None

    # Build list of verses
    lines = []
    for ref, text in kjv.items():
        # Truncate for display
        display_text = text[:100] + "..." if len(text) > 100 else text
        lines.append(f"{ref}\t{display_text}")

    # Pre-filter if keyword provided
    if prefilter:
        prefilter_lower = prefilter.lower()
        lines = [l for l in lines if prefilter_lower in l.lower()]

    if not lines:
        print(f"No verses match: {prefilter}")
        return None

    # Write to temp input
    input_text = '\n'.join(lines)

    # Build fzf command
    fzf_cmd = [
        'fzf',
        '--height', '50%',
        '--layout', 'reverse',
        '--border',
        '--header', f'LOGOS ENGINE - {len(lines)} verses',
        '--prompt', 'Search: ',
        '--delimiter', '\t',
        '--with-nth', '1,2',
    ]

    if preview:
        # Preview shows full verse
        fzf_cmd.extend([
            '--preview', 'echo {} | cut -f1 | xargs -I{} grep -F "{}" ' + str(DATA_DIR / 'kjv.json') + ' | head -5',
            '--preview-window', 'down:3:wrap'
        ])

    try:
        result = subprocess.run(
            fzf_cmd,
            input=input_text,
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout.strip():
            # Extract reference from selection
            selected = result.stdout.strip()
            ref = selected.split('\t')[0]
            return ref
        else:
            return None

    except FileNotFoundError:
        print("fzf not installed. Install with: pkg install fzf")
        return None


def pick_verse(prefilter=None):
    """Pick a verse and display it"""
    ref = fuzzy_search(prefilter)

    if ref:
        kjv = load_kjv()
        print(f"\n{ref}")
        print(kjv.get(ref, ""))
        print()
        return ref

    return None


def pick_and_graph(prefilter=None):
    """Pick a verse and generate its graph"""
    ref = fuzzy_search(prefilter)

    if ref:
        from src.visualize import generate_graph
        generate_graph(ref, depth=1)
        return ref

    return None


def pick_and_image(prefilter=None, theme='parchment'):
    """Pick a verse and generate its image"""
    ref = fuzzy_search(prefilter)

    if ref:
        from src.image import generate_verse_image
        generate_verse_image(ref, theme)
        return ref

    return None


if __name__ == "__main__":
    import sys
    prefilter = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else None
    pick_verse(prefilter)
