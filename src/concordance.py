"""
LOGOS ENGINE - Concordance System
Hebrew/Greek integration via Strong's Numbers

Strong's Concordance:
- H#### = Hebrew (Old Testament)
- G#### = Greek (New Testament)
"""

import json
import re
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"


class Concordance:
    """
    Build concordance mapping:
    - English word -> [verse refs]
    - English word -> Strong's number -> Hebrew/Greek root
    - Strong's number -> [verse refs]
    """

    def __init__(self):
        self.word_index = defaultdict(list)      # word -> [(ref, position)]
        self.strongs_index = defaultdict(list)   # H/G#### -> [(ref, word)]
        self.verse_words = {}                     # ref -> [words]
        self.strongs_definitions = {}             # H/G#### -> {hebrew/greek, transliteration, definition}

        self._load_kjv()
        self._load_strongs()

    def _load_kjv(self):
        """Load KJV and build word index"""
        kjv_path = DATA_DIR / "kjv.json"

        if not kjv_path.exists():
            print("KJV not found. Run: python logos.py init")
            return

        with open(kjv_path, 'r') as f:
            kjv = json.load(f)

        print(f"Building word index from {len(kjv)} verses...")

        for ref, text in kjv.items():
            # Clean and tokenize
            words = self._tokenize(text)
            self.verse_words[ref] = words

            for pos, word in enumerate(words):
                word_lower = word.lower()
                self.word_index[word_lower].append((ref, pos))

        print(f"Indexed {len(self.word_index)} unique words")

    def _tokenize(self, text):
        """Tokenize verse text"""
        # Remove punctuation but keep word structure
        text = re.sub(r'[^\w\s\-]', '', text)
        return text.split()

    def _load_strongs(self):
        """Load Strong's definitions if available"""
        strongs_path = DATA_DIR / "strongs.json"

        if strongs_path.exists():
            with open(strongs_path, 'r') as f:
                self.strongs_definitions = json.load(f)
            print(f"Loaded {len(self.strongs_definitions)} Strong's definitions")
        else:
            print("Strong's definitions not found. Creating structure...")
            self._create_strongs_structure()

    def _create_strongs_structure(self):
        """Create Strong's structure for manual population"""
        # Core theological words with Strong's numbers
        core_strongs = {
            # Hebrew (OT)
            "H430": {
                "hebrew": "אֱלֹהִים",
                "transliteration": "elohim",
                "definition": "God, gods, mighty ones",
                "occurrences": 2606
            },
            "H3068": {
                "hebrew": "יְהוָה",
                "transliteration": "YHWH/Yahweh",
                "definition": "The LORD, the self-existent One",
                "occurrences": 6519
            },
            "H1697": {
                "hebrew": "דָּבָר",
                "transliteration": "dabar",
                "definition": "word, speech, matter, thing",
                "occurrences": 1441
            },
            "H7307": {
                "hebrew": "רוּחַ",
                "transliteration": "ruach",
                "definition": "spirit, wind, breath",
                "occurrences": 378
            },
            "H571": {
                "hebrew": "אֶמֶת",
                "transliteration": "emeth",
                "definition": "truth, faithfulness, stability",
                "occurrences": 127
            },
            "H2617": {
                "hebrew": "חֶסֶד",
                "transliteration": "chesed",
                "definition": "lovingkindness, mercy, steadfast love",
                "occurrences": 248
            },
            "H6663": {
                "hebrew": "צָדַק",
                "transliteration": "tsadaq",
                "definition": "to be righteous, justified",
                "occurrences": 41
            },
            "H539": {
                "hebrew": "אָמַן",
                "transliteration": "aman",
                "definition": "to believe, be faithful, trust",
                "occurrences": 108
            },
            "H8085": {
                "hebrew": "שָׁמַע",
                "transliteration": "shama",
                "definition": "to hear, listen, obey (Shema)",
                "occurrences": 1159
            },

            # Greek (NT)
            "G3056": {
                "greek": "λόγος",
                "transliteration": "logos",
                "definition": "word, reason, the Word (Christ)",
                "occurrences": 330
            },
            "G2316": {
                "greek": "θεός",
                "transliteration": "theos",
                "definition": "God",
                "occurrences": 1343
            },
            "G4151": {
                "greek": "πνεῦμα",
                "transliteration": "pneuma",
                "definition": "spirit, breath, wind",
                "occurrences": 385
            },
            "G26": {
                "greek": "ἀγάπη",
                "transliteration": "agape",
                "definition": "love (divine, unconditional)",
                "occurrences": 116
            },
            "G4102": {
                "greek": "πίστις",
                "transliteration": "pistis",
                "definition": "faith, belief, trust",
                "occurrences": 244
            },
            "G225": {
                "greek": "ἀλήθεια",
                "transliteration": "aletheia",
                "definition": "truth",
                "occurrences": 110
            },
            "G5485": {
                "greek": "χάρις",
                "transliteration": "charis",
                "definition": "grace, favor, kindness",
                "occurrences": 156
            },
            "G1343": {
                "greek": "δικαιοσύνη",
                "transliteration": "dikaiosyne",
                "definition": "righteousness, justice",
                "occurrences": 92
            },
            "G4991": {
                "greek": "σωτηρία",
                "transliteration": "soteria",
                "definition": "salvation, deliverance",
                "occurrences": 46
            },
            "G3341": {
                "greek": "μετάνοια",
                "transliteration": "metanoia",
                "definition": "repentance, change of mind",
                "occurrences": 24
            }
        }

        strongs_path = DATA_DIR / "strongs.json"
        with open(strongs_path, 'w') as f:
            json.dump(core_strongs, f, indent=2, ensure_ascii=False)

        self.strongs_definitions = core_strongs
        print(f"Created Strong's structure with {len(core_strongs)} core definitions")

    def search_word(self, word, limit=20):
        """Find all occurrences of an English word"""
        word_lower = word.lower()
        occurrences = self.word_index.get(word_lower, [])
        return occurrences[:limit]

    def search_strongs(self, strongs_num):
        """Find all verses containing a Strong's number (requires tagged text)"""
        return self.strongs_index.get(strongs_num, [])

    def get_strongs_definition(self, strongs_num):
        """Get Hebrew/Greek definition for Strong's number"""
        return self.strongs_definitions.get(strongs_num)

    def word_study(self, word):
        """Complete word study: English -> occurrences + Strong's info"""
        results = {
            'word': word,
            'occurrences': [],
            'strongs': [],
            'related_hebrew': [],
            'related_greek': []
        }

        # Get occurrences
        occurrences = self.search_word(word)
        results['occurrences'] = occurrences[:10]
        results['total_occurrences'] = len(self.word_index.get(word.lower(), []))

        # Map to Strong's (basic mapping for common words)
        word_to_strongs = {
            'god': ['H430', 'G2316'],
            'lord': ['H3068', 'H136', 'G2962'],
            'word': ['H1697', 'G3056'],
            'spirit': ['H7307', 'G4151'],
            'love': ['H157', 'H160', 'G26', 'G5368'],
            'faith': ['H530', 'G4102'],
            'truth': ['H571', 'G225'],
            'grace': ['H2580', 'G5485'],
            'righteous': ['H6662', 'G1342'],
            'salvation': ['H3444', 'G4991'],
            'repent': ['H5162', 'G3340']
        }

        strongs_nums = word_to_strongs.get(word.lower(), [])
        for sn in strongs_nums:
            definition = self.get_strongs_definition(sn)
            if definition:
                results['strongs'].append({
                    'number': sn,
                    'definition': definition
                })
                if sn.startswith('H'):
                    results['related_hebrew'].append(definition)
                else:
                    results['related_greek'].append(definition)

        return results

    def three_witness_hebrew(self, strongs_num):
        """
        Three-witness pattern using Hebrew/Greek root
        Find 3 verses using the same original language word
        """
        definition = self.get_strongs_definition(strongs_num)
        if not definition:
            return None

        # For now, return the definition with placeholder for verses
        # Full implementation requires Strong's-tagged KJV text
        return {
            'strongs': strongs_num,
            'definition': definition,
            'note': 'Full verse mapping requires Strongs-tagged KJV (next phase)'
        }


