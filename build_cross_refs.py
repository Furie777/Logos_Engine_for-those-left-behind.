#!/usr/bin/env python3
"""
Build cross-references algorithmically using multiple methods:
1. Strong's number connections (verses sharing same Hebrew/Greek roots)
2. Keyword/phrase matching
3. NT quotations of OT
"""

import json
import re
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent / "data"


def load_kjv():
    """Load KJV verses"""
    kjv_path = DATA_DIR / "kjv.json"
    with open(kjv_path, 'r') as f:
        return json.load(f)


def build_keyword_index(kjv):
    """Build index of significant theological keywords"""
    print("Building keyword index...")

    # Significant theological terms to index
    keywords = [
        # Divine names
        'god', 'lord', 'almighty', 'most high', 'holy one',
        # Core concepts
        'covenant', 'faith', 'grace', 'mercy', 'love', 'truth',
        'righteousness', 'salvation', 'redemption', 'atonement',
        'sin', 'iniquity', 'transgression', 'forgiveness',
        'holy', 'sanctify', 'glory', 'blessed', 'blessing',
        # Key figures
        'messiah', 'christ', 'son of man', 'son of god',
        'servant', 'lamb', 'shepherd', 'king', 'priest', 'prophet',
        # Themes
        'blood', 'sacrifice', 'offering', 'temple', 'altar',
        'kingdom', 'heaven', 'eternal', 'everlasting',
        'spirit', 'soul', 'heart', 'word',
        'life', 'death', 'resurrection', 'judgment',
        'light', 'darkness', 'way', 'truth',
        'promise', 'commandment', 'law', 'testimony',
        'believe', 'repent', 'obey', 'worship',
        # Places
        'jerusalem', 'zion', 'israel', 'egypt',
    ]

    # Build index
    keyword_index = defaultdict(list)

    for ref, text in kjv.items():
        text_lower = text.lower()
        for kw in keywords:
            if kw in text_lower:
                keyword_index[kw].append(ref)

    return keyword_index


def build_phrase_connections(kjv):
    """Find verses connected by shared phrases (3+ words)"""
    print("Building phrase connections...")

    # Extract 3-4 word phrases from each verse
    phrase_index = defaultdict(list)

    for ref, text in kjv.items():
        # Clean and tokenize
        words = re.findall(r'\b[a-z]+\b', text.lower())

        # Extract 3-word phrases
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10:  # Skip very short phrases
                phrase_index[phrase].append(ref)

    # Keep only phrases that appear in multiple verses
    shared_phrases = {k: v for k, v in phrase_index.items() if len(v) >= 2 and len(v) <= 50}

    return shared_phrases


