#!/usr/bin/env python3
"""
LOGOS ENGINE - Semantic Search
Meaning-based verse discovery using Strong's numbers and concept mapping
"""

import json
import re
import math
from pathlib import Path
from collections import defaultdict, Counter

DATA_DIR = Path(__file__).parent.parent / "data"


class SemanticSearch:
    """
    Semantic search using:
    1. Strong's number mapping (shared Hebrew/Greek roots)
    2. Theological concept categories
    3. TF-IDF weighted similarity
    """

    def __init__(self):
        self.kjv = {}
        self.strongs = {}
        self.word_to_strongs = {}
        self.concept_map = {}
        self.verse_concepts = {}
        self.verse_vectors = {}
        self.idf = {}

        self._load_data()
        self._build_indices()

    def _load_data(self):
        """Load KJV and Strong's data"""
        kjv_path = DATA_DIR / "kjv.json"
        strongs_path = DATA_DIR / "strongs.json"

        with open(kjv_path, 'r') as f:
            self.kjv = json.load(f)

        if strongs_path.exists():
            with open(strongs_path, 'r') as f:
                self.strongs = json.load(f)

        print(f"Loaded {len(self.kjv)} verses, {len(self.strongs)} Strong's entries")

    def _build_indices(self):
        """Build semantic indices"""
        print("Building semantic indices...")

        # Map English words to Strong's numbers
        self._build_word_strongs_map()

        # Build concept categories
        self._build_concept_map()

        # Build verse concept vectors
        self._build_verse_vectors()

        print(f"  Word->Strong's mappings: {len(self.word_to_strongs)}")
        print(f"  Concept categories: {len(self.concept_map)}")
        print(f"  Verse vectors built: {len(self.verse_vectors)}")

    def _build_word_strongs_map(self):
        """Map key English words to their Strong's numbers"""
        # Direct mapping of important theological terms
        self.word_to_strongs = {
            # Divine terms
            'god': {'H430', 'H410', 'G2316'},
            'lord': {'H3068', 'H136', 'G2962'},
            'almighty': {'H7706', 'G3841'},
            'holy': {'H6918', 'G40'},
            'spirit': {'H7307', 'G4151'},

            # Salvation terms
            'save': {'H3467', 'G4982'},
            'saved': {'H3467', 'G4982'},
            'salvation': {'H3444', 'G4991'},
            'saviour': {'H3467', 'G4990'},
            'savior': {'H3467', 'G4990'},
            'redeem': {'H1350', 'H6299', 'G3084'},
            'redeemed': {'H1350', 'G3084'},
            'redemption': {'H1353', 'G629'},

            # Grace/Mercy
            'grace': {'H2580', 'G5485'},
            'mercy': {'H2617', 'G1656'},
            'merciful': {'H2617', 'G1656'},
            'compassion': {'H7355', 'G4697'},
            'forgive': {'H5545', 'G863'},
            'forgiveness': {'H5547', 'G859'},

            # Faith/Believe
            'faith': {'H530', 'G4102'},
            'believe': {'H539', 'G4100'},
            'believed': {'H539', 'G4100'},
            'believeth': {'H539', 'G4100'},
            'trust': {'H982', 'G4100'},

            # Love
            'love': {'H157', 'H160', 'G26', 'G25'},
            'loved': {'H157', 'G25'},
            'loveth': {'H157', 'G25'},
            'lovingkindness': {'H2617'},

            # Sin
            'sin': {'H2398', 'H2403', 'G266'},
            'sins': {'H2398', 'G266'},
            'sinned': {'H2398', 'G264'},
            'sinner': {'H2400', 'G268'},
            'iniquity': {'H5771', 'G458'},
            'transgression': {'H6588', 'G3900'},
            'evil': {'H7451', 'G4190'},

            # Righteousness
            'righteous': {'H6662', 'G1342'},
            'righteousness': {'H6664', 'G1343'},
            'just': {'H6662', 'G1342'},
            'justice': {'H4941', 'G1343'},

            # Covenant
            'covenant': {'H1285', 'G1242'},
            'promise': {'H1697', 'G1860'},
            'oath': {'H7621', 'G3727'},

            # Life/Death
            'life': {'H2416', 'G2222'},
            'live': {'H2421', 'G2198'},
            'death': {'H4194', 'G2288'},
            'die': {'H4191', 'G599'},
            'eternal': {'H5769', 'G166'},
            'everlasting': {'H5769', 'G166'},
            'resurrection': {'G386', 'G1453'},

            # Blood/Sacrifice
            'blood': {'H1818', 'G129'},
            'sacrifice': {'H2077', 'G2378'},
            'offering': {'H5930', 'H7133', 'G4376'},
            'atonement': {'H3722', 'G2434'},
            'lamb': {'H3532', 'G286', 'G721'},

            # Kingdom
            'kingdom': {'H4438', 'G932'},
            'king': {'H4428', 'G935'},
            'throne': {'H3678', 'G2362'},
            'reign': {'H4427', 'G936'},

            # Messiah
            'messiah': {'H4899', 'G5547'},
            'christ': {'G5547'},
            'anointed': {'H4886', 'G5547'},
            'son': {'H1121', 'G5207'},

            # Law/Word
            'law': {'H8451', 'G3551'},
            'commandment': {'H4687', 'G1785'},
            'word': {'H1697', 'G3056'},
            'truth': {'H571', 'G225'},

            # Worship
            'worship': {'H7812', 'G4352'},
            'prayer': {'H8605', 'G4335'},
            'praise': {'H8416', 'G136'},

            # People/Place
            'israel': {'H3478', 'G2474'},
            'jerusalem': {'H3389', 'G2419'},
            'church': {'G1577'},

            # Heaven/Earth
            'heaven': {'H8064', 'G3772'},
            'earth': {'H776', 'G1093'},
            'light': {'H216', 'G5457'},
            'darkness': {'H2822', 'G4655'},

            # Heart/Soul
            'heart': {'H3820', 'G2588'},
            'soul': {'H5315', 'G5590'},

            # Wisdom
            'wisdom': {'H2451', 'G4678'},
            'knowledge': {'H1847', 'G1108'},

            # Judgment
            'judgment': {'H4941', 'G2920'},
            'judge': {'H8199', 'G2919'},
            'wrath': {'H639', 'G3709'},

            # Additional verb forms
            'saves': {'H3467', 'G4982'},
            'saving': {'H3467', 'G4982'},
            'sinners': {'H2400', 'G268'},
            'perish': {'H6', 'G622'},
            'lives': {'H2416', 'G2198'},
            'living': {'H2416', 'G2198'},
            'dying': {'H4191', 'G599'},
            'begotten': {'G3439', 'G1080'},
            'world': {'H8398', 'G2889'},
            'gave': {'H5414', 'G1325'},
            'give': {'H5414', 'G1325'},
            'given': {'H5414', 'G1325'},
            'blessed': {'H1288', 'G2127'},
            'blessing': {'H1293', 'G2129'},
            'glory': {'H3519', 'G1391'},
            'glorify': {'H3513', 'G1392'},

            # Persecution/Tribulation/Endurance
            'endure': {'G5281', 'G5278', 'H3201'},
            'endurance': {'G5281', 'H3201'},
            'endureth': {'G5281', 'G5278'},
            'patient': {'G5281', 'G3114'},
            'patience': {'G5281', 'G3115', 'H3201'},
            'persecute': {'G1377', 'H7291'},
            'persecuted': {'G1377', 'G1559', 'H7291'},
            'persecution': {'G1375', 'G1377'},
            'persecutions': {'G1375', 'G1377'},
            'tribulation': {'G2347', 'H6869', 'H6862'},
            'tribulations': {'G2347', 'H6869'},
            'affliction': {'G2347', 'H6040', 'H6869'},
            'afflictions': {'G2347', 'H6040'},
            'suffer': {'G3958', 'G2553', 'H5375'},
            'suffered': {'G3958', 'H5375'},
            'suffering': {'G3958', 'G3804'},
            'sufferings': {'G3804', 'G3958'},
            'overcome': {'G3528', 'H3898', 'H1396'},
            'overcometh': {'G3528'},
            'overcame': {'G3528', 'H3898'},
            'conquer': {'G3528', 'H3898'},
            'victory': {'G3529', 'H5331', 'H8668'},
            'trial': {'G3986', 'H4531'},
            'trials': {'G3986'},
            'temptation': {'G3986', 'H4531'},
            'temptations': {'G3986'},
            'test': {'G3986', 'G1381', 'H974'},
            'tested': {'G3986', 'H974'},
            'saints': {'H6918', 'G40'},
            'martyr': {'G3144'},
            'witness': {'G3144', 'H5707'},
            'witnesses': {'G3144', 'H5707'},
            'testimony': {'G3141', 'H5715'},
        }

    def _build_concept_map(self):
        """Map Strong's numbers to theological concept categories"""
        self.concept_map = {
            # DIVINE NATURE
            'divinity': {'H430', 'H410', 'H433', 'H3068', 'H136', 'H5945', 'H7706',
                        'G2316', 'G2962', 'G5547', 'G2424'},
            'trinity': {'H430', 'H7307', 'G2316', 'G4151', 'G5207', 'G3962'},
            'holiness': {'H6918', 'H6944', 'H6942', 'G40', 'G37', 'G38'},
            'glory': {'H3519', 'H3513', 'G1391', 'G1392'},
            'power': {'H3581', 'H1369', 'H5797', 'G1411', 'G1849', 'G2904'},
            'eternal': {'H5769', 'G166', 'G165'},

            # SALVATION
            'salvation': {'H3467', 'H3444', 'H6299', 'H1350', 'G4991', 'G4982', 'G4990'},
            'redemption': {'H1350', 'H6299', 'H3722', 'G629', 'G3084', 'G59'},
            'atonement': {'H3722', 'H3725', 'G2434', 'G2435'},
            'forgiveness': {'H5545', 'H5547', 'G863', 'G859'},
            'grace': {'H2580', 'H2603', 'G5485', 'G5463'},
            'mercy': {'H2617', 'H7355', 'G1656', 'G3628'},

            # SIN
            'sin': {'H2398', 'H2399', 'H2403', 'H5771', 'H6588', 'G266', 'G264', 'G268'},
            'evil': {'H7451', 'H7563', 'H7562', 'G4190', 'G2556'},
            'transgression': {'H6588', 'H5674', 'G3900', 'G458'},

            # RIGHTEOUSNESS
            'righteousness': {'H6662', 'H6663', 'H6664', 'H6666', 'G1342', 'G1343', 'G1344'},
            'justice': {'H4941', 'H6664', 'G2917', 'G2920', 'G2919'},
            'truth': {'H571', 'H530', 'G225', 'G227'},

            # FAITH
            'faith': {'H539', 'H530', 'H982', 'G4102', 'G4100', 'G4103'},
            'believe': {'H539', 'G4100', 'G4102'},
            'trust': {'H982', 'H539', 'G4100', 'G3982'},
            'hope': {'H3176', 'H8615', 'G1680', 'G1679'},

            # LOVE
            'love': {'H157', 'H160', 'H2617', 'G26', 'G25', 'G5368'},
            'compassion': {'H7355', 'H7356', 'G3628', 'G4697'},

            # COVENANT
            'covenant': {'H1285', 'G1242'},
            'promise': {'H1696', 'G1860', 'G1861'},
            'oath': {'H7621', 'H7650', 'G3727', 'G3726'},

            # LAW/WORD
            'law': {'H8451', 'H4687', 'H2706', 'G3551', 'G1785'},
            'commandment': {'H4687', 'H6680', 'G1785', 'G1781'},
            'word': {'H1697', 'H561', 'G3056', 'G4487'},
            'testimony': {'H5715', 'H5749', 'G3141', 'G3140'},

            # WORSHIP
            'worship': {'H7812', 'H5647', 'G4352', 'G3000'},
            'prayer': {'H6419', 'H8605', 'G4336', 'G4335'},
            'praise': {'H1984', 'H8416', 'G134', 'G136'},
            'sacrifice': {'H2076', 'H2077', 'H5930', 'G2378', 'G4376'},

            # SPIRIT
            'spirit': {'H7307', 'H5315', 'G4151', 'G5590'},
            'soul': {'H5315', 'G5590'},
            'heart': {'H3820', 'H3824', 'G2588'},
            'mind': {'H3820', 'G3563', 'G5590'},

            # LIFE/DEATH
            'life': {'H2416', 'H2421', 'G2222', 'G2198'},
            'death': {'H4191', 'H4194', 'G2288', 'G599'},
            'resurrection': {'G386', 'G450', 'G1453'},
            'blood': {'H1818', 'G129'},

            # KINGDOM
            'kingdom': {'H4427', 'H4428', 'H4438', 'G932', 'G935', 'G936'},
            'king': {'H4428', 'G935'},
            'throne': {'H3678', 'G2362'},
            'reign': {'H4427', 'H4910', 'G936', 'G757'},

            # PEOPLE
            'israel': {'H3478', 'G2474'},
            'nation': {'H1471', 'H5971', 'G1484'},
            'church': {'G1577'},
            'people': {'H5971', 'H1471', 'G2992', 'G1484'},

            # MESSIAH
            'messiah': {'H4899', 'G5547'},
            'christ': {'G5547'},
            'savior': {'H3467', 'G4990'},
            'lord': {'H113', 'H136', 'H3068', 'G2962'},
            'servant': {'H5650', 'H5647', 'G1401', 'G1249'},
            'shepherd': {'H7462', 'G4166'},
            'lamb': {'H3532', 'H7716', 'G286', 'G721'},

            # JUDGMENT
            'judgment': {'H4941', 'H8199', 'G2917', 'G2920', 'G2919'},
            'wrath': {'H639', 'H2534', 'G3709', 'G2372'},
            'punishment': {'H6066', 'H5771', 'G2851', 'G5098'},

            # CREATION
            'creation': {'H1254', 'H3335', 'H6213', 'G2936', 'G2937'},
            'heaven': {'H8064', 'G3772'},
            'earth': {'H776', 'G1093'},
            'light': {'H216', 'G5457'},
            'darkness': {'H2822', 'G4655', 'G4653'},

            # BLESSING
            'blessing': {'H1288', 'H1293', 'G2127', 'G2129'},
            'curse': {'H779', 'H7045', 'G2671', 'G2672'},

            # PROPHECY
            'prophecy': {'H5030', 'H5012', 'G4394', 'G4395', 'G4396'},
            'vision': {'H2377', 'H4759', 'G3705', 'G3701'},

            # WISDOM
            'wisdom': {'H2451', 'H2449', 'H998', 'G4678', 'G4680'},
            'knowledge': {'H1847', 'H3045', 'G1108', 'G1097'},
            'understanding': {'H998', 'H8394', 'G4907', 'G3563'},

            # TIME
            'day': {'H3117', 'G2250'},
            'end_times': {'H319', 'H7093', 'G2078', 'G5056'},
            'forever': {'H5769', 'H5703', 'G166', 'G165'},

            # PERSECUTION/TRIBULATION (for the days ahead)
            'persecution': {'G1375', 'G1377', 'G1559', 'H7291', 'H7852'},
            'tribulation': {'G2347', 'H6869', 'H6862', 'H6887'},
            'affliction': {'G2347', 'H6040', 'H6869', 'H6887'},
            'suffering': {'G3958', 'G3804', 'G2553', 'H5375'},
            'endurance': {'G5281', 'G5278', 'G3114', 'G3115'},
            'patience': {'G5281', 'G3114', 'G3115', 'H3201'},
            'overcome': {'G3528', 'H3898', 'H1396', 'H5329'},
            'victory': {'G3528', 'G3529', 'H5331', 'H8668'},
            'trial': {'G3986', 'G1381', 'H974', 'H4531'},
            'temptation': {'G3986', 'H4531', 'H5254'},
            'martyrdom': {'G3144', 'G3141', 'H5707'},
        }

        # Reverse map: Strong's -> concepts
        self.strongs_to_concepts = defaultdict(set)
        for concept, strongs_set in self.concept_map.items():
            for s in strongs_set:
                self.strongs_to_concepts[s].add(concept)

    def _build_verse_vectors(self):
        """Build concept vectors for each verse"""
        # Document frequency for IDF
        doc_freq = Counter()

        # First pass: count document frequencies
        for ref, text in self.kjv.items():
            words = set(re.findall(r'\b[a-z]{3,}\b', text.lower()))
            concepts = set()

            for word in words:
                if word in self.word_to_strongs:
                    for strongs_id in self.word_to_strongs[word]:
                        if strongs_id in self.strongs_to_concepts:
                            concepts.update(self.strongs_to_concepts[strongs_id])

            for concept in concepts:
                doc_freq[concept] += 1

            self.verse_concepts[ref] = concepts

        # Calculate IDF
        num_docs = len(self.kjv)
        for concept, freq in doc_freq.items():
            self.idf[concept] = math.log(num_docs / (1 + freq))

        # Build TF-IDF vectors
        for ref, concepts in self.verse_concepts.items():
            if concepts:
                vector = {}
                for concept in concepts:
                    tf = 1  # Binary presence
                    vector[concept] = tf * self.idf.get(concept, 1)
                self.verse_vectors[ref] = vector

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two concept vectors"""
        if not vec1 or not vec2:
            return 0

        # Find common concepts
        common = set(vec1.keys()) & set(vec2.keys())
        if not common:
            return 0

        # Calculate dot product
        dot = sum(vec1[c] * vec2[c] for c in common)

        # Calculate magnitudes
        mag1 = math.sqrt(sum(v*v for v in vec1.values()))
        mag2 = math.sqrt(sum(v*v for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot / (mag1 * mag2)

    def similar_verses(self, ref, n=10):
        """Find verses semantically similar to given reference"""
        if ref not in self.verse_vectors:
            # Try to find the verse
            for key in self.kjv:
                if ref.lower() in key.lower():
                    ref = key
                    break

        if ref not in self.verse_vectors:
            print(f"Reference not found: {ref}")
            return []

        query_vec = self.verse_vectors[ref]
        query_concepts = self.verse_concepts.get(ref, set())

        scores = []
        for other_ref, other_vec in self.verse_vectors.items():
            if other_ref != ref:
                sim = self._cosine_similarity(query_vec, other_vec)
                if sim > 0:
                    scores.append((other_ref, sim))

        # Sort by similarity
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:n]

    def search_concept(self, concept, n=20):
        """Find verses related to a theological concept"""
        concept = concept.lower()

        if concept not in self.concept_map:
            # Try to find partial match
            matches = [c for c in self.concept_map if concept in c]
            if matches:
                concept = matches[0]
            else:
                print(f"Concept not found: {concept}")
                print(f"Available: {', '.join(sorted(self.concept_map.keys()))}")
                return []

        target_strongs = self.concept_map[concept]

        results = []
        for ref, concepts in self.verse_concepts.items():
            if concept in concepts:
                # Score by how many Strong's numbers from this concept are present
                score = len(concepts & {concept})
                results.append((ref, self.kjv[ref], score))

        results.sort(key=lambda x: x[2], reverse=True)
        return results[:n]

    def search_meaning(self, query, n=20):
        """Search by meaning - find verses matching the semantic intent"""
        query_words = re.findall(r'\b[a-z]{3,}\b', query.lower())

        # Build query vector from concepts
        query_concepts = set()
        for word in query_words:
            # Check if word is a concept
            if word in self.concept_map:
                query_concepts.add(word)

            # Check word->Strong's->concept mapping
            if word in self.word_to_strongs:
                for strongs_id in self.word_to_strongs[word]:
                    if strongs_id in self.strongs_to_concepts:
                        query_concepts.update(self.strongs_to_concepts[strongs_id])

        if not query_concepts:
            print(f"No semantic concepts found for: {query}")
            return []

        print(f"Searching concepts: {query_concepts}")

        # Build query vector
        query_vec = {c: self.idf.get(c, 1) for c in query_concepts}

        # Find similar verses
        scores = []
        for ref, vec in self.verse_vectors.items():
            sim = self._cosine_similarity(query_vec, vec)
            if sim > 0:
                scores.append((ref, self.kjv[ref], sim))

        scores.sort(key=lambda x: x[2], reverse=True)
        return scores[:n]

    def explain_connection(self, ref1, ref2):
        """Explain why two verses are semantically connected"""
        concepts1 = self.verse_concepts.get(ref1, set())
        concepts2 = self.verse_concepts.get(ref2, set())

        shared = concepts1 & concepts2

        if not shared:
            return None

        return {
            'ref1': ref1,
            'ref2': ref2,
            'shared_concepts': list(shared),
            'similarity': self._cosine_similarity(
                self.verse_vectors.get(ref1, {}),
                self.verse_vectors.get(ref2, {})
            )
        }


def semantic_repl():
    """Interactive semantic search REPL"""
    sem = SemanticSearch()

    print("\n=== LOGOS SEMANTIC SEARCH ===")
    print("Commands:")
    print("  similar <ref>       - Find semantically similar verses")
    print("  concept <name>      - Search by theological concept")
    print("  meaning <query>     - Search by meaning")
    print("  explain <ref1> <ref2> - Explain connection")
    print("  concepts            - List all concepts")
    print("  quit                - Exit")
    print()

    while True:
        try:
            cmd = input("SEMANTIC> ").strip()
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

        elif command == 'similar':
            results = sem.similar_verses(arg)
            print(f"\nVerses similar to {arg}:\n")
            for ref, score in results[:10]:
                print(f"  {score:.3f} | {ref}")
                print(f"         {sem.kjv[ref][:70]}...")
            print()

        elif command == 'concept':
            results = sem.search_concept(arg)
            print(f"\nVerses about '{arg}':\n")
            for ref, text, score in results[:10]:
                print(f"  {ref}")
                print(f"    {text[:80]}...")
            print()

        elif command == 'meaning':
            results = sem.search_meaning(arg)
            print(f"\nVerses matching meaning '{arg}':\n")
            for ref, text, score in results[:10]:
                print(f"  {score:.3f} | {ref}")
                print(f"         {text[:70]}...")
            print()

        elif command == 'explain':
            refs = arg.split()
            if len(refs) >= 2:
                result = sem.explain_connection(refs[0], ' '.join(refs[1:]))
                if result:
                    print(f"\nConnection between {result['ref1']} and {result['ref2']}:")
                    print(f"  Shared concepts: {', '.join(result['shared_concepts'])}")
                    print(f"  Similarity: {result['similarity']:.3f}")
                else:
                    print("No semantic connection found")
            else:
                print("Usage: explain <ref1> <ref2>")

        elif command == 'concepts':
            print("\nTheological concepts:")
            for c in sorted(sem.concept_map.keys()):
                print(f"  {c}")
            print()

        elif command == 'help':
            print("\nCommands:")
            print("  similar <ref>       - Find semantically similar verses")
            print("  concept <name>      - Search by theological concept")
            print("  meaning <query>     - Search by meaning")
            print("  explain <ref1> <ref2> - Explain connection")
            print("  concepts            - List all concepts")
            print()

        else:
            # Default: treat as meaning search
            results = sem.search_meaning(cmd)
            if results:
                print(f"\nVerses matching '{cmd}':\n")
                for ref, text, score in results[:10]:
                    print(f"  {score:.3f} | {ref}")
                    print(f"         {text[:70]}...")
            print()


if __name__ == "__main__":
    semantic_repl()
