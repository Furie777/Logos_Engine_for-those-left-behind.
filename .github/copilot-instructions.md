# GitHub Copilot Instructions for Logos Engine

## Project Overview

**Logos Engine** is a self-contained Scripture study system that treats the Bible as a network graph. It combines the KJV Bible text with cross-references, Strong's Hebrew/Greek definitions, and semantic search capabilities to enable deep Scripture study offline.

**Purpose:** Designed to survive and serve when infrastructure fails - built for "those left behind."

**Key Stats:**
- 36,586 verses (KJV + 1611 Apocrypha)
- 14,180 Strong's entries (Hebrew + Greek)
- 2,588,197 cross-reference connections
- Built with NetworkX graph library

## Technology Stack

- **Language:** Python 3.x
- **Core Dependencies:**
  - NetworkX (graph operations) - REQUIRED
- **Optional Dependencies:**
  - graphviz (network visualization)
  - imagemagick (verse image generation)
  - figlet (ASCII banners)
  - fzf (fuzzy search)
  - espeak/pyttsx3 (text-to-speech)

## Project Architecture

```
Logos_Engine_for-those-left-behind./
├── logos.py                    # Main CLI entry point
├── src/                        # Core modules
│   ├── loader.py               # Data loading (KJV, Strong's, cross-refs)
│   ├── graph.py                # NetworkX graph builder
│   ├── query.py                # Search and query engine
│   ├── concordance.py          # Hebrew/Greek concordance
│   ├── semantic.py             # Semantic/meaning-based search
│   ├── visualize.py            # Graphviz visualization
│   ├── image.py                # ImageMagick verse images
│   ├── chain.py                # Network traversal (shortest path)
│   ├── fuzzy.py                # fzf integration
│   ├── integrity.py            # Data verification/checksums
│   ├── voice.py                # Text-to-speech
│   ├── pdf.py                  # PDF generation
│   ├── qr.py                   # QR code generation
│   ├── daily.py                # Daily verse (deterministic)
│   └── api.py                  # Bible API integration
├── neural/                     # Neural network demos
│   ├── baby_brain.py           # Simple neural demo
│   └── sentinel_brain.py       # SENTINEL architecture
├── data/                       # Scripture data
│   ├── kjv.json                # KJV verses (main)
│   ├── strongs.json            # Strong's definitions
│   ├── strongs_complete.json   # Complete Strong's data
│   ├── cross_refs.json         # Cross-references
│   ├── HebrewStrong.xml        # Hebrew source data
│   ├── strongsgreek.xml        # Greek source data
│   ├── apocrypha_*.json        # 1611 Apocrypha books
│   ├── apocrypha_structure.json # Apocrypha metadata
│   └── cache/                  # Cached data
├── docs/                       # Documentation
│   ├── INSTALL.md              # Installation guide
│   ├── RECOVERY.md             # Disaster recovery
│   ├── HARDWARE_KIT.md         # Physical hardware
│   └── FARADAY_ROOM_GUIDE.md   # EMP protection
└── output/                     # Generated files (created at runtime)
    ├── logos_graph.gpickle     # Pre-built graph
    ├── *.dot                   # Graphviz source files
    ├── *.png                   # Generated images
    ├── *.pdf                   # Generated PDF documents
    └── *.qr                    # QR code files
```

## Core Commands

### Setup and Initialization
```bash
# Download KJV text and setup data
python logos.py init

# Build the network graph from data
python logos.py build

# Verify data integrity
python logos.py verify
```

### Running the Application
```bash
# Look up a verse
python logos.py verse "John 3:16"

# Search for a term
python logos.py search "grace"

# Interactive query mode
python logos.py query

# Show statistics
python logos.py stats

# Display help
python logos.py help
```

### Development Testing
```bash
# Quick smoke test
python logos.py verse "Genesis 1:1" && python logos.py stats

# Test graph building
python logos.py build

# Test data integrity
python logos.py verify
```

**Note:** There is no formal test suite. Manual testing via CLI commands is the standard practice.

## Code Style and Conventions

### Python Style
- **Docstrings:** Use triple-quoted strings at the top of modules and classes
- **Imports:** Standard library first, then third-party, then local imports
- **Error Handling:** Graceful degradation - catch exceptions and provide helpful error messages
- **Dependencies:** Always check for optional dependencies and provide install instructions if missing

Example error handling pattern:
```python
try:
    import networkx as nx
except ImportError:
    print("ERROR: NetworkX library required but not found.")
    print("Install with: pip install networkx")
    sys.exit(1)
```

### Naming Conventions
- **Files:** lowercase with underscores (e.g., `build_strongs.py`, `parse_strongs_xml.py`)
- **Classes:** PascalCase (e.g., `LogosQuery`)
- **Functions:** lowercase with underscores (e.g., `load_kjv()`, `build_graph()`)
- **Constants:** UPPERCASE with underscores (e.g., `DATA_DIR`, `KJV_URL`)

