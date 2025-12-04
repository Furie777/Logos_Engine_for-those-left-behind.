#!/usr/bin/env python3
"""
LOGOS ENGINE - QR Code Module
Generate scannable QR codes for verses

Commands:
    python logos.py qr "John 3:16"         # QR code with verse text
    python logos.py qr "Romans 8:28" link  # QR code with Bible link
    python logos.py qr "Psalm 23:1" mini   # Smaller QR code

The QR codes can be:
- Printed and shared
- Scanned to read the verse
- Used in study materials

Requires: qrcode (pip install qrcode[pil])

Glory to LOGOS.
"""

import json
from pathlib import Path

try:
    import qrcode
    from PIL import Image
    HAS_QR = True
except ImportError:
    HAS_QR = False

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


def generate_qr(ref, mode='text', size='normal'):
    """
    Generate QR code for a verse.

    mode:
      - 'text': QR contains the verse text
      - 'link': QR contains a link to BibleGateway
      - 'ref': QR contains just the reference

    size: 'mini', 'normal', 'large'
    """
    if not HAS_QR:
        print("QR code library not installed.")
        print("Install with: pip install qrcode[pil]")
        return None

    ref = normalize_ref(ref)
    kjv = load_kjv()

    if ref not in kjv:
        print(f"Verse not found: {ref}")
        return None

    verse_text = kjv[ref]

    # Determine QR content based on mode
    if mode == 'link':
        # Create BibleGateway link
        book_chapter_verse = ref.replace(" ", "+")
        content = f"https://www.biblegateway.com/passage/?search={book_chapter_verse}&version=KJV"
    elif mode == 'ref':
        content = ref
    else:
        # Full verse text
        content = f"{ref}\n\n{verse_text}"

    # Size settings
    sizes = {
        'mini': (1, 4),
        'normal': (2, 6),
        'large': (3, 8)
    }
    box_size, border = sizes.get(size, (2, 6))

    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size * 5,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Safe filename
    safe_name = ref.replace(" ", "_").replace(":", "_")
    output_path = OUTPUT_DIR / f"{safe_name}_qr_{mode}.png"

    img.save(str(output_path))

    print(f"\n=== QR CODE GENERATED ===")
    print(f"Reference: {ref}")
    print(f"Mode: {mode}")
    print(f"Size: {size}")
    print(f"Output: {output_path}")
    print(f"\n{verse_text[:100]}{'...' if len(verse_text) > 100 else ''}\n")

    return str(output_path)


def generate_qr_batch(refs, mode='link'):
    """Generate QR codes for multiple verses"""
    if not HAS_QR:
        print("QR code library not installed.")
        return []

    results = []
    for ref in refs:
        path = generate_qr(ref, mode=mode)
        if path:
            results.append(path)

    print(f"\nGenerated {len(results)} QR codes.")
    return results


def terminal_qr(ref):
    """Print QR code in terminal using ASCII"""
    if not HAS_QR:
        print("QR code library not installed.")
        return

    ref = normalize_ref(ref)
    kjv = load_kjv()

    if ref not in kjv:
        print(f"Verse not found: {ref}")
        return

    verse_text = kjv[ref]
    content = f"{ref}\n{verse_text}"

    # Generate QR with ASCII output
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(content)
    qr.make(fit=True)

    # Print to terminal
    print(f"\n{ref}")
    qr.print_ascii(invert=True)
    print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ref = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else 'text'
        generate_qr(ref, mode)
    else:
        print("Usage: python qr.py <reference> [text|link|ref]")
