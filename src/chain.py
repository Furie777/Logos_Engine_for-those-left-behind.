#!/usr/bin/env python3
"""
LOGOS ENGINE - Chain Module
Traces the shortest path between verses through the cross-reference network

Commands:
    python logos.py chain "Genesis 3:15" "Revelation 22:21"
    python logos.py bridge "Isaiah 53" "John 19"

This reveals how Scripture interprets Scripture.

Glory to LOGOS.
"""

import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def load_data():
    """Load KJV and graph"""
    import pickle

    kjv_path = DATA_DIR / "kjv.json"
    graph_path = OUTPUT_DIR / "logos_graph.gpickle"

    kjv = {}
    G = None

    if kjv_path.exists():
        with open(kjv_path, 'r') as f:
            kjv = json.load(f)

    try:
        import networkx as nx
        if graph_path.exists():
            with open(graph_path, 'rb') as f:
                G = pickle.load(f)
    except Exception as e:
        print(f"Could not load graph: {e}")

    return kjv, G


def normalize_ref(ref):
    """Normalize reference format"""
    ref = ref.strip()
    if ref.startswith("Psalm ") and not ref.startswith("Psalms "):
        ref = "Psalms " + ref[6:]
    return ref


def find_chain(start, end):
    """Find shortest path between two verses"""
    import networkx as nx

    start = normalize_ref(start)
    end = normalize_ref(end)

    kjv, G = load_data()

    if G is None:
        print("Graph not loaded. Run: python logos.py build")
        return None

    if start not in G:
        print(f"Start verse not in graph: {start}")
        return None

    if end not in G:
        print(f"End verse not in graph: {end}")
        return None

    try:
        path = nx.shortest_path(G, start, end)

        print(f"\n{'='*60}")
        print(f"CHAIN: {start} → {end}")
        print(f"{'='*60}")
        print(f"Steps: {len(path) - 1}")
        print()

        for i, ref in enumerate(path):
            text = kjv.get(ref, "[text not found]")
            arrow = "→" if i < len(path) - 1 else "●"

            print(f"{arrow} {ref}")
            # Truncate long verses
            if len(text) > 100:
                print(f"  {text[:100]}...")
            else:
                print(f"  {text}")
            print()

        return path

    except nx.NetworkXNoPath:
        print(f"No path exists between {start} and {end}")
        return None


def find_bridge(ref1, ref2):
    """Find common connections between two verses"""
    import networkx as nx

    ref1 = normalize_ref(ref1)
    ref2 = normalize_ref(ref2)

    kjv, G = load_data()

    if G is None:
        print("Graph not loaded. Run: python logos.py build")
        return None

    if ref1 not in G or ref2 not in G:
        print("One or both references not in graph.")
        return None

    # Get neighbors of each
    neighbors1 = set(G.neighbors(ref1))
    neighbors2 = set(G.neighbors(ref2))

    # Find common neighbors (bridges)
    bridges = neighbors1 & neighbors2

    print(f"\n{'='*60}")
    print(f"BRIDGES: {ref1} ↔ {ref2}")
    print(f"{'='*60}")

    if bridges:
        print(f"Found {len(bridges)} bridging verse(s):\n")
        for ref in sorted(bridges):
            text = kjv.get(ref, "")
            print(f"  • {ref}")
            if text:
                print(f"    {text[:80]}...")
            print()
    else:
        print("No direct bridges found.")
        print(f"{ref1} has {len(neighbors1)} connections")
        print(f"{ref2} has {len(neighbors2)} connections")

    return bridges


def protoevangelium_to_consummation():
    """The great chain from Genesis 3:15 to Revelation 22:21"""
    print("\n" + "="*60)
    print("THE GREAT CHAIN")
    print("From Protoevangelium to Consummation")
    print("="*60)
    return find_chain("Genesis 3:15", "Revelation 22:21")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        find_chain(sys.argv[1], sys.argv[2])
    else:
        protoevangelium_to_consummation()
