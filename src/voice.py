#!/usr/bin/env python3
"""
LOGOS ENGINE - Voice Module
Text-to-speech for Scripture reading

Commands:
    python logos.py speak "John 3:16"          # Speak a verse
    python logos.py speak "Psalm 23" slow      # Slower speech
    python logos.py audio "Romans 8:28"        # Save to audio file

Requires: espeak (pkg install espeak)
Optional: termux-tts-speak (uses Android TTS)

Glory to LOGOS.
"""

import subprocess
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


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


def speak_verse(ref, speed='normal', use_android=False):
    """
    Speak a verse using text-to-speech.

    speed: 'slow', 'normal', 'fast'
    use_android: Use termux-tts-speak instead of espeak
    """
    ref = normalize_ref(ref)
    kjv = load_kjv()

    if ref not in kjv:
        print(f"Verse not found: {ref}")
        return False

    verse_text = kjv[ref]
    full_text = f"{ref}. {verse_text}"

    # Speed settings for espeak
    speeds = {
        'slow': 120,
        'normal': 160,
        'fast': 200
    }
    rate = speeds.get(speed, 160)

    print(f"\n{ref}")
    print(f"{verse_text}\n")
    print(f"Speaking... ({speed})")

    if use_android:
        # Use Android TTS via termux-api
        try:
            subprocess.run(
                ['termux-tts-speak', '-r', str(rate/160), full_text],
                check=True
            )
            return True
        except FileNotFoundError:
            print("termux-tts-speak not available. Install termux-api.")
            return False
    else:
        # Use espeak
        try:
            subprocess.run(
                ['espeak', '-s', str(rate), '-v', 'en', full_text],
                check=True
            )
            return True
        except FileNotFoundError:
            print("espeak not installed. Install with: pkg install espeak")
            return False


def save_audio(ref, output_format='wav'):
    """Save verse as audio file"""
    ref = normalize_ref(ref)
    kjv = load_kjv()

    if ref not in kjv:
        print(f"Verse not found: {ref}")
        return None

    verse_text = kjv[ref]
    full_text = f"{ref}. {verse_text}"

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Safe filename
    safe_name = ref.replace(" ", "_").replace(":", "_")
    output_path = OUTPUT_DIR / f"{safe_name}.{output_format}"

    try:
        subprocess.run(
            ['espeak', '-v', 'en', '-w', str(output_path), full_text],
            check=True,
            capture_output=True
        )

        print(f"\n=== AUDIO SAVED ===")
        print(f"Reference: {ref}")
        print(f"Output: {output_path}")
        print(f"\n{verse_text}\n")

        return str(output_path)

    except FileNotFoundError:
        print("espeak not installed. Install with: pkg install espeak")
        return None


def speak_chapter(book_chapter, speed='normal', pause=2):
    """Speak an entire chapter"""
    kjv = load_kjv()

    # Find all verses in this chapter
    verses = []
    for ref in kjv.keys():
        if ref.startswith(book_chapter):
            verses.append(ref)

    if not verses:
        print(f"No verses found for: {book_chapter}")
        return

    # Sort by verse number
    def verse_num(ref):
        try:
            return int(ref.split(':')[1])
        except:
            return 0

    verses.sort(key=verse_num)

    print(f"\n=== SPEAKING: {book_chapter} ===")
    print(f"Verses: {len(verses)}")
    print()

    for ref in verses:
        speak_verse(ref, speed=speed)


def list_voices():
    """List available espeak voices"""
    try:
        result = subprocess.run(
            ['espeak', '--voices'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("espeak not installed.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ref = sys.argv[1]
        speed = sys.argv[2] if len(sys.argv) > 2 else 'normal'
        speak_verse(ref, speed)
    else:
        print("Usage: python voice.py <reference> [slow|normal|fast]")
