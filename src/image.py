#!/usr/bin/env python3
"""
LOGOS ENGINE - Image Generation Module
Creates shareable verse images using ImageMagick

Commands:
    python logos.py image "John 3:16"              # Create verse image
    python logos.py image "Romans 8:28" dark       # Dark theme
    python logos.py image "Psalm 23:1" parchment   # Parchment style

Requires: imagemagick (pkg install imagemagick)

Glory to LOGOS.
"""

import subprocess
import json
import textwrap
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Themes
THEMES = {
    'light': {
        'bg': '#FFFFFF',
        'text': '#1a1a1a',
        'ref': '#666666',
        'border': '#dddddd'
    },
    'dark': {
        'bg': '#1a1a2e',
        'text': '#eeeeff',
        'ref': '#aaaacc',
        'border': '#333355'
    },
    'parchment': {
        'bg': '#f4e4bc',
        'text': '#3d2914',
        'ref': '#5d4934',
        'border': '#c4b49c'
    },
    'royal': {
        'bg': '#1a0a2e',
        'text': '#ffd700',
        'ref': '#cc9900',
        'border': '#4a2a5e'
    }
}


def load_kjv():
    """Load KJV data"""
    kjv_path = DATA_DIR / "kjv.json"
    if kjv_path.exists():
        with open(kjv_path, 'r') as f:
            return json.load(f)
    return {}


def normalize_ref(ref):
    """Normalize reference format"""
    ref = ref.strip()
    if ref.startswith("Psalm ") and not ref.startswith("Psalms "):
        ref = "Psalms " + ref[6:]
    return ref


def wrap_text(text, width=40):
    """Wrap text for image"""
    return textwrap.fill(text, width=width)


def generate_verse_image(ref, theme='parchment', width=800, height=600):
    """Generate a shareable verse image"""
    ref = normalize_ref(ref)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load verse
    kjv = load_kjv()
    if ref not in kjv:
        print(f"Verse not found: {ref}")
        return None

    verse_text = kjv[ref]

    # Get theme colors
    colors = THEMES.get(theme, THEMES['parchment'])

    # Wrap text
    wrapped = wrap_text(verse_text, width=45)
    lines = wrapped.split('\n')

    # Safe filename
    safe_name = ref.replace(" ", "_").replace(":", "_")
    output_path = OUTPUT_DIR / f"{safe_name}_{theme}.png"

    # Build ImageMagick command
    # Create base image with background
    cmd = [
        'convert',
        '-size', f'{width}x{height}',
        f'xc:{colors["bg"]}',
        # Add border
        '-bordercolor', colors['border'],
        '-border', '10',
        # Add reference at top
        '-font', 'DejaVu-Sans-Bold',
        '-pointsize', '28',
        '-fill', colors['ref'],
        '-gravity', 'North',
        '-annotate', '+0+40', ref,
        # Add verse text centered
        '-font', 'DejaVu-Sans',
        '-pointsize', '24',
        '-fill', colors['text'],
        '-gravity', 'Center',
        '-annotate', '+0+0', wrapped,
        # Add attribution at bottom
        '-pointsize', '14',
        '-fill', colors['ref'],
        '-gravity', 'South',
        '-annotate', '+0+20', 'LOGOS ENGINE - KJV 1611',
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"\n=== VERSE IMAGE CREATED ===\n")
            print(f"Reference: {ref}")
            print(f"Theme: {theme}")
            print(f"Output: {output_path}")
            print(f"\n{verse_text}\n")
            return str(output_path)
        else:
            print(f"ImageMagick error: {result.stderr}")
            return None

    except FileNotFoundError:
        print("ImageMagick not installed. Install with: pkg install imagemagick")
        return None


def list_themes():
    """Show available themes"""
    print("\n=== AVAILABLE THEMES ===\n")
    for name, colors in THEMES.items():
        print(f"  {name}:")
        print(f"    Background: {colors['bg']}")
        print(f"    Text: {colors['text']}")
        print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ref = sys.argv[1]
        theme = sys.argv[2] if len(sys.argv) > 2 else 'parchment'
        generate_verse_image(ref, theme)
    else:
        list_themes()