def build_concordance():
    """Build and save concordance"""
    print("=== BUILDING CONCORDANCE ===\n")
    conc = Concordance()

    # Save word index
    index_path = DATA_DIR / "word_index.json"
    # Convert tuples to lists for JSON serialization
    word_index_serializable = {k: v for k, v in conc.word_index.items()}
    with open(index_path, 'w') as f:
        json.dump(word_index_serializable, f)
    print(f"Saved word index to {index_path}")

    return conc


def repl():
    """Interactive concordance REPL"""
    conc = Concordance()

    print("\n=== LOGOS CONCORDANCE ===")
    print("Commands: word, strongs, study, hebrew, greek, quit")
    print("Example: word love")
    print("Example: strongs H430")
    print("Example: study faith")
    print()

    while True:
        try:
            cmd = input("CONCORDANCE> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShalom.")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command in ('quit', 'exit'):
            print("Shalom.")
            break

        elif command == 'word':
            results = conc.search_word(arg)
            print(f"\n'{arg}' appears {len(results)} times (showing first 10):\n")
            for ref, pos in results[:10]:
                print(f"  {ref}")
            print()

        elif command == 'strongs':
            definition = conc.get_strongs_definition(arg.upper())
            if definition:
                print(f"\n{arg.upper()}:")
                for key, val in definition.items():
                    print(f"  {key}: {val}")
                print()
            else:
                print(f"Strong's {arg} not found")

        elif command == 'study':
            results = conc.word_study(arg)
            print(f"\n=== WORD STUDY: {arg.upper()} ===\n")
            print(f"Total occurrences: {results['total_occurrences']}")
            print(f"\nSample verses:")
            for ref, pos in results['occurrences'][:5]:
                print(f"  {ref}")

            if results['strongs']:
                print(f"\nStrong's connections:")
                for s in results['strongs']:
                    print(f"\n  {s['number']}:")
                    d = s['definition']
                    if 'hebrew' in d:
                        print(f"    Hebrew: {d['hebrew']} ({d['transliteration']})")
                    if 'greek' in d:
                        print(f"    Greek: {d['greek']} ({d['transliteration']})")
                    print(f"    Meaning: {d['definition']}")
            print()

        elif command == 'hebrew':
            # List all Hebrew Strong's
            hebrew = {k: v for k, v in conc.strongs_definitions.items() if k.startswith('H')}
            print(f"\n{len(hebrew)} Hebrew words loaded:\n")
            for sn, d in hebrew.items():
                print(f"  {sn}: {d['hebrew']} ({d['transliteration']}) - {d['definition'][:40]}...")
            print()

        elif command == 'greek':
            # List all Greek Strong's
            greek = {k: v for k, v in conc.strongs_definitions.items() if k.startswith('G')}
            print(f"\n{len(greek)} Greek words loaded:\n")
            for sn, d in greek.items():
                print(f"  {sn}: {d['greek']} ({d['transliteration']}) - {d['definition'][:40]}...")
            print()

        elif command == 'help':
            print("\nCommands:")
            print("  word <term>     - Find occurrences of English word")
            print("  strongs <H/G#>  - Get Strong's definition")
            print("  study <term>    - Full word study with Hebrew/Greek")
            print("  hebrew          - List all Hebrew definitions")
            print("  greek           - List all Greek definitions")
            print("  quit            - Exit")
            print()

        else:
            print(f"Unknown: {command}. Type 'help'")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        build_concordance()
    else:
        repl()
