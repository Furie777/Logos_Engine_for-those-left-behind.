#!/usr/bin/env python3
"""
Parse Strong's XML files into JSON database
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def parse_hebrew_xml():
    """Parse HebrewStrong.xml"""
    xml_path = DATA_DIR / "HebrewStrong.xml"
    if not xml_path.exists():
        print("HebrewStrong.xml not found")
        return {}

    print("Parsing Hebrew Strong's XML...")

    # Use regex - more reliable for this format
    hebrew = {}

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match entries
    entry_pattern = r'<entry id="(H?\d+)">(.*?)</entry>'

    for match in re.finditer(entry_pattern, content, re.DOTALL):
        strongs_id = match.group(1)
        if not strongs_id.startswith('H'):
            strongs_id = 'H' + strongs_id
        entry_content = match.group(2)

        data = {'hebrew': '', 'translit': '', 'def': '', 'kjv': ''}

        # Extract Hebrew word from <w> tag
        w_match = re.search(r'<w[^>]*>([^<]+)</w>', entry_content)
        if w_match:
            data['hebrew'] = w_match.group(1)

        # Extract transliteration from xlit attribute
        xlit_match = re.search(r'xlit="([^"]+)"', entry_content)
        if xlit_match:
            data['translit'] = xlit_match.group(1)

        # Extract meaning - look for <def> inside <meaning> or just text
        def_match = re.search(r'<def>([^<]+)</def>', entry_content)
        if def_match:
            data['def'] = def_match.group(1).strip()
        else:
            # Try getting text from <meaning> tag
            meaning_match = re.search(r'<meaning>([^<]*(?:<[^>]+>[^<]*)*)</meaning>', entry_content)
            if meaning_match:
                # Strip tags and get plain text
                meaning_text = re.sub(r'<[^>]+>', '', meaning_match.group(1))
                data['def'] = meaning_text.strip()[:200]

        # Extract usage
        usage_match = re.search(r'<usage>([^<]+)</usage>', entry_content)
        if usage_match:
            data['kjv'] = usage_match.group(1).strip()[:150]

        if data['hebrew'] or data['def']:
            hebrew[strongs_id] = data

    print(f"  Parsed {len(hebrew)} Hebrew entries")
    return hebrew


def parse_hebrew_regex(xml_path):
    """Fallback: parse Hebrew XML with regex"""
    print("  Using regex fallback...")
    hebrew = {}

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match entries
    entry_pattern = r'<entry[^>]*id="?(\d+)"?[^>]*>(.*?)</entry>'

    for match in re.finditer(entry_pattern, content, re.DOTALL):
        num = match.group(1)
        strongs_id = f"H{int(num)}"
        entry_content = match.group(2)

        data = {'hebrew': '', 'translit': '', 'def': '', 'kjv': ''}

        # Extract Hebrew word
        w_match = re.search(r'<w[^>]*>([^<]+)</w>', entry_content)
        if w_match:
            data['hebrew'] = w_match.group(1)

        # Extract transliteration
        xlit_match = re.search(r'xlit="([^"]+)"', entry_content)
        if xlit_match:
            data['translit'] = xlit_match.group(1)

        # Extract meaning/definition
        for tag in ['meaning', 'def', 'strongs_def']:
            meaning_match = re.search(rf'<{tag}>([^<]+)</{tag}>', entry_content)
            if meaning_match:
                data['def'] = meaning_match.group(1).strip()[:200]
                break

        if data['hebrew'] or data['def']:
            hebrew[strongs_id] = data

    print(f"  Parsed {len(hebrew)} Hebrew entries (regex)")
    return hebrew


def parse_greek_xml():
    """Parse Greek Strong's XML"""
    xml_path = DATA_DIR / "strongsgreek.xml"
    if not xml_path.exists():
        xml_path = DATA_DIR / "GreekStrong.xml"
    if not xml_path.exists():
        print("Greek Strong's XML not found")
        return {}

    print("Parsing Greek Strong's XML...")

    greek = {}

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for entry in root.iter('entry'):
            strongs_id = entry.get('strongs', '') or entry.get('id', '')
            if not strongs_id:
                continue

            # Normalize to G#### format
            strongs_id = strongs_id.upper()
            if not strongs_id.startswith('G'):
                strongs_id = 'G' + strongs_id.lstrip('0')

            data = {
                'greek': '',
                'translit': '',
                'def': '',
                'kjv': ''
            }

            # Get Greek word
            for elem_name in ['greek', 'word', 'w']:
                for elem in entry.iter(elem_name):
                    if elem.text:
                        data['greek'] = elem.text
                    data['translit'] = elem.get('translit', '') or elem.get('xlit', '')
                    if data['greek']:
                        break
                if data['greek']:
                    break

            # Get definition
            for elem_name in ['strongs_def', 'def', 'meaning', 'definition']:
                for elem in entry.iter(elem_name):
                    if elem.text:
                        data['def'] = elem.text.strip()[:200]
                        break
                if data['def']:
                    break

            # Get KJV usage
            for elem in entry.iter('kjv_def'):
                if elem.text:
                    data['kjv'] = elem.text.strip()[:100]
                    break

            if data['greek'] or data['def']:
                greek[strongs_id] = data

        print(f"  Parsed {len(greek)} Greek entries")

    except ET.ParseError as e:
        print(f"  XML Parse error: {e}")
        greek = parse_greek_regex(xml_path)

    return greek


