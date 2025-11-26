# LOGOS ENGINE - Complete Recovery Guide

**How to rebuild everything from scratch if needed.**

---

## SCENARIO 1: You Have the Archive (Easiest)

If you have the LOGOS_ENGINE folder intact on USB, SD card, or phone:

### On Termux (Android)

```bash
# 1. Install Termux from F-Droid (not Play Store)
# 2. Open Termux and run:

pkg update && pkg upgrade
pkg install python

# 3. Setup storage access
termux-setup-storage
# (Grant permission when prompted)

# 4. Copy archive from phone storage
cp -r ~/storage/shared/LOGOS_BACKUP ~/LOGOS_ENGINE
# OR from USB/SD:
cp -r ~/storage/external-1/LOGOS_ENGINE ~/LOGOS_ENGINE

# 5. Install Python dependency
pip install networkx

# 6. Test
cd ~/LOGOS_ENGINE
python logos.py verse "John 3:16"
```

### On Linux / Raspberry Pi

```bash
# 1. Install Python
sudo apt update
sudo apt install python3 python3-pip

# 2. Copy archive
cp -r /media/USB_DRIVE/LOGOS_ENGINE ~/LOGOS_ENGINE

# 3. Install dependency
pip3 install networkx

# 4. Test
cd ~/LOGOS_ENGINE
python3 logos.py verse "John 3:16"
```

### On Windows

```
1. Install Python from python.org (check "Add to PATH")
2. Copy LOGOS_ENGINE folder from USB to C:\LOGOS_ENGINE
3. Open Command Prompt (Win+R, type cmd)
4. Run:
   pip install networkx
   cd C:\LOGOS_ENGINE
   python logos.py verse "John 3:16"
```

### On Mac

```bash
# 1. Open Terminal
# 2. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. Install Python
brew install python

# 4. Copy archive
cp -r /Volumes/USB_DRIVE/LOGOS_ENGINE ~/LOGOS_ENGINE

# 5. Install and test
pip3 install networkx
cd ~/LOGOS_ENGINE
python3 logos.py verse "John 3:16"
```

---

## SCENARIO 2: Data Files Are Corrupted

If the archive exists but JSON files are corrupted:

### Rebuild Cross-References

```bash
cd ~/LOGOS_ENGINE
python build_cross_refs.py
```

This recreates `data/cross_refs.json` from scratch using:
- OT-NT quotation links
- Keyword connections
- Phrase matching

### Rebuild Strong's Concordance

```bash
python parse_strongs_xml.py
```

This recreates `data/strongs.json` from the XML source files:
- `data/HebrewStrong.xml` (8,674 Hebrew entries)
- `data/strongsgreek.xml` (5,506 Greek entries)

### Rebuild Graph

```bash
python logos.py build
```

This recreates `output/logos_graph.gpickle` from kjv.json and cross_refs.json.

---

## SCENARIO 3: You Only Have Source Data

If you only have the raw data files (kjv.json, XML files):

### Required Files

```
data/
├── kjv.json              # KJV Bible text (CRITICAL)
├── HebrewStrong.xml      # Hebrew Strong's source
├── strongsgreek.xml      # Greek Strong's source
```

### Rebuild Everything

```bash
# 1. Rebuild Strong's from XML
python parse_strongs_xml.py

# 2. Rebuild cross-references
python build_cross_refs.py

# 3. Rebuild graph
python logos.py build

# 4. Test
python logos.py stats
```

---

## SCENARIO 4: You Have Nothing But Internet

If starting completely fresh with internet access:

### Step 1: Create Directory Structure

```bash
mkdir -p LOGOS_ENGINE/{data,src,output,docs}
cd LOGOS_ENGINE
```

### Step 2: Download KJV Bible

```bash
# From GitHub (thiagobodruk/bible)
curl -o data/kjv_raw.json "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"
```

Or manually download from:
- https://github.com/thiagobodruk/bible
- https://www.sacred-texts.com/bib/kjv/
- https://ebible.org/kjv/

### Step 3: Download Strong's XML

Hebrew:
```bash
curl -o data/HebrewStrong.xml "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/HebrewStrong.xml"
```

Greek:
```bash
curl -o data/strongsgreek.xml "https://raw.githubusercontent.com/morphgnt/strongs-dictionary-xml/master/strongsgreek.xml"
```

### Step 4: Recreate Python Files

You'll need to recreate the source code. The key files are:

**logos.py** - Main CLI entry point
**src/loader.py** - Loads KJV data
**src/graph.py** - Builds NetworkX graph
**src/query.py** - Query functions
**src/concordance.py** - Hebrew/Greek lookup
**src/semantic.py** - Semantic search

