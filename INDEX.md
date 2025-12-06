# LOGOS ENGINE - NAVIGATION INDEX
## Your Guide to Everything in This Repository

**Welcome!** This document helps you find everything you need, organized by purpose.

---

## 🚀 **START HERE (First Time?)**

| File | What It Is | Why Read It |
|------|-----------|-------------|
| **[START_HERE.txt](START_HERE.txt)** | First contact document | Read this FIRST if you've never used this repository |
| **[WHY.txt](WHY.txt)** | The Gospel message | Understand why this exists |
| **[docs/INSTALL.md](docs/INSTALL.md)** | Complete setup guide | Step-by-step installation for ANY platform |

**Quick Start:** Read START_HERE.txt → Follow docs/INSTALL.md → Run your first command

---

## 📖 **WHAT IS THIS?**

This repository contains:
- Complete King James Bible (KJV) with 1611 Apocrypha
- 36,586 verses
- 14,180 Hebrew and Greek word definitions
- 2.5+ million cross-reference connections
- Runs completely offline, no internet needed

**Purpose:** A self-contained Scripture study system designed to survive and serve when infrastructure fails.

---

## 📚 **ALL DOCUMENTATION**

### Essential Documents (Read These)

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Technical overview and commands reference |
| [START_HERE.txt](START_HERE.txt) | First contact - what this is and how to begin |
| [WHY.txt](WHY.txt) | The Gospel and why this exists |
| [docs/INSTALL.md](docs/INSTALL.md) | Complete installation guide for all platforms |

### User Guides

| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Simplified quick start guide (no tech experience needed) |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common problems and solutions |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card (print this!) |
| [FILE_STRUCTURE.md](FILE_STRUCTURE.md) | Visual guide to where everything is located |
| [FOR_ANNA.md](FOR_ANNA.md) | Scripture guide for conversations with non-believers |
| [GOSSIP.md](GOSSIP.md) | How to share this with others |

### Technical Documentation

| Document | Purpose |
|----------|---------|
| [THE_JOURNEY.md](THE_JOURNEY.md) | How this was built (so you can rebuild it) |
| [docs/RECOVERY.md](docs/RECOVERY.md) | Disaster recovery - rebuild from scratch |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |

### Preparation & Survival

| Document | Purpose |
|----------|---------|
| [docs/HARDWARE_KIT.md](docs/HARDWARE_KIT.md) | Recommended physical equipment |
| [docs/FARADAY_ROOM_GUIDE.md](docs/FARADAY_ROOM_GUIDE.md) | EMP protection guide |
| [PUSH_INSTRUCTIONS.md](PUSH_INSTRUCTIONS.md) | How to update/distribute this repository |

### Personal & Historical

| Document | Purpose |
|----------|---------|
| [DECEMBER_FOURTH.md](DECEMBER_FOURTH.md) | Development journal entry |
| [docs/TO_MY_CAMILLES.md](docs/TO_MY_CAMILLES.md) | Personal letter from creator |
| [docs/SESSION_LOG_*.md](docs/) | Development session logs |

---

## 💾 **DATA FILES**

All Scripture and reference data is in the `data/` folder:

| File | Content |
|------|---------|
| `data/kjv.json` | Complete KJV Bible (36,586 verses) |
| `data/strongs.json` | Hebrew & Greek word definitions (14,180 entries) |
| `data/cross_refs.json` | Cross-reference connections (2.5M+ links) |
| `data/apocrypha_*.json` | 1611 Apocrypha books |
| `data/HebrewStrong.xml` | Source Hebrew Strong's data |
| `data/strongsgreek.xml` | Source Greek Strong's data |

**All data files are accessible and readable.** They're in JSON format (human-readable text).

---

## 🛠️ **TOOLS & SCRIPTS**

### Main Program

| File | What It Does |
|------|-------------|
| `logos.py` | Main command-line interface - run this to use LOGOS |