def parse_greek_regex(xml_path):
    """Fallback: parse Greek XML with regex"""
    print("  Using regex fallback...")
    greek = {}

    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for entries
    entry_pattern = r'<entry[^>]*strongs="?[Gg]?(\d+)"?[^>]*>(.*?)</entry>'

    for match in re.finditer(entry_pattern, content, re.DOTALL):
        num = match.group(1)
        strongs_id = f"G{int(num)}"
        entry_content = match.group(2)

        data = {'greek': '', 'translit': '', 'def': '', 'kjv': ''}

        # Extract Greek word
        greek_match = re.search(r'<greek[^>]*>([^<]+)</greek>', entry_content)
        if greek_match:
            data['greek'] = greek_match.group(1)

        # Extract transliteration
        translit_match = re.search(r'translit="([^"]+)"', entry_content)
        if translit_match:
            data['translit'] = translit_match.group(1)

        # Extract definition
        def_match = re.search(r'<strongs_def>([^<]+)</strongs_def>', entry_content)
        if def_match:
            data['def'] = def_match.group(1).strip()[:200]

        # Extract KJV usage
        kjv_match = re.search(r'<kjv_def>([^<]+)</kjv_def>', entry_content)
        if kjv_match:
            data['kjv'] = kjv_match.group(1).strip()[:100]

        if data['greek'] or data['def']:
            greek[strongs_id] = data

    print(f"  Parsed {len(greek)} Greek entries (regex)")
    return greek


def build_complete_strongs():
    """Build complete Strong's database from XML files"""
    print("="*60)
    print("BUILDING COMPLETE STRONG'S CONCORDANCE")
    print("="*60)

    # Parse both
    hebrew = parse_hebrew_xml()
    greek = parse_greek_xml()

    # Load existing (to preserve our curated entries)
    existing_path = DATA_DIR / "strongs.json"
    existing = {}
    if existing_path.exists():
        with open(existing_path, 'r') as f:
            existing = json.load(f)
        print(f"\nLoaded {len(existing)} existing curated entries")

    # Merge: existing entries take precedence (they're curated)
    combined = {}

    # Add parsed entries first
    combined.update(hebrew)
    combined.update(greek)

    # Overlay existing curated entries (better quality)
    for key, value in existing.items():
        if key in combined:
            # Merge: keep curated definition if better
            if len(value.get('def', value.get('definition', ''))) > len(combined[key].get('def', '')):
                combined[key].update(value)
        else:
            combined[key] = value

    # Save complete database
    output_path = DATA_DIR / "strongs_complete.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    # Also update main strongs.json
    with open(existing_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    # Stats
    h_count = sum(1 for k in combined if k.startswith('H'))
    g_count = sum(1 for k in combined if k.startswith('G'))

    print(f"\n{'='*60}")
    print("COMPLETE STRONG'S DATABASE BUILT")
    print("="*60)
    print(f"Hebrew (H):  {h_count:,}")
    print(f"Greek (G):   {g_count:,}")
    print(f"TOTAL:       {len(combined):,}")
    print(f"\nSaved to: {output_path}")
    print("="*60)

    return combined


if __name__ == "__main__":
    build_complete_strongs()
