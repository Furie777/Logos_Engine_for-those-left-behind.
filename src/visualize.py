#!/usr/bin/env python3
"""
LOGOS ENGINE - Visualization Module
Generates visual network maps using Graphviz

Commands:
    python logos.py graph "John 3:16"              # Visual map of connections
    python logos.py graph "Romans 8:28" --depth 2  # Deeper traversal
    python logos.py banner "LOGOS"                 # ASCII art banner

Requires: graphviz (pkg install graphviz)
Optional: figlet (pkg install figlet)

Glory to LOGOS.
"""

import os
import subprocess
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def load_data():
    """Load KJV and cross-references"""
    kjv_path = DATA_DIR / "kjv.json"
    xref_path = DATA_DIR / "cross_refs.json"

    kjv = {}
    cross_refs = {}

    if kjv_path.exists():
        with open(kjv_path, 'r') as f:
            kjv = json.load(f)

    if xref_path.exists():
        with open(xref_path, 'r') as f:
            cross_refs = json.load(f)

    return kjv, cross_refs


def normalize_ref(ref):
    """Normalize reference format (Psalm -> Psalms, etc.)"""
    ref = ref.strip()

    # Common corrections
    if ref.startswith("Psalm ") and not ref.startswith("Psalms "):
        ref = "Psalms " + ref[6:]

    return ref


def get_connections(ref, cross_refs, depth=1, max_per_level=10):
    """Get connected verses up to specified depth"""
    ref = normalize_ref(ref)
    connections = {}
    visited = set()
    current_level = [ref]

    for d in range(depth):
        next_level = []
        for r in current_level:
            if r in visited:
                continue
            visited.add(r)

            # Get connections for this reference
            refs_out = cross_refs.get(r, [])[:max_per_level]
            connections[r] = refs_out
            next_level.extend(refs_out)

        current_level = next_level

    return connections


def generate_dot(ref, connections, kjv):
    """Generate Graphviz DOT format"""
    ref = normalize_ref(ref)

    lines = [
        'digraph LOGOS {',
        '  rankdir=LR;',
        '  node [shape=box, style=rounded, fontname="Helvetica"];',
        '  edge [color="#666666"];',
        '',
        f'  // Central verse: {ref}',
        f'  "{ref}" [style="filled,rounded", fillcolor=gold, penwidth=2];',
        ''
    ]

    # Add edges
    for source, targets in connections.items():
        for target in targets:
            lines.append(f'  "{source}" -> "{target}";')

    # Add tooltips with verse text (if available)
    lines.append('')
    lines.append('  // Verse text tooltips')
    all_refs = set(connections.keys())
    for targets in connections.values():
        all_refs.update(targets)

    for r in all_refs:
        text = kjv.get(r, "")[:80].replace('"', "'")
        if text:
            lines.append(f'  "{r}" [tooltip="{text}..."];')

    lines.append('}')

    return '\n'.join(lines)


def generate_graph(ref, depth=1, output_format='png'):
    """Generate visual graph for a verse"""
    ref = normalize_ref(ref)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load data
    kjv, cross_refs = load_data()

    if ref not in kjv and ref not in cross_refs:
        print(f"Reference not found: {ref}")
        return None

    # Get connections
    connections = get_connections(ref, cross_refs, depth=depth)

    if not connections:
        print(f"No connections found for: {ref}")
        return None

    # Generate DOT
    dot_content = generate_dot(ref, connections, kjv)

    # Safe filename
    safe_name = ref.replace(" ", "_").replace(":", "_")
    dot_path = OUTPUT_DIR / f"{safe_name}.dot"
    output_path = OUTPUT_DIR / f"{safe_name}_graph.{output_format}"

    # Write DOT file
    with open(dot_path, 'w') as f:
        f.write(dot_content)

    # Generate image with graphviz
    try:
        result = subprocess.run(
            ['dot', f'-T{output_format}', str(dot_path), '-o', str(output_path)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Count connections
            total_edges = sum(len(targets) for targets in connections.values())
            total_nodes = len(set(connections.keys()) | set(t for targets in connections.values() for t in targets))

            print(f"\n=== LOGOS GRAPH: {ref} ===\n")
            print(f"Nodes: {total_nodes}")
            print(f"Edges: {total_edges}")
            print(f"Depth: {depth}")
            print(f"\nGenerated: {output_path}")
            print(f"DOT file:  {dot_path}")

            # Show verse text
            if ref in kjv:
                print(f"\n{ref}")
                print(f"{kjv[ref]}")

            return str(output_path)
        else:
            print(f"Graphviz error: {result.stderr}")
            return None

    except FileNotFoundError:
        print("Graphviz not installed. Install with: pkg install graphviz")
        print(f"DOT file saved to: {dot_path}")
        return str(dot_path)


def ascii_banner(text, font='slant'):
    """Generate ASCII art banner using figlet"""
    try:
        result = subprocess.run(
            ['figlet', '-f', font, text],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"=== {text} ==="
    except FileNotFoundError:
        # Figlet not installed - simple fallback
        return f"\n{'='*50}\n{text.center(50)}\n{'='*50}\n"


def show_banner(text, font='slant'):
    """Display ASCII art banner"""
    banner = ascii_banner(text, font)
    print(banner)


def graph_repl():
    """Interactive graph generation mode"""
    print(ascii_banner("LOGOS GRAPH", 'small'))
    print("Visual Network Explorer")
    print("Commands: <reference>, depth <n>, format <png|svg>, quit")
    print()

    depth = 1
    output_format = 'png'

    while True:
        try:
            user_input = input("graph> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFarewell.")
            break

        if not user_input:
            continue

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Farewell.")
            break

        if user_input.lower().startswith('depth '):
            try:
                depth = int(user_input.split()[1])
                print(f"Depth set to {depth}")
            except:
                print("Usage: depth <number>")
            continue

        if user_input.lower().startswith('format '):
            fmt = user_input.split()[1].lower()
            if fmt in ['png', 'svg', 'pdf']:
                output_format = fmt
                print(f"Format set to {output_format}")
            else:
                print("Formats: png, svg, pdf")
            continue

        # Treat as verse reference
        generate_graph(user_input, depth=depth, output_format=output_format)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ref = ' '.join(sys.argv[1:])
        generate_graph(ref)
    else:
        graph_repl()