Run `python logos.py help` to see all available commands.

### Build Scripts (Advanced)

| File | Purpose |
|------|---------|
| `build_strongs.py` | Rebuild Strong's concordance from XML |
| `build_cross_refs.py` | Rebuild cross-reference network |
| `parse_strongs_xml.py` | Parse Strong's XML source data |
| `download_apocrypha.py` | Download Apocrypha books |
| `resume_apocrypha.py` | Resume interrupted Apocrypha download |

### Source Code (Python Modules)

Located in `src/` folder:

| Module | Function |
|--------|----------|
| `loader.py` | Load Bible data from JSON files |
| `graph.py` | Build Scripture network graph |
| `query.py` | Search and query functions |
| `concordance.py` | Hebrew/Greek word study tools |
| `semantic.py` | Meaning-based search |
| `visualize.py` | Network visualization (requires graphviz) |
| `image.py` | Generate verse images (requires imagemagick) |
| `chain.py` | Network traversal and pathfinding |
| `fuzzy.py` | Fuzzy search integration (requires fzf) |
| `integrity.py` | Data verification and integrity checks |
| `api.py` | Bible API interface (optional, for online access) |

### Neural Network Demos

Located in `neural/` folder:
- `baby_brain.py` - Neural network demonstration
- `sentinel_brain.py` - SENTINEL architecture demo

---

## 🎯 **HOW TO USE THIS**

### For Complete Beginners

1. **Read:** [START_HERE.txt](START_HERE.txt)
2. **Read:** [WHY.txt](WHY.txt)
3. **Follow:** [GETTING_STARTED.md](GETTING_STARTED.md)
4. **Install:** Follow [docs/INSTALL.md](docs/INSTALL.md) for your device
5. **Try:** Run `python logos.py verse "John 3:16"`

### For People with Some Computer Experience

1. **Quick overview:** [README.md](README.md)
2. **Installation:** [docs/INSTALL.md](docs/INSTALL.md)
3. **Test:** `python logos.py help`
4. **Explore:** Try different commands

### For Developers

1. Read [THE_JOURNEY.md](THE_JOURNEY.md) to understand the architecture
2. Check source code in `src/` folder
3. Review build scripts to understand data processing
4. See [docs/RECOVERY.md](docs/RECOVERY.md) for rebuild procedures

---

## 📁 **COMPLETE FILE STRUCTURE**

```
LOGOS_ENGINE/
│
├── INDEX.md                    ← YOU ARE HERE
├── GETTING_STARTED.md          ← Simplified quick start
├── TROUBLESHOOTING.md          ← Common problems & solutions
├── README.md                   ← Technical overview
├── START_HERE.txt              ← First contact document
├── WHY.txt                     ← The Gospel message
├── CHANGELOG.md                ← Version history
├── GOSSIP.md                   ← How to share this
├── FOR_ANNA.md                 ← Scripture conversation guide
├── THE_JOURNEY.md              ← How this was built
├── DECEMBER_FOURTH.md          ← Development journal
├── PUSH_INSTRUCTIONS.md        ← Distribution guide
│
├── logos.py                    ← MAIN PROGRAM - RUN THIS
│
├── build_strongs.py            ← Rebuild Strong's data
├── build_cross_refs.py         ← Rebuild cross-references
├── parse_strongs_xml.py        ← Parse XML sources
├── download_apocrypha.py       ← Download Apocrypha
├── resume_apocrypha.py         ← Resume downloads
│
├── data/                       ← ALL BIBLE DATA (accessible)
│   ├── kjv.json                   • Complete KJV (36,586 verses)
│   ├── strongs.json               • Hebrew/Greek definitions
│   ├── cross_refs.json            • Cross-references
│   ├── apocrypha_*.json           • Apocrypha books
│   ├── HebrewStrong.xml           • Hebrew source data
│   └── strongsgreek.xml           • Greek source data
│
├── src/                        ← SOURCE CODE
│   ├── loader.py                  • Data loading
│   ├── graph.py                   • Network graph builder
│   ├── query.py                   • Search functions
│   ├── concordance.py             • Hebrew/Greek tools
│   ├── semantic.py                • Meaning-based search
│   ├── visualize.py               • Network visualization
│   ├── image.py                   • Verse image generation
│   ├── chain.py                   • Network traversal
│   ├── fuzzy.py                   • Fuzzy search
│   ├── integrity.py               • Data verification
│   └── api.py                     • Bible API interface
│
├── docs/                       ← DOCUMENTATION
│   ├── INSTALL.md                 • Complete setup guide
│   ├── RECOVERY.md                • Disaster recovery
│   ├── HARDWARE_KIT.md            • Equipment recommendations
│   ├── FARADAY_ROOM_GUIDE.md      • EMP protection
│   ├── TO_MY_CAMILLES.md          • Personal letter
│   └── SESSION_LOG_*.md           • Development logs
│
├── neural/                     ← NEURAL NETWORK DEMOS
│   ├── baby_brain.py              • Basic neural network
│   └── sentinel_brain.py          • SENTINEL architecture
│
└── output/                     ← GENERATED FILES
    ├── logos_graph.gpickle        • Prebuilt network graph
    ├── *.dot                      • Graphviz source files
    └── *.png                      • Generated images
```