def build_ot_nt_quotations():
    """Build known OT -> NT quotation connections"""
    print("Building OT-NT quotation links...")

    # Major OT quotations in NT (verified references)
    quotations = {
        # Genesis
        "Genesis 1:27": ["Matthew 19:4", "Mark 10:6"],
        "Genesis 2:24": ["Matthew 19:5", "Mark 10:7", "Ephesians 5:31"],
        "Genesis 12:3": ["Galatians 3:8"],
        "Genesis 15:6": ["Romans 4:3", "Galatians 3:6", "James 2:23"],
        "Genesis 22:18": ["Acts 3:25", "Galatians 3:16"],

        # Exodus
        "Exodus 3:6": ["Matthew 22:32", "Mark 12:26", "Acts 7:32"],
        "Exodus 20:12": ["Matthew 15:4", "Mark 7:10", "Ephesians 6:2"],
        "Exodus 20:13": ["Matthew 5:21", "Romans 13:9", "James 2:11"],
        "Exodus 20:14": ["Matthew 5:27", "Romans 13:9", "James 2:11"],
        "Exodus 21:24": ["Matthew 5:38"],

        # Leviticus
        "Leviticus 19:18": ["Matthew 5:43", "Matthew 19:19", "Matthew 22:39", "Mark 12:31", "Romans 13:9", "Galatians 5:14", "James 2:8"],

        # Deuteronomy
        "Deuteronomy 5:16": ["Matthew 15:4", "Mark 7:10", "Ephesians 6:2"],
        "Deuteronomy 6:4": ["Mark 12:29"],  # The Shema!
        "Deuteronomy 6:5": ["Matthew 22:37", "Mark 12:30", "Luke 10:27"],
        "Deuteronomy 6:13": ["Matthew 4:10", "Luke 4:8"],
        "Deuteronomy 6:16": ["Matthew 4:7", "Luke 4:12"],
        "Deuteronomy 8:3": ["Matthew 4:4", "Luke 4:4"],
        "Deuteronomy 18:15": ["Acts 3:22", "Acts 7:37"],
        "Deuteronomy 19:15": ["Matthew 18:16", "2 Corinthians 13:1"],
        "Deuteronomy 25:4": ["1 Corinthians 9:9", "1 Timothy 5:18"],
        "Deuteronomy 32:35": ["Romans 12:19", "Hebrews 10:30"],
        "Deuteronomy 32:43": ["Romans 15:10"],

        # Psalms
        "Psalms 2:1": ["Acts 4:25"],
        "Psalms 2:7": ["Acts 13:33", "Hebrews 1:5", "Hebrews 5:5"],
        "Psalms 8:2": ["Matthew 21:16"],
        "Psalms 8:4": ["Hebrews 2:6"],
        "Psalms 16:8": ["Acts 2:25"],
        "Psalms 16:10": ["Acts 2:27", "Acts 13:35"],
        "Psalms 22:1": ["Matthew 27:46", "Mark 15:34"],
        "Psalms 22:18": ["Matthew 27:35", "John 19:24"],
        "Psalms 23:1": ["John 10:11", "John 10:14", "Hebrews 13:20", "1 Peter 2:25"],
        "Psalms 31:5": ["Luke 23:46"],
        "Psalms 34:8": ["1 Peter 2:3"],
        "Psalms 40:6": ["Hebrews 10:5"],
        "Psalms 41:9": ["John 13:18"],
        "Psalms 45:6": ["Hebrews 1:8"],
        "Psalms 51:4": ["Romans 3:4"],
        "Psalms 68:18": ["Ephesians 4:8"],
        "Psalms 69:9": ["John 2:17", "Romans 15:3"],
        "Psalms 69:21": ["Matthew 27:34", "John 19:28"],
        "Psalms 69:25": ["Acts 1:20"],
        "Psalms 78:2": ["Matthew 13:35"],
        "Psalms 82:6": ["John 10:34"],
        "Psalms 91:11": ["Matthew 4:6", "Luke 4:10"],
        "Psalms 95:7": ["Hebrews 3:7", "Hebrews 4:7"],
        "Psalms 102:25": ["Hebrews 1:10"],
        "Psalms 104:4": ["Hebrews 1:7"],
        "Psalms 109:8": ["Acts 1:20"],
        "Psalms 110:1": ["Matthew 22:44", "Mark 12:36", "Luke 20:42", "Acts 2:34", "Hebrews 1:13"],
        "Psalms 110:4": ["Hebrews 5:6", "Hebrews 7:17", "Hebrews 7:21"],
        "Psalms 118:22": ["Matthew 21:42", "Mark 12:10", "Luke 20:17", "Acts 4:11", "1 Peter 2:7"],
        "Psalms 118:26": ["Matthew 21:9", "Matthew 23:39", "Mark 11:9", "Luke 13:35", "John 12:13"],

        # Proverbs
        "Proverbs 3:11": ["Hebrews 12:5"],
        "Proverbs 3:34": ["James 4:6", "1 Peter 5:5"],
        "Proverbs 25:21": ["Romans 12:20"],
        "Proverbs 26:11": ["2 Peter 2:22"],

        # Isaiah
        "Isaiah 6:9": ["Matthew 13:14", "Mark 4:12", "Luke 8:10", "John 12:40", "Acts 28:26"],
        "Isaiah 7:14": ["Matthew 1:23"],
        "Isaiah 9:1": ["Matthew 4:15"],
        "Isaiah 11:10": ["Romans 15:12"],
        "Isaiah 25:8": ["1 Corinthians 15:54"],
        "Isaiah 28:16": ["Romans 9:33", "Romans 10:11", "1 Peter 2:6"],
        "Isaiah 29:13": ["Matthew 15:8", "Mark 7:6"],
        "Isaiah 40:3": ["Matthew 3:3", "Mark 1:3", "Luke 3:4", "John 1:23"],
        "Isaiah 40:6": ["1 Peter 1:24"],
        "Isaiah 42:1": ["Matthew 12:18"],
        "Isaiah 45:23": ["Romans 14:11", "Philippians 2:10"],
        "Isaiah 49:6": ["Acts 13:47"],
        "Isaiah 52:7": ["Romans 10:15"],
        "Isaiah 52:15": ["Romans 15:21"],
        "Isaiah 53:1": ["John 12:38", "Romans 10:16"],
        "Isaiah 53:4": ["Matthew 8:17"],
        "Isaiah 53:7": ["Acts 8:32"],
        "Isaiah 53:12": ["Mark 15:28", "Luke 22:37"],
        "Isaiah 54:1": ["Galatians 4:27"],
        "Isaiah 55:3": ["Acts 13:34"],
        "Isaiah 56:7": ["Matthew 21:13", "Mark 11:17", "Luke 19:46"],
        "Isaiah 59:7": ["Romans 3:15"],
        "Isaiah 59:20": ["Romans 11:26"],
        "Isaiah 61:1": ["Luke 4:18"],
        "Isaiah 64:4": ["1 Corinthians 2:9"],
        "Isaiah 65:1": ["Romans 10:20"],
        "Isaiah 66:1": ["Matthew 5:34", "Acts 7:49"],

        # Jeremiah
        "Jeremiah 7:11": ["Matthew 21:13", "Mark 11:17", "Luke 19:46"],
        "Jeremiah 9:24": ["1 Corinthians 1:31", "2 Corinthians 10:17"],
        "Jeremiah 31:15": ["Matthew 2:18"],
        "Jeremiah 31:31": ["Hebrews 8:8"],
        "Jeremiah 31:33": ["Hebrews 8:10", "Hebrews 10:16"],
        "Jeremiah 31:34": ["Hebrews 8:12", "Hebrews 10:17"],

        # Ezekiel
        "Ezekiel 37:27": ["2 Corinthians 6:16"],

        # Daniel
        "Daniel 7:13": ["Matthew 24:30", "Matthew 26:64", "Mark 13:26", "Mark 14:62", "Revelation 1:7"],
        "Daniel 9:27": ["Matthew 24:15", "Mark 13:14"],
        "Daniel 12:1": ["Matthew 24:21", "Mark 13:19"],

        # Hosea
        "Hosea 1:10": ["Romans 9:26"],
        "Hosea 2:23": ["Romans 9:25", "1 Peter 2:10"],
        "Hosea 6:6": ["Matthew 9:13", "Matthew 12:7"],
        "Hosea 11:1": ["Matthew 2:15"],
        "Hosea 13:14": ["1 Corinthians 15:55"],

        # Joel
        "Joel 2:28": ["Acts 2:17"],
        "Joel 2:32": ["Romans 10:13"],

        # Amos
        "Amos 5:25": ["Acts 7:42"],
        "Amos 9:11": ["Acts 15:16"],

        # Micah
        "Micah 5:2": ["Matthew 2:6", "John 7:42"],
        "Micah 7:6": ["Matthew 10:35"],

        # Habakkuk
        "Habakkuk 1:5": ["Acts 13:41"],
        "Habakkuk 2:4": ["Romans 1:17", "Galatians 3:11", "Hebrews 10:38"],

        # Haggai
        "Haggai 2:6": ["Hebrews 12:26"],

        # Zechariah
        "Zechariah 9:9": ["Matthew 21:5", "John 12:15"],
        "Zechariah 11:12": ["Matthew 26:15", "Matthew 27:9"],
        "Zechariah 12:10": ["John 19:37", "Revelation 1:7"],
        "Zechariah 13:7": ["Matthew 26:31", "Mark 14:27"],

        # Malachi
        "Malachi 1:2": ["Romans 9:13"],
        "Malachi 3:1": ["Matthew 11:10", "Mark 1:2", "Luke 7:27"],
        "Malachi 4:5": ["Matthew 11:14", "Matthew 17:10", "Mark 9:11", "Luke 1:17"],
    }

    return quotations