If you have a copy of the code anywhere, use it. If not, the logic is:
1. Load KJV JSON into dictionary {reference: text}
2. Build NetworkX graph with verses as nodes
3. Add edges for cross-references and sequential reading
4. Provide search, lookup, and analysis functions

### Step 5: Download Apocrypha (Optional)

The 1611 KJV included 14 Apocrypha books. To add them:

```bash
# Uses bible-api.com (rate limited)
python download_apocrypha.py
python logos.py merge
```

Apocrypha books:
- 1 Esdras, 2 Esdras
- Tobit, Judith
- Wisdom of Solomon, Sirach (Ecclesiasticus)
- Baruch, Letter of Jeremiah
- Prayer of Azariah, Susanna, Bel and the Dragon
- Prayer of Manasseh
- 1 Maccabees, 2 Maccabees

---

## SCENARIO 5: No Internet, No Archive

Absolute worst case. You have a device but no data.

### Option A: Physical Bible

Use your physical KJV Bible. This system was always just a tool to help
study the Word - the Word itself is what matters.

### Option B: Find Another Copy

This archive was designed to be copied and distributed. Look for:
- Other believers who may have copies
- USB drives in cached locations
- Printed copies of recovery instructions

### Option C: Manual Recreation

If you have time and a physical Strong's Concordance:
1. Type in the KJV text (or find any digital copy)
2. Manually create cross-references by reading
3. Build the connections the old-fashioned way

The early church had none of this technology. They had the Word, the Spirit,
and each other. That's enough.

---

## DATA FILE FORMATS

### kjv.json

```json
{
  "Genesis 1:1": "In the beginning God created the heaven and the earth.",
  "Genesis 1:2": "And the earth was without form, and void...",
  ...
}
```

Simple dictionary: reference string → verse text.

### strongs.json

```json
{
  "H430": {
    "hebrew": "אֱלֹהִים",
    "translit": "elohiym",
    "def": "gods, God, judges, angels",
    "kjv": "God, god, judge, mighty..."
  },
  "G26": {
    "greek": "ἀγάπη",
    "translit": "agape",
    "def": "love, charity",
    "kjv": "love, charity, dear..."
  },
  ...
}
```

### cross_refs.json

```json
{
  "Genesis 1:1": ["John 1:1", "Hebrews 1:10", "Colossians 1:16"],
  "John 3:16": ["Romans 5:8", "1 John 4:9", "Ephesians 2:4"],
  ...
}
```

Dictionary: reference → list of connected references.

---

## VERIFYING YOUR INSTALLATION

Run these tests:

```bash
# Basic verse lookup
python logos.py verse "John 3:16"
# Should show: "For God so loved the world..."

# Search
python logos.py search "grace"
# Should show multiple verses

# Strong's lookup
python logos.py strongs H430
# Should show: Elohim, "gods, God, judges..."

# Semantic search
python logos.py similar "John 3:16"
# Should show related verses about salvation/eternal life

# Graph stats
python logos.py stats
# Should show: ~36,000 nodes, ~2.5M edges
```

If all pass, your installation is complete.

---

## COMMON PROBLEMS

### "No module named networkx"
```bash
pip install networkx
# or
pip3 install networkx
```

### "python: command not found"
```bash
# Try python3
python3 logos.py verse "John 3:16"
```

### "File not found: kjv.json"
```bash
# Check you're in the right directory
pwd
ls data/
# Should see kjv.json
```

### "Permission denied"
```bash
chmod +x logos.py
chmod -R 755 LOGOS_ENGINE/
```

### "JSON decode error"
Data file is corrupted. Restore from backup or rebuild:
```bash
python build_cross_refs.py
python parse_strongs_xml.py
```

### "Graph not found"
```bash
python logos.py build
```

---

## CONTACT / ATTRIBUTION

**Original Builder**: Taylor Weathers, November 2025

**Built With**:
- Claude Code (Anthropic)
- Python 3 / NetworkX
- Termux on Android

**Data Sources**:
- KJV text: github.com/thiagobodruk/bible
- Strong's Hebrew: github.com/openscriptures/HebrewLexicon
- Strong's Greek: github.com/morphgnt/strongs-dictionary-xml
- Apocrypha: bible-api.com

**License**: Freely given, freely share. The Word of God belongs to no one
and everyone.

---

*"The grass withereth, the flower fadeth: but the word of our God shall
stand for ever."* - Isaiah 40:8

---

Built November 2025 | "until it is all in all" - 1 Corinthians 15:28
