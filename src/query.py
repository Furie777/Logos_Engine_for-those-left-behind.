"""
LOGOS ENGINE - Query Engine
Search Scripture as network topology
"""

import re
from collections import Counter

try:
    import networkx as nx
except ImportError:
    print("\n" + "=" * 60)
    print("ERROR: NetworkX library required but not found.")
    print("=" * 60)
    print("\nInstall with:")
    print("    pip install networkx")
    print("\nOr on some systems:")
    print("    pip3 install networkx")
    print("=" * 60 + "\n")
    import sys
    sys.exit(1)

from .graph import load_graph
from .loader import load_kjv


class LogosQuery:
    """Query interface for LOGOS Scripture graph"""

    def __init__(self):
        self.G = load_graph()
        self.kjv = load_kjv()
        print(f"LOGOS ready: {self.G.number_of_nodes()} verses, {self.G.number_of_edges()} connections")

    def verse(self, ref):
        """Get verse text by reference"""
        if ref in self.kjv:
            return self.kjv[ref]
        # Try fuzzy match
        for key in self.kjv:
            if ref.lower() in key.lower():
                return f"{key}: {self.kjv[key]}"
        return None

    def connections(self, ref, depth=1):
        """Get verses connected to given reference"""
        if ref not in self.G.nodes:
            print(f"Reference not found: {ref}")
            return []

        if depth == 1:
            # Direct connections
            outgoing = list(self.G.successors(ref))
            incoming = list(self.G.predecessors(ref))
            return {
                'outgoing': outgoing,
                'incoming': incoming,
                'total': len(outgoing) + len(incoming)
            }
        else:
            # Multi-hop connections using BFS
            connected = set()
            current = {ref}
            for _ in range(depth):
                next_level = set()
                for node in current:
                    next_level.update(self.G.successors(node))
                    next_level.update(self.G.predecessors(node))
                connected.update(next_level)
                current = next_level - connected

            connected.discard(ref)
            return list(connected)

    def path(self, from_ref, to_ref):
        """Find shortest path between two verses"""
        try:
            path = nx.shortest_path(self.G, from_ref, to_ref)
            return path
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound as e:
            print(f"Node not found: {e}")
            return None

    def central(self, n=10, book=None):
        """Get most central verses (by degree)"""
        if book:
            nodes = [n for n in self.G.nodes if n.startswith(book)]
            subgraph = self.G.subgraph(nodes)
            centrality = nx.degree_centrality(subgraph)
        else:
            centrality = nx.degree_centrality(self.G)

        sorted_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return sorted_central[:n]

    def search(self, term, limit=20):
        """Search verses containing term"""
        results = []
        term_lower = term.lower()

        for ref, text in self.kjv.items():
            if term_lower in text.lower():
                results.append((ref, text))
                if len(results) >= limit:
                    break

        return results

    def cluster(self, ref, radius=2):
        """Get cluster of verses around a reference"""
        if ref not in self.G.nodes:
            return None

        # Get ego graph (local neighborhood)
        ego = nx.ego_graph(self.G, ref, radius=radius, undirected=True)

        return {
            'center': ref,
            'nodes': list(ego.nodes),
            'size': ego.number_of_nodes(),
            'edges': ego.number_of_edges()
        }

    def themes(self, book=None):
        """Identify thematic clusters using community detection"""
        if book:
            nodes = [n for n in self.G.nodes if n.startswith(book)]
            subgraph = self.G.subgraph(nodes).to_undirected()
        else:
            # Use undirected version for community detection
            subgraph = self.G.to_undirected()

        try:
            from networkx.algorithms import community
            communities = community.greedy_modularity_communities(subgraph)
            return [list(c)[:10] for c in list(communities)[:5]]  # Top 5 communities, 10 verses each
        except:
            return None

    def witness(self, term, n=3):
        """Three-witness pattern: find multiple verses supporting a concept"""
        results = self.search(term, limit=50)

        if len(results) < n:
            return results

        # Score by connectivity
        scored = []
        for ref, text in results:
            if ref in self.G.nodes:
                degree = self.G.degree(ref)
                scored.append((ref, text, degree))

        # Return top n by connectivity
        scored.sort(key=lambda x: x[2], reverse=True)
        return [(r, t) for r, t, _ in scored[:n]]


def repl():
    """Interactive LOGOS query REPL"""
    logos = LogosQuery()

    print("\n=== LOGOS ENGINE ===")
    print("Commands: verse, search, path, central, cluster, witness, quit")
    print("Example: verse John 3:16")
    print("Example: search love")
    print("Example: witness faith")
    print()

    while True:
        try:
            cmd = input("LOGOS> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShalom.")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command == 'quit' or command == 'exit':
            print("Shalom.")
            break

        elif command == 'verse':
            result = logos.verse(arg)
            if result:
                print(f"\n{result}\n")
            else:
                print("Verse not found")

        elif command == 'search':
            results = logos.search(arg)
            print(f"\nFound {len(results)} verses containing '{arg}':\n")
            for ref, text in results[:10]:
                print(f"{ref}: {text[:80]}...")
            print()

        elif command == 'path':
            refs = arg.split(' to ')
            if len(refs) == 2:
                path = logos.path(refs[0].strip(), refs[1].strip())
                if path:
                    print(f"\nPath ({len(path)} steps):")
                    for p in path:
                        print(f"  -> {p}")
                    print()
                else:
                    print("No path found")
            else:
                print("Usage: path Genesis 1:1 to Revelation 22:21")

        elif command == 'central':
            n = int(arg) if arg.isdigit() else 10
            results = logos.central(n)
            print(f"\nTop {n} central verses:")
            for ref, score in results:
                print(f"  {ref}: {score:.4f}")
            print()

        elif command == 'cluster':
            result = logos.cluster(arg)
            if result:
                print(f"\nCluster around {arg}:")
                print(f"  Size: {result['size']} verses")
                print(f"  Edges: {result['edges']} connections")
                print(f"  Sample: {result['nodes'][:5]}")
            else:
                print("Reference not found")

        elif command == 'witness':
            results = logos.witness(arg)
            print(f"\nThree-witness pattern for '{arg}':\n")
            for i, (ref, text) in enumerate(results, 1):
                print(f"Witness {i}: {ref}")
                print(f"  {text[:100]}...\n")

        elif command == 'help':
            print("\nCommands:")
            print("  verse <ref>     - Get verse text")
            print("  search <term>   - Search for term")
            print("  path <A> to <B> - Find path between verses")
            print("  central [n]     - Top n central verses")
            print("  cluster <ref>   - Get verse cluster")
            print("  witness <term>  - Three-witness pattern")
            print("  quit            - Exit")
            print()

        else:
            print(f"Unknown command: {command}. Type 'help' for options.")


if __name__ == "__main__":
    repl()
