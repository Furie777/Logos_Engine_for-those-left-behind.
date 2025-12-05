#!/usr/bin/env python3
"""
LOGOS ENGINE - Example Usage Script

This demonstrates how to use LOGOS ENGINE programmatically from Python code.
Perfect for AI agents, automated systems, or integration into other applications.
"""

import sys
from pathlib import Path

# Add LOGOS ENGINE to Python path
# Adjust this path to where you have LOGOS ENGINE installed
LOGOS_PATH = Path(__file__).parent
sys.path.insert(0, str(LOGOS_PATH))

def example_basic_usage():
    """Basic verse lookup and search"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70)
    
    from src.query import LogosQuery
    
    # Initialize LOGOS
    logos = LogosQuery()
    
    # Get a single verse
    print("\n1. Looking up John 3:16:")
    verse = logos.verse("John 3:16")
    print(f"   {verse}")
    
    # Search for a word
    print("\n2. Searching for 'grace' (first 3 results):")
    results = logos.search("grace")
    for ref, text in results[:3]:
        print(f"   {ref}: {text[:60]}...")
    
    print(f"\n   Total results: {len(results)}")


def example_strongs():
    """Hebrew/Greek word study"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Hebrew/Greek Study")
    print("=" * 70)
    
    from src.concordance import Concordance
    
    conc = Concordance()
    
    # Look up a Strong's number
    print("\n1. Looking up H430 (Hebrew for 'God'):")
    definition = conc.get_strongs_definition("H430")
    if definition:
        print(f"   Hebrew: {definition.get('hebrew', 'N/A')}")
        print(f"   Transliteration: {definition.get('transliteration', 'N/A')}")
        print(f"   Definition: {definition.get('definition', 'N/A')}")
        print(f"   Occurrences: {definition.get('occur', 'N/A')}")


def example_semantic():
    """Semantic/meaning-based search"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Semantic Search")
    print("=" * 70)
    
    from src.semantic import SemanticSearch
    
    sem = SemanticSearch()
    
    # Find similar verses
    print("\n1. Finding verses similar to John 3:16 (top 3):")
    similar = sem.similar_verses("John 3:16", n=3)
    for ref, score in similar:
        print(f"   {score:.3f} - {ref}")
        print(f"          {sem.kjv[ref][:60]}...")
    
    # Search by meaning
    print("\n2. Searching by meaning: 'God saves sinners' (top 3):")
    results = sem.search_meaning("God saves sinners", n=3)
    for ref, text, score in results:
        print(f"   {score:.3f} - {ref}")
        print(f"          {text[:60]}...")


def example_network():
    """Network graph analysis"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Network Analysis")
    print("=" * 70)
    
    from src.graph import load_graph, get_stats
    
    # Load the graph
    print("\n1. Loading network graph...")
    G = load_graph()
    
    # Get statistics
    print("\n2. Network statistics:")
    stats = get_stats(G)
    print(f"   Verses (nodes): {stats['nodes']:,}")
    print(f"   Connections (edges): {stats['edges']:,}")
    print(f"   Network density: {stats['density']:.6f}")
    print(f"   Is connected: {stats['is_connected']}")
    
    print("\n3. Most central verses (top 3):")
    for ref, score in stats['top_10_central'][:3]:
        print(f"   {score:.4f} - {ref}")


def example_batch_processing():
    """Process multiple verses at once"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Batch Processing")
    print("=" * 70)
    
    from src.query import LogosQuery
    
    logos = LogosQuery()
    
    # List of verses to look up
    verses_to_lookup = [
        "Genesis 1:1",
        "John 1:1",
        "John 3:16",
        "Romans 8:28",
        "Revelation 22:21"
    ]
    
    print("\n Looking up multiple verses:")
    for ref in verses_to_lookup:
        verse = logos.verse(ref)
        print(f"\n   {ref}")
        print(f"   {verse[:70]}...")


def main():
    """Run all examples"""
    print("\n")
    print("=" * 70)
    print(" LOGOS ENGINE - Python API Examples")
    print("=" * 70)
    print("\n This script demonstrates programmatic usage of LOGOS ENGINE.")
    print(" Perfect for AI agents, automation, and integration.\n")
    
    try:
        example_basic_usage()
        example_strongs()
        example_semantic()
        example_network()
        example_batch_processing()
        
        print("\n" + "=" * 70)
        print(" All examples completed successfully!")
        print("=" * 70)
        print("\n Use these patterns in your own code to integrate LOGOS ENGINE.")
        print(" See src/ directory for more functionality.\n")
        
    except ImportError as e:
        print(f"\n ERROR: Missing required module - {e}")
        print("\n Make sure networkx is installed: 'pip3 install networkx'")
        print(" and that you're running from the LOGOS ENGINE directory.\n")
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"\n ERROR: Required file not found - {e}")
        print("\n Make sure you've run 'python3 logos.py build' first")
        print(" to create the graph database.\n")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        print("\n This might happen if:")
        print(" 1. You haven't run 'python3 logos.py build' yet")
        print(" 2. networkx is not installed: 'pip3 install networkx'")
        print(" 3. You're not in the LOGOS ENGINE directory\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
