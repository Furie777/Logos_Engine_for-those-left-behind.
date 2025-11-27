# LOGOS ENGINE
## Scripture as Living Network - KJV + 1611 Apocrypha

**Built:** November 26-27, 2025 | Thanksgiving
**Builder:** Taylor Weathers
**Purpose:** For those left behind, that some may come to the knowledge of the truth

---

## What This Is

A self-contained Scripture study system designed to survive and serve when infrastructure fails.

| Component | Count |
|-----------|-------|
| Verses (KJV + Apocrypha) | 36,586 |
| Strong's entries (Hebrew + Greek) | 14,180 |
| Cross-reference connections | 2,588,197 |
| Theological concepts | 76 |
| Semantic word mappings | 99 |

**Runs offline. Runs anywhere. No internet required.**

---

## Quick Start

### Option A: Download ZIP (no coding required)

1. Click the green **"Code"** button above
2. Click **"Download ZIP"**
3. Extract the ZIP to a folder
4. Follow `docs/INSTALL.md` for your platform

### Option B: Git Clone

```bash
git clone https://github.com/Furie777/Logos_Engine_for-those-left-behind..git
cd Logos_Engine_for-those-left-behind.

# Install dependency
pip install networkx

# Test
python logos.py verse "John 3:16"
```

---

## Commands

### Verse Lookup
```bash
python logos.py verse "Genesis 1:1"
python logos.py verse "John 1:1"
python logos.py verse "Revelation 22:21"
```

### Search
```bash
python logos.py search "grace"
python logos.py search "faith"
python logos.py witness "salvation"    # Find three witnesses
```

### Hebrew/Greek Study
```bash
python logos.py strongs H430    # Elohim - God
python logos.py strongs H3068   # YHWH - LORD
python logos.py strongs G26     # Agape - Love
python logos.py strongs G4102   # Pistis - Faith
```

### Semantic Search (by meaning)
```bash
python logos.py similar "John 3:16"           # Find similar verses
python logos.py concept salvation             # Search by concept
python logos.py meaning "God saves sinners"   # Search by meaning
```

### Interactive Modes
```bash
python logos.py query         # Interactive search
python logos.py concordance   # Hebrew/Greek explorer
python logos.py semantic      # Meaning-based search
```

### System
```bash
python logos.py stats    # Show network statistics
python logos.py build    # Rebuild graph from data
python logos.py help     # Show all commands
```

---

## Architecture

```
LOGOS_ENGINE/
├── logos.py                    # Main CLI
├── START_HERE.txt              # First contact document
├── WHY.txt                     # The witness (Gospel)
├── GOSSIP.md                   # Share this
│
├── src/
│   ├── loader.py               # Data loading
│   ├── graph.py                # NetworkX graph builder
│   ├── query.py                # Search functions
│   ├── concordance.py          # Hebrew/Greek tools
│   ├── semantic.py             # Meaning-based search
│   └── api.py                  # Bible API (optional)
│
├── data/
│   ├── kjv.json                # 36,586 verses
│   ├── strongs.json            # 14,180 definitions
│   ├── cross_refs.json         # 2.5M+ connections
│   ├── HebrewStrong.xml        # Source Hebrew data
│   └── strongsgreek.xml        # Source Greek data
│
├── docs/
│   ├── INSTALL.md              # Complete setup guide
│   ├── RECOVERY.md             # Disaster recovery
│   ├── HARDWARE_KIT.md         # Physical equipment
│   └── FARADAY_ROOM_GUIDE.md   # EMP protection
│
└── output/
    └── logos_graph.gpickle     # Prebuilt network graph
```

---

## The Network

Every verse is a **node**. Cross-references are **edges**.

The Bible is not a flat text - it's a living graph of interconnected truth.

When you study John 3:16, you discover:
- Its connections to Old Testament prophecy
- Its echoes in the epistles
- Its theological family (verses sharing concepts)
- Its linguistic roots (Hebrew/Greek definitions)

*"Scripture interprets Scripture"* - but now you can see it.

---

## Requirements

- Python 3.x
- NetworkX (`pip install networkx`)
- 200MB storage
- Works on: Windows, Mac, Linux, Raspberry Pi, Android (Termux)

---

## For Those Who Find This

If you're reading this after infrastructure has failed:

1. Read `START_HERE.txt`
2. Read `WHY.txt`
3. Follow `docs/INSTALL.md`
4. If data is corrupted, see `docs/RECOVERY.md`
5. For physical setup, see `docs/HARDWARE_KIT.md`

The system is designed to be rebuilt from partial data.

---

## Inheritance

For **Alfred William Weathers** and **Lavender Camille Weathers**.

And for all who seek truth in dark times.

---

## License

Freely given, freely share.

> "And the things that thou hast heard of me among many witnesses, the same commit thou to faithful men, who shall be able to teach others also." - 2 Timothy 2:2

---

## The Vision

> "Write the vision, and make it plain upon tables, that he may run that readeth it." - Habakkuk 2:2

This is the vision, made plain.

---

*"In the beginning was the Word, and the Word was with God, and the Word was God."*
— John 1:1

*"Heaven and earth shall pass away, but my words shall not pass away."*
— Matthew 24:35

---

**Soli Deo Gloria**

Built Thanksgiving 2025 | "until it is all in all" - 1 Corinthians 15:28