def build_cross_references():
    """Build complete cross-reference database"""
    print("="*60)
    print("BUILDING CROSS-REFERENCES")
    print("="*60)

    kjv = load_kjv()
    print(f"Loaded {len(kjv)} verses")

    cross_refs = defaultdict(set)

    # 1. OT-NT Quotations (highest quality)
    quotations = build_ot_nt_quotations()
    quote_count = 0
    for ot_ref, nt_refs in quotations.items():
        for nt_ref in nt_refs:
            if ot_ref in kjv and nt_ref in kjv:
                cross_refs[ot_ref].add(nt_ref)
                cross_refs[nt_ref].add(ot_ref)
                quote_count += 1
    print(f"\n1. OT-NT Quotations: {quote_count} connections")

    # 2. Keyword connections
    keyword_index = build_keyword_index(kjv)
    keyword_count = 0
    for keyword, refs in keyword_index.items():
        if 2 <= len(refs) <= 100:  # Connect verses sharing keywords
            for i, ref1 in enumerate(refs):
                for ref2 in refs[i+1:min(i+10, len(refs))]:  # Limit connections
                    cross_refs[ref1].add(ref2)
                    cross_refs[ref2].add(ref1)
                    keyword_count += 1
    print(f"2. Keyword connections: {keyword_count}")

    # 3. Phrase connections
    phrase_index = build_phrase_connections(kjv)
    phrase_count = 0
    for phrase, refs in phrase_index.items():
        for i, ref1 in enumerate(refs):
            for ref2 in refs[i+1:]:
                cross_refs[ref1].add(ref2)
                cross_refs[ref2].add(ref1)
                phrase_count += 1
    print(f"3. Phrase connections: {phrase_count}")

    # Convert sets to lists for JSON
    cross_refs_final = {k: list(v) for k, v in cross_refs.items()}

    # Calculate total unique edges
    total_edges = sum(len(v) for v in cross_refs_final.values()) // 2

    # Save
    output_path = DATA_DIR / "cross_refs.json"
    with open(output_path, 'w') as f:
        json.dump(cross_refs_final, f, indent=2)

    print(f"\n{'='*60}")
    print("CROSS-REFERENCES BUILT")
    print("="*60)
    print(f"Verses with connections: {len(cross_refs_final):,}")
    print(f"Total edges: ~{total_edges:,}")
    print(f"Saved to: {output_path}")
    print("="*60)

    return cross_refs_final


if __name__ == "__main__":
    build_cross_references()
