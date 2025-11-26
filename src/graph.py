"""
LOGOS ENGINE - Graph Builder
Creates NetworkX graph from Scripture + cross-references
"""

import json
import pickle
from pathlib import Path

try:
    import networkx as nx
except ImportError:
    print("Installing networkx...")
    import subprocess
    subprocess.run(["pip", "install", "networkx"])
    import networkx as nx

from .loader import load_kjv, load_cross_references

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def build_graph():
    """Build Scripture network graph"""
    print("=== BUILDING LOGOS GRAPH ===\n")

    kjv = load_kjv()
    cross_refs = load_cross_references()

    if not kjv:
        print("ERROR: KJV not loaded")
        return None

    G = nx.DiGraph()

    # Add all verses as nodes
    print(f"Adding {len(kjv)} verse nodes...")
    for ref, text in kjv.items():
        G.add_node(ref, text=text, book=ref.split()[0])

    # Add cross-reference edges
    edge_count = 0
    print("Adding cross-reference edges...")

    for from_ref, to_refs in cross_refs.items():
        if isinstance(to_refs, list):
            for to_ref in to_refs:
                if from_ref in G.nodes and to_ref in G.nodes:
                    if not G.has_edge(from_ref, to_ref):
                        G.add_edge(from_ref, to_ref, type='cross_ref')
                        edge_count += 1

    print(f"Added {edge_count} cross-reference edges")

    # Add sequential edges (verse to next verse)
    print("Adding sequential edges...")
    refs = list(kjv.keys())
    seq_count = 0
    for i in range(len(refs) - 1):
        # Only connect within same book
        if refs[i].split()[0] == refs[i+1].split()[0]:
            G.add_edge(refs[i], refs[i+1], type='sequential')
            seq_count += 1

    print(f"Added {seq_count} sequential edges")

    # Save graph
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph_path = OUTPUT_DIR / "logos_graph.gpickle"

    with open(graph_path, 'wb') as f:
        pickle.dump(G, f)

    print(f"\nGraph saved to {graph_path}")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")

    return G


def load_graph():
    """Load existing graph from pickle"""
    graph_path = OUTPUT_DIR / "logos_graph.gpickle"

    if not graph_path.exists():
        print("Graph not found. Building...")
        return build_graph()

    with open(graph_path, 'rb') as f:
        return pickle.load(f)


def get_stats(G=None):
    """Get graph statistics"""
    if G is None:
        G = load_graph()

    stats = {
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_connected': nx.is_weakly_connected(G) if G.is_directed() else nx.is_connected(G)
    }

    # Top 10 by degree centrality
    degree_cent = nx.degree_centrality(G)
    stats['top_10_central'] = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]

    return stats


if __name__ == "__main__":
    G = build_graph()
    if G:
        stats = get_stats(G)
        print("\n=== GRAPH STATISTICS ===")
        print(f"Nodes: {stats['nodes']}")
        print(f"Edges: {stats['edges']}")
        print(f"Density: {stats['density']:.6f}")
        print("\nTop 10 Central Verses:")
        for ref, score in stats['top_10_central']:
            print(f"  {ref}: {score:.4f}")
