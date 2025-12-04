#!/usr/bin/env python3
"""
LOGOS ENGINE - Main CLI
Scripture as Network Topology | KJV 1611 Edition (with Apocrypha structure)

Usage:
    python logos.py init       # Download KJV + setup data
    python logos.py build      # Build network graph
    python logos.py query      # Interactive query mode
    python logos.py stats      # Show graph statistics
    python logos.py verse <ref>     # Get specific verse
    python logos.py search <term>   # Search verses
    python logos.py witness <term>  # Three-witness pattern

    CONCORDANCE (Hebrew/Greek):
    python logos.py concordance     # Interactive concordance
    python logos.py study <word>    # Word study with Strong's
    python logos.py strongs <H/G#>  # Strong's definition
    python logos.py hebrew          # List Hebrew words
    python logos.py greek           # List Greek words

    APOCRYPHA (1611 KJV):
    python logos.py fetch <ref>         # Fetch verse from API (works with Apocrypha)
    python logos.py apocrypha <book>    # Download entire Apocrypha book
    python logos.py merge               # Merge Apocrypha into main KJV

    SEMANTIC SEARCH:
    python logos.py semantic            # Interactive semantic search
    python logos.py similar <ref>       # Find semantically similar verses
    python logos.py meaning <query>     # Search by meaning
    python logos.py concept <name>      # Search by theological concept

    INTEGRITY (Autoimmune System):
    python logos.py verify              # Verify all data checksums
    python logos.py integrity           # Interactive integrity checker
    python logos.py diagnose <file>     # Diagnose specific file

    VISUALIZATION (Graphviz):
    python logos.py graph <ref>         # Generate visual network map
    python logos.py graph <ref> <depth> # Deeper traversal (default: 1)
    python logos.py banner <text>       # ASCII art banner

    IMAGE GENERATION (ImageMagick):
    python logos.py image <ref>         # Create shareable verse image
    python logos.py image <ref> <theme> # Themes: light, dark, parchment, royal

    FUZZY SEARCH (fzf):
    python logos.py fzf                 # Interactive verse picker
    python logos.py fzf <keyword>       # Pre-filter by keyword
    python logos.py pick                # Pick and display verse

    NETWORK TRAVERSAL:
    python logos.py chain <start> <end> # Shortest path between verses
    python logos.py bridge <ref1> <ref2> # Find common connections
    python logos.py genesis-revelation   # The great chain (Gen 3:15 → Rev 22:21)

    VOICE (Text-to-Speech):
    python logos.py speak <ref>         # Speak a verse aloud
    python logos.py speak <ref> slow    # Slower speech
    python logos.py audio <ref>         # Save verse as audio file

    QR CODES:
    python logos.py qr <ref>            # QR code with verse text
    python logos.py qr <ref> link       # QR code with Bible link
    python logos.py qrterm <ref>        # ASCII QR in terminal

    DOCUMENTS:
    python logos.py doc <ref>           # Create verse document (.docx)
    python logos.py doc "Psalm 23"      # Full chapter document
    python logos.py topic <word>        # Topic collection document

    DAILY VERSE:
    python logos.py daily               # Today's verse (deterministic)
    python logos.py daily 2025-12-25    # Verse for specific date
    python logos.py week                # This week's verses
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == 'init':
        from src.loader import init_data
        init_data()

    elif command == 'build':
        from src.graph import build_graph
        build_graph()

    elif command == 'query':
        from src.query import repl
        repl()

    elif command == 'stats':
        from src.graph import load_graph, get_stats
        G = load_graph()
        stats = get_stats(G)

        print("\n=== LOGOS GRAPH STATISTICS ===\n")
        print(f"Verses (nodes):     {stats['nodes']:,}")
        print(f"Connections (edges): {stats['edges']:,}")
        print(f"Density:            {stats['density']:.6f}")
        print(f"Connected:          {stats['is_connected']}")

        print("\n--- Most Central Verses ---")
        for ref, score in stats['top_10_central']:
            print(f"  {ref}: {score:.4f}")

    elif command == 'verse':
        if len(sys.argv) < 3:
            print("Usage: python logos.py verse <reference>")
            return
        ref = ' '.join(sys.argv[2:])
        from src.query import LogosQuery
        logos = LogosQuery()
        result = logos.verse(ref)
        if result:
            print(f"\n{result}\n")
        else:
            print(f"Verse not found: {ref}")

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python logos.py search <term>")
            return
        term = ' '.join(sys.argv[2:])
        from src.query import LogosQuery
        logos = LogosQuery()
        results = logos.search(term)
        print(f"\nFound {len(results)} verses containing '{term}':\n")
        for ref, text in results:
            print(f"{ref}")
            print(f"  {text[:100]}...\n")

    elif command == 'witness':
        if len(sys.argv) < 3:
            print("Usage: python logos.py witness <term>")
            return
        term = ' '.join(sys.argv[2:])
        from src.query import LogosQuery
        logos = LogosQuery()
        results = logos.witness(term)
        print(f"\n=== THREE WITNESSES: {term.upper()} ===\n")
        for i, (ref, text) in enumerate(results, 1):
            print(f"WITNESS {i}: {ref}")
            print(f"{text}\n")

    elif command == 'concordance':
        from src.concordance import repl as conc_repl
        conc_repl()

    elif command == 'study':
        if len(sys.argv) < 3:
            print("Usage: python logos.py study <word>")
            return
        word = ' '.join(sys.argv[2:])
        from src.concordance import Concordance
        conc = Concordance()
        results = conc.word_study(word)

        print(f"\n=== WORD STUDY: {word.upper()} ===\n")
        print(f"Total occurrences in KJV: {results['total_occurrences']}")

        if results['strongs']:
            for s in results['strongs']:
                d = s['definition']
                print(f"\n{s['number']}:")
                translit = d.get('transliteration', d.get('translit', ''))
                meaning = d.get('definition', d.get('def', ''))
                if 'hebrew' in d:
                    print(f"  Hebrew: {d['hebrew']}")
                    print(f"  Transliteration: {translit}")
                if 'greek' in d:
                    print(f"  Greek: {d['greek']}")
                    print(f"  Transliteration: {translit}")
                print(f"  Definition: {meaning}")

    elif command == 'strongs':
        if len(sys.argv) < 3:
            print("Usage: python logos.py strongs <H####/G####>")
            return
        sn = sys.argv[2].upper()
        from src.concordance import Concordance
        conc = Concordance()
        d = conc.get_strongs_definition(sn)
        if d:
            print(f"\n{sn}:")
            if 'hebrew' in d:
                print(f"  Hebrew: {d['hebrew']}")
            if 'greek' in d:
                print(f"  Greek: {d['greek']}")
            translit = d.get('transliteration', d.get('translit', ''))
            if translit:
                print(f"  Transliteration: {translit}")
            meaning = d.get('definition', d.get('def', ''))
            if meaning:
                print(f"  Definition: {meaning}")
            kjv = d.get('kjv', '')
            if kjv:
                print(f"  KJV usage: {kjv}")
            occur = d.get('occur', d.get('occurrences', ''))
            if occur:
                print(f"  Occurrences: {occur}")
        else:
            print(f"Strong's {sn} not found")

    elif command == 'hebrew':
        from src.concordance import Concordance
        conc = Concordance()
        hebrew = {k: v for k, v in conc.strongs_definitions.items() if k.startswith('H')}
        print(f"\n=== HEBREW WORDS ({len(hebrew)}) ===\n")
        for sn, d in hebrew.items():
            print(f"{sn}: {d['hebrew']} ({d['transliteration']})")
            print(f"      {d['definition']}\n")

    elif command == 'greek':
        from src.concordance import Concordance
        conc = Concordance()
        greek = {k: v for k, v in conc.strongs_definitions.items() if k.startswith('G')}
        print(f"\n=== GREEK WORDS ({len(greek)}) ===\n")
        for sn, d in greek.items():
            print(f"{sn}: {d['greek']} ({d['transliteration']})")
            print(f"      {d['definition']}\n")

    elif command == 'fetch':
        if len(sys.argv) < 3:
            print("Usage: python logos.py fetch <reference>")
            print("Example: python logos.py fetch 'Tobit 4:5'")
            return
        ref = ' '.join(sys.argv[2:])
        from src.api import fetch_verse
        result = fetch_verse(ref)
        if result and result['verses']:
            print(f"\n{result['reference']}:\n")
            for v in result['verses']:
                print(f"  {v['number']}: {v['text']}")
            print()
        else:
            print(f"Could not fetch: {ref}")

    elif command == 'apocrypha':
        if len(sys.argv) < 3:
            print("Usage: python logos.py apocrypha <book>")
            print("Books: Tobit, Judith, Wisdom, Sirach, Baruch, 1 Maccabees, 2 Maccabees, etc.")
            return
        book = ' '.join(sys.argv[2:])
        from src.api import fetch_apocrypha_book
        fetch_apocrypha_book(book)

    elif command == 'merge':
        from src.api import add_apocrypha_to_kjv
        add_apocrypha_to_kjv()

    elif command == 'semantic':
        from src.semantic import semantic_repl
        semantic_repl()

    elif command == 'similar':
        if len(sys.argv) < 3:
            print("Usage: python logos.py similar <reference>")
            return
        ref = ' '.join(sys.argv[2:])
        from src.semantic import SemanticSearch
        sem = SemanticSearch()
        results = sem.similar_verses(ref, n=10)
        print(f"\n=== VERSES SIMILAR TO: {ref} ===\n")
        print(f"{sem.kjv.get(ref, 'Reference not found')}\n")
        print("Semantically similar:")
        for r, score in results:
            print(f"  {score:.3f} | {r}")
            print(f"          {sem.kjv[r][:70]}...")

    elif command == 'meaning':
        if len(sys.argv) < 3:
            print("Usage: python logos.py meaning <query>")
            return
        query = ' '.join(sys.argv[2:])
        from src.semantic import SemanticSearch
        sem = SemanticSearch()
        results = sem.search_meaning(query, n=10)
        print(f"\n=== VERSES BY MEANING: {query} ===\n")
        for r, text, score in results:
            print(f"  {score:.3f} | {r}")
            print(f"          {text[:70]}...")

    elif command == 'concept':
        if len(sys.argv) < 3:
            print("Usage: python logos.py concept <concept_name>")
            print("Concepts: salvation, redemption, grace, mercy, faith, love, sin,")
            print("          righteousness, covenant, eternal, kingdom, messiah, etc.")
            return
        concept = ' '.join(sys.argv[2:])
        from src.semantic import SemanticSearch
        sem = SemanticSearch()
        results = sem.search_concept(concept, n=15)
        print(f"\n=== VERSES ABOUT: {concept.upper()} ===\n")
        for r, text, score in results:
            print(f"  {r}")
            print(f"    {text[:80]}...")

    elif command == 'verify':
        from src.integrity import verify_all
        verify_all()

    elif command == 'integrity':
        from src.integrity import repl as integrity_repl
        integrity_repl()

    elif command == 'diagnose':
        if len(sys.argv) < 3:
            print("Usage: python logos.py diagnose <filepath>")
            print("Example: python logos.py diagnose data/kjv.json")
            return
        filepath = sys.argv[2]
        from src.integrity import diagnose
        diagnose(filepath)

    elif command == 'graph':
        if len(sys.argv) < 3:
            from src.visualize import graph_repl
            graph_repl()
        else:
            ref = sys.argv[2]
            # Check if depth provided
            depth = 1
            if len(sys.argv) > 3:
                try:
                    depth = int(sys.argv[3])
                except ValueError:
                    # Not a number, might be part of reference
                    ref = ' '.join(sys.argv[2:])
            from src.visualize import generate_graph
            generate_graph(ref, depth=depth)

    elif command == 'banner':
        if len(sys.argv) < 3:
            text = "LOGOS"
        else:
            text = ' '.join(sys.argv[2:])
        from src.visualize import show_banner
        show_banner(text)

    elif command == 'image':
        if len(sys.argv) < 3:
            print("Usage: python logos.py image <reference> [theme]")
            print("Themes: light, dark, parchment, royal")
            return
        ref = sys.argv[2]
        theme = sys.argv[3] if len(sys.argv) > 3 else 'parchment'
        from src.image import generate_verse_image
        generate_verse_image(ref, theme)

    elif command == 'fzf':
        prefilter = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else None
        from src.fuzzy import pick_verse
        pick_verse(prefilter)

    elif command == 'pick':
        prefilter = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else None
        from src.fuzzy import pick_verse
        pick_verse(prefilter)

    elif command == 'chain':
        if len(sys.argv) < 4:
            print("Usage: python logos.py chain <start_ref> <end_ref>")
            print("Example: python logos.py chain 'Genesis 1:1' 'John 1:1'")
            return
        start = sys.argv[2]
        end = sys.argv[3]
        from src.chain import find_chain
        find_chain(start, end)

    elif command == 'bridge':
        if len(sys.argv) < 4:
            print("Usage: python logos.py bridge <ref1> <ref2>")
            return
        ref1 = sys.argv[2]
        ref2 = sys.argv[3]
        from src.chain import find_bridge
        find_bridge(ref1, ref2)

    elif command == 'genesis-revelation':
        from src.chain import protoevangelium_to_consummation
        protoevangelium_to_consummation()

    elif command == 'speak':
        if len(sys.argv) < 3:
            print("Usage: python logos.py speak <reference> [slow|normal|fast]")
            return
        ref = sys.argv[2]
        speed = sys.argv[3] if len(sys.argv) > 3 else 'normal'
        from src.voice import speak_verse
        speak_verse(ref, speed)

    elif command == 'audio':
        if len(sys.argv) < 3:
            print("Usage: python logos.py audio <reference>")
            return
        ref = sys.argv[2]
        from src.voice import save_audio
        save_audio(ref)

    elif command == 'qr':
        if len(sys.argv) < 3:
            print("Usage: python logos.py qr <reference> [text|link|ref]")
            return
        ref = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else 'text'
        from src.qr import generate_qr
        generate_qr(ref, mode)

    elif command == 'qrterm':
        if len(sys.argv) < 3:
            print("Usage: python logos.py qrterm <reference>")
            return
        ref = sys.argv[2]
        from src.qr import terminal_qr
        terminal_qr(ref)

    elif command == 'doc':
        if len(sys.argv) < 3:
            print("Usage: python logos.py doc <reference or chapter>")
            return
        ref = ' '.join(sys.argv[2:])
        from src.pdf import save_verse_pdf
        save_verse_pdf(ref)

    elif command == 'topic':
        if len(sys.argv) < 3:
            print("Usage: python logos.py topic <keyword>")
            return
        topic = ' '.join(sys.argv[2:])
        from src.pdf import save_topic_collection
        save_topic_collection(topic)

    elif command == 'daily':
        date_str = sys.argv[2] if len(sys.argv) > 2 else None
        from src.daily import show_daily_verse
        show_daily_verse(date_str)

    elif command == 'week':
        from src.daily import show_weekly
        show_weekly()

    elif command == 'help':
        print(__doc__)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
