# LOGOS ENGINE - Quick Start Guide

**Get running in 60 seconds with simple copy-paste commands.**

---

## New Users: Choose Your Path

### Path A: Automated Setup (Recommended)

**Windows:**
1. Download this repository
2. Double-click `setup.bat`
3. Done!

**Linux/Mac/Raspberry Pi:**
```bash
bash setup.sh
```
Done!

---

### Path B: Manual Setup (3 commands)

**Copy and paste these commands one at a time:**

#### Windows (Command Prompt or PowerShell)
```cmd
pip install networkx
python logos.py build
python logos.py verse "John 3:16"
```

#### Linux/Mac/Raspberry Pi/Termux
```bash
pip3 install networkx
python3 logos.py build
python3 logos.py verse "John 3:16"
```

---

### Path C: One-Line Install (Advanced Users)

**Linux/Mac/Raspberry Pi:**
```bash
pip3 install networkx && python3 logos.py verse "John 3:16"
```

**Windows:**
```cmd
pip install networkx && python logos.py verse "John 3:16"
```

The graph will build automatically on first run.

---

## First Commands to Try

**After setup, copy and paste these:**

### Look up verses
```bash
# Linux/Mac/Termux
python3 logos.py verse "Genesis 1:1"
python3 logos.py verse "John 3:16"
python3 logos.py verse "Revelation 22:21"

# Windows
python logos.py verse "Genesis 1:1"
python logos.py verse "John 3:16"
python logos.py verse "Revelation 22:21"
```

### Search for words
```bash
# Linux/Mac/Termux
python3 logos.py search "grace"
python3 logos.py search "faith"
python3 logos.py search "love"

# Windows
python logos.py search "grace"
python logos.py search "faith"
python logos.py search "love"
```

### Study Hebrew/Greek
```bash
# Linux/Mac/Termux
python3 logos.py strongs H430   # Hebrew word for "God"
python3 logos.py strongs G26    # Greek word for "love"

# Windows
python logos.py strongs H430    # Hebrew word for "God"
python logos.py strongs G26     # Greek word for "love"
```

### Network Statistics
```bash
# Linux/Mac/Termux
python3 logos.py stats

# Windows
python logos.py stats
```

### Get Help
```bash
# Linux/Mac/Termux
python3 logos.py help

# Windows
python logos.py help
```

---

## Installation Details

### What Gets Installed
- **networkx** - Python library for graph networks (required)
- **Graph database** - Built from Bible data (automatic on first run)

### Storage Required
- Minimum: 200 MB
- Recommended: 500 MB

### No Internet Required
Once installed, LOGOS ENGINE runs completely offline.

---

## Troubleshooting

### "python not found"
**Fix:** Use `python3` instead of `python`
```bash
python3 logos.py verse "John 3:16"
```

### "pip not found"
**Fix:** Install pip first

**Ubuntu/Debian:**
```bash
sudo apt install python3-pip
```

**Mac:**
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

**Windows:**
- Reinstall Python from python.org
- Check "Add Python to PATH" during installation

### "No module named networkx"
**Fix:** Install networkx
```bash
# Linux/Mac
pip3 install networkx

# Windows
pip install networkx
```

### "Permission denied" (Linux/Mac)
**Fix:** Make setup script executable
```bash
chmod +x setup.sh
./setup.sh
```

### "Graph not found"
**Fix:** Build the graph
```bash
# Linux/Mac
python3 logos.py build

# Windows
python logos.py build
```

---

## For AI Agents and Automated Systems

### Installation Command (Unix-like)
```bash
cd /path/to/Logos_Engine_for-those-left-behind. && pip3 install --user networkx && python3 logos.py build
```

### Installation Command (Windows)
```cmd
cd C:\path\to\Logos_Engine_for-those-left-behind. && pip install networkx && python logos.py build
```

### Verification Command
```bash
# Unix-like
python3 logos.py verse "John 3:16"

# Windows
python logos.py verse "John 3:16"
```

Expected output:
```
For God so loved the world, that he gave his only begotten Son, that whosoever
believeth in him should not perish, but have everlasting life.
```

### API-Style Usage (from Python code)
```python
# Add to your Python script
import sys
from pathlib import Path
sys.path.insert(0, str(Path('/path/to/Logos_Engine_for-those-left-behind.')))

from src.query import LogosQuery

# Initialize
logos = LogosQuery()

# Get a verse
verse = logos.verse("John 3:16")
print(verse)

# Search
results = logos.search("grace")
for ref, text in results:
    print(f"{ref}: {text}")
```

---

## Complete Feature List

Once installed, you have access to:

- **Verse Lookup** - All 36,586 verses (KJV + Apocrypha)
- **Text Search** - Search by any word or phrase
- **Hebrew/Greek Study** - 14,180 Strong's definitions
- **Semantic Search** - Find verses by meaning, not just keywords
- **Network Analysis** - See how verses connect
- **Cross-References** - 2.5 million connections between verses
- **Interactive Modes** - Query, concordance, semantic search
- **Visualization** - Network graphs (requires graphviz)
- **Image Generation** - Shareable verse images (requires imagemagick)

See `README.md` for complete command list.

---

## Next Steps

1. Read `START_HERE.txt` - Understand what this is
2. Read `WHY.txt` - The Gospel message
3. Read `README.md` - Complete documentation
4. Read `docs/INSTALL.md` - Detailed installation guide
5. Try commands above
6. Explore interactive modes:
   ```bash
   python3 logos.py query        # Interactive query mode
   python3 logos.py concordance  # Hebrew/Greek explorer
   python3 logos.py semantic     # Meaning-based search
   ```

---

## Share This

This is freely given. Share widely.

```bash
# Clone command for others
git clone https://github.com/Furie777/Logos_Engine_for-those-left-behind..git
cd Logos_Engine_for-those-left-behind.
bash setup.sh  # Linux/Mac
# or
setup.bat      # Windows
```

---

*"Write the vision, and make it plain upon tables, that he may run that readeth it."* - Habakkuk 2:2

**Built Thanksgiving 2025 | For those left behind**