### File Organization
- Core library code in `src/` directory
- Data files in `data/` directory
- Generated output in `output/` directory
- Documentation in `docs/` directory
- Main CLI in root `logos.py`

### Comments
- Keep comments minimal and purposeful
- Focus on explaining "why" not "what"
- Use docstrings for module/class/function documentation
- Add comments for non-obvious algorithms or biblical references

## Boundaries and Rules

### Files You SHOULD Edit
- `src/*.py` - Core functionality modules
- `logos.py` - Main CLI (when adding new commands)
- `docs/*.md` - Documentation
- `README.md` - Main documentation
- `build_*.py` - Build scripts for data processing

### Files You SHOULD NOT Edit
- `data/kjv.json` - Source Bible text (generated)
- `data/strongs.json` - Strong's definitions (generated)
- `data/strongs_complete.json` - Complete Strong's data (generated)
- `data/cross_refs.json` - Cross-references (generated)
- `data/apocrypha_*.json` - Apocrypha text (generated from API)
- `data/*.xml` - Source XML files (external)
- `data/cache/` - Cached data
- `output/` - All generated output files
- `.git*` - Git configuration
- `__pycache__/` - Python cache

### Security Considerations
- Never commit sensitive data or credentials
- No API keys should be in source code
- Data files are public domain Scripture text only
- No user authentication or personal data handling

### Project-Specific Guidelines
1. **Scripture Integrity:** Never modify or alter Scripture text except through proper data sources
2. **Offline-First:** All core features must work without internet
3. **Minimal Dependencies:** Keep required dependencies minimal (only NetworkX)
4. **Graceful Degradation:** Optional features (visualization, TTS) should fail gracefully
5. **Self-Documenting:** Code should be clear enough for future maintainers to rebuild from scratch
6. **Resilience:** System designed to survive infrastructure failure - prioritize robustness

## Common Tasks

### Adding a New Command
1. Add the command handler in `logos.py` main() function
2. Create corresponding function in appropriate `src/` module
3. Update the help text/docstring in `logos.py`
4. Test the command manually

### Adding a New Feature Module
1. Create file in `src/` directory
2. Import necessary dependencies with error handling
3. Follow existing module patterns (see `src/loader.py` or `src/query.py`)
4. Import and integrate in `logos.py`

### Modifying Data Processing
1. Build scripts are in root: `build_strongs.py`, `build_cross_refs.py`, etc.
2. Data loading logic is in `src/loader.py`
3. Always preserve existing data format compatibility
4. Test with `python logos.py verify`

## Special Considerations

### Biblical References
- Use standard notation: "Book Chapter:Verse" (e.g., "John 3:16")
- Support both full names and abbreviations
- Case-insensitive matching for user input

### Graph Operations
- The Bible is modeled as a directed graph (NetworkX DiGraph)
- Verses are nodes, cross-references are edges
- Use NetworkX algorithms for path finding, centrality, etc.

### Performance
- Pre-build graph and save as pickle for fast loading
- Lazy loading where possible
- Keep data in JSON for human readability

### Documentation Philosophy
- "For those left behind" - assume reader may have limited technical knowledge
- Provide step-by-step instructions
- Include offline-capable alternatives
- Document both the "how" and the "why"

## Examples to Follow

### Good: Module with dependency checking
```python
"""
LOGOS ENGINE - Query Engine
Search Scripture as network topology
"""

try:
    import networkx as nx
except ImportError:
    print("ERROR: NetworkX library required")
    print("Install with: pip install networkx")
    import sys
    sys.exit(1)

from .loader import load_kjv
```

### Good: Graceful feature degradation
```python
def visualize(ref):
    """Generate graph visualization"""
    try:
        import graphviz
    except ImportError:
        print("Graphviz not installed. Install with: apt install graphviz")
        print("Falling back to text output...")
        return text_representation(ref)
```

### Good: Clear error messages
```python
if ref not in self.kjv:
    print(f"Reference not found: {ref}")
    print("Try: python logos.py search <keyword>")
    return None
```

## Git Workflow

- Main development branch: `main`
- Work on feature branches for new features
- Keep commits focused and descriptive
- No force-pushing to shared branches

## Questions or Clarifications

If you're unsure about:
- **Scripture data formats:** Check `data/` directory and `src/loader.py`
- **Graph structure:** See `src/graph.py` and NetworkX documentation
- **CLI patterns:** Review `logos.py` main() function
- **Error handling:** Look at existing `src/` modules for patterns
- **Feature requirements:** Consider the "offline-first, resilient" design philosophy

---

*"For the word of God is quick, and powerful, and sharper than any twoedged sword"* - Hebrews 4:12

Built for those who seek truth, even when all systems fail.