---

## ❓ **NEED HELP?**

### I don't know where to start
→ Read [START_HERE.txt](START_HERE.txt)

### I want to install this on my computer
→ Follow [docs/INSTALL.md](docs/INSTALL.md)

### I'm getting errors
→ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### I want to understand why this exists
→ Read [WHY.txt](WHY.txt)

### I want to share this with others
→ Read [GOSSIP.md](GOSSIP.md)

### I need to rebuild everything from scratch
→ Follow [docs/RECOVERY.md](docs/RECOVERY.md)

### I want to see all available commands
→ Run `python logos.py help`

### I have no technical experience at all
→ Follow [GETTING_STARTED.md](GETTING_STARTED.md)

---

## 🔓 **ACCESSIBILITY**

**Everything in this repository is accessible and freely available:**

✅ All documentation files are readable text
✅ All data files are accessible JSON/XML format
✅ All source code is open and readable
✅ No passwords or restrictions
✅ No hidden files (except system files like .git)
✅ No proprietary formats
✅ Works offline - no internet required
✅ Designed for people with minimal technical experience

**You can:**
- Read any file
- Copy any file
- Modify any file
- Share everything freely
- Rebuild everything from source data

---

## 📜 **LICENSE**

Freely given, freely share.

> "And the things that thou hast heard of me among many witnesses, the same commit thou to faithful men, who shall be able to teach others also." - 2 Timothy 2:2

---

## 🎯 **QUICK REFERENCE**

### Most Important Files (Start Here)
1. [START_HERE.txt](START_HERE.txt)
2. [WHY.txt](WHY.txt)
3. [docs/INSTALL.md](docs/INSTALL.md)
4. [GETTING_STARTED.md](GETTING_STARTED.md)

### Most Useful Commands
```bash
python logos.py help                    # Show all commands
python logos.py verse "John 3:16"       # Look up a verse
python logos.py search "faith"          # Search for a word
python logos.py similar "John 3:16"     # Find similar verses
python logos.py strongs H430            # Hebrew/Greek study
```

### Where to Find Everything
- **Bible data:** `data/` folder
- **Documentation:** Root folder + `docs/` folder  
- **Source code:** `src/` folder
- **Main program:** `logos.py` (root folder)

---

*"Write the vision, and make it plain upon tables, that he may run that readeth it."* - Habakkuk 2:2

**This index makes the vision plain.**

---

**Built:** Thanksgiving 2025 | **For:** Those left behind | **Soli Deo Gloria**
