# FILE STRUCTURE GUIDE
## Where Everything Is Located

**A visual guide to help you navigate the LOGOS ENGINE repository.**

---

## 📂 ROOT FOLDER (Main Directory)

When you open the LOGOS_ENGINE folder, you see:

```
LOGOS_ENGINE/
│
├── 📘 DOCUMENTATION (Read These First)
│   ├── INDEX.md                 ← START HERE for navigation
│   ├── GETTING_STARTED.md       ← Setup guide for beginners
│   ├── START_HERE.txt           ← First contact document
│   ├── README.md                ← Technical overview
│   ├── WHY.txt                  ← The Gospel message
│   ├── TROUBLESHOOTING.md       ← Problems and solutions
│   ├── QUICK_REFERENCE.md       ← Print this card
│   ├── THE_JOURNEY.md           ← How it was built
│   ├── FOR_ANNA.md              ← Evangelism guide
│   ├── GOSSIP.md                ← How to share
│   ├── CHANGELOG.md             ← Version history
│   ├── DECEMBER_FOURTH.md       ← Journal entry
│   └── PUSH_INSTRUCTIONS.md     ← Distribution guide
│
├── 🖥️ MAIN PROGRAM
│   └── logos.py                 ← Run this to use LOGOS
│
├── 🛠️ BUILD TOOLS (Advanced)
│   ├── build_strongs.py
│   ├── build_cross_refs.py
│   ├── parse_strongs_xml.py
│   ├── download_apocrypha.py
│   └── resume_apocrypha.py
│
├── 📁 FOLDERS
│   ├── data/                    ← All Bible data
│   ├── src/                     ← Source code
│   ├── docs/                    ← Additional documentation
│   ├── neural/                  ← Neural network demos
│   └── output/                  ← Generated files
```

---

## 📁 DATA FOLDER

**Location:** `data/`  
**Purpose:** All Bible text and reference data

```
data/
├── kjv.json                     ← Complete KJV Bible (36,586 verses)
├── strongs.json                 ← Hebrew/Greek definitions (14,180)
├── cross_refs.json              ← Cross-references (2.5M+ connections)
├── strongs_complete.json        ← Complete Strong's data
│
├── APOCRYPHA (1611 KJV)
│   ├── apocrypha_1_esdras.json
│   ├── apocrypha_1_maccabees.json
│   ├── apocrypha_2_esdras.json
│   ├── apocrypha_2_maccabees.json
│   ├── apocrypha_baruch.json
│   ├── apocrypha_bel_and_the_dragon.json
│   ├── apocrypha_esther_greek.json
│   ├── apocrypha_judith.json
│   ├── apocrypha_letter_of_jeremiah.json
│   ├── apocrypha_prayer_of_azariah.json
│   ├── apocrypha_prayer_of_manasseh.json
│   ├── apocrypha_sirach.json
│   ├── apocrypha_structure.json
│   ├── apocrypha_susanna.json
│   ├── apocrypha_tobit.json
│   └── apocrypha_wisdom_of_solomon.json
│
├── SOURCE DATA (XML)
│   ├── HebrewStrong.xml         ← Hebrew Strong's source
│   └── strongsgreek.xml         ← Greek Strong's source
│
└── cache/                       ← Temporary cache files
```

**All data files are readable JSON/XML text!**  
Open with any text editor to view raw Bible data.

---

## 💻 SRC FOLDER (Source Code)

**Location:** `src/`  
**Purpose:** Python modules that power LOGOS

```
src/
├── __init__.py                  ← Package initialization
├── loader.py                    ← Load Bible data from JSON
├── graph.py                     ← Build Scripture network graph
├── query.py                     ← Search and query functions
├── concordance.py               ← Hebrew/Greek word study
├── semantic.py                  ← Meaning-based search
├── visualize.py                 ← Network visualization
├── image.py                     ← Verse image generation
├── chain.py                     ← Network traversal
├── fuzzy.py                     ← Fuzzy search
├── integrity.py                 ← Data verification
├── api.py                       ← Bible API interface
├── daily.py                     ← Daily verse
├── pdf.py                       ← PDF generation
├── qr.py                        ← QR code generation
└── voice.py                     ← Voice/audio features
```

**All code is Python and well-commented!**

---

## 📚 DOCS FOLDER (Additional Documentation)

**Location:** `docs/`  
**Purpose:** Detailed guides and logs

```
docs/
├── INSTALL.md                   ← Complete installation guide
├── RECOVERY.md                  ← Disaster recovery procedures
├── HARDWARE_KIT.md              ← Equipment recommendations
├── FARADAY_ROOM_GUIDE.md        ← EMP protection guide
│
├── PERSONAL
│   ├── TO_MY_CAMILLES.md        ← Personal letter
│   └── COMMISSIONING_LOG_NOV30_2025.md
│
└── BUILD LOGS
    ├── SESSION_LOG_NOV26_2025.md
    ├── SESSION_LOG_NOV27_2025.md
    └── SESSION_LOG_NOV29_2025.md
```

---

## 🧠 NEURAL FOLDER (Demos)

**Location:** `neural/`  
**Purpose:** Neural network demonstrations

```
neural/
├── baby_brain.py                ← Basic neural network demo
└── sentinel_brain.py            ← SENTINEL architecture demo
```

---

## 📤 OUTPUT FOLDER (Generated Files)

**Location:** `output/`  
**Purpose:** Files created when you run LOGOS

```
output/
├── logos_graph.gpickle          ← Prebuilt network graph
├── *.dot                        ← Graphviz source files
└── *.png                        ← Generated images
```

**Note:** This folder is created automatically if it doesn't exist.

---

## 🎯 QUICK NAVIGATION

### "Where is the Bible text?"
→ `data/kjv.json`

### "Where are the Hebrew/Greek definitions?"
→ `data/strongs.json`

### "Where is the main program?"
→ `logos.py` (in root folder)

### "Where are the installation instructions?"
→ `GETTING_STARTED.md` (beginners) or `docs/INSTALL.md` (detailed)

### "Where do I find help?"
→ `TROUBLESHOOTING.md`

### "Where is everything explained?"
→ `INDEX.md` (complete navigation)

### "Where is the Gospel message?"
→ `WHY.txt`

### "How do I rebuild if data is lost?"
→ `docs/RECOVERY.md`

---

## 📖 READING THE DATA FILES

All data is stored in **JSON format** - human-readable text.

### To View Bible Verses:
1. Open `data/kjv.json` in any text editor
2. Each verse is structured like:
```json
{
  "book": "Genesis",
  "chapter": 1,
  "verse": 1,
  "text": "In the beginning God created the heaven and the earth."
}
```

### To View Strong's Definitions:
1. Open `data/strongs.json` in any text editor
2. Each entry is structured like:
```json
{
  "number": "H430",
  "word": "אֱלֹהִים",
  "transliteration": "elohiym",
  "definition": "gods, God, judges, angels..."
}
```

**You don't need special software - just a text editor!**

---

## 🔍 FINDING SPECIFIC FILES

### Documentation Files
**All in root folder**, except:
- Detailed guides → `docs/` folder
- Session logs → `docs/` folder

### Data Files
**All in `data/` folder**

### Program Files
- Main program → `logos.py` (root)
- Source code → `src/` folder
- Build scripts → Root folder (`build_*.py`)

### Generated Files
**All in `output/` folder**

---

## 📏 FILE SIZES (Approximate)

| File | Size | Notes |
|------|------|-------|
| `data/kjv.json` | ~4.5 MB | All KJV verses |
| `data/strongs.json` | ~2 MB | Definitions |
| `data/cross_refs.json` | ~40 MB | All cross-refs |
| `output/logos_graph.gpickle` | ~80 MB | Network graph |
| **Total repository** | ~200 MB | Complete system |

---

## 🔓 ACCESSIBILITY NOTES

### All Files Are Accessible

✅ **No hidden files** (except system files like `.git`)  
✅ **No encrypted files**  
✅ **No password-protected files**  
✅ **No proprietary formats**  
✅ **Everything is readable text** (JSON, XML, Python, Markdown)

### You Can:
- Open any file with a text editor
- Copy any file
- Modify any file
- Move files around
- Share everything

### Standard Permissions:
All files have standard read/write permissions:
- `-rw-rw-r--` (user can read/write, others can read)
- This is normal and means files are accessible

---

## 💡 TIPS FOR NAVIGATING

1. **Start at the top** - Read `INDEX.md` first
2. **Data is separate from code** - Data in `data/`, code in `src/`
3. **Documentation is everywhere** - Root folder AND `docs/` folder
4. **Main program is simple** - Just `logos.py`
5. **Everything is labeled** - File names are descriptive

---

## 🗺️ NAVIGATION FLOW

```
New User Journey:
1. INDEX.md (or START_HERE.txt)
   ↓
2. WHY.txt (understand purpose)
   ↓
3. GETTING_STARTED.md (setup)
   ↓
4. logos.py (run program)
   ↓
5. TROUBLESHOOTING.md (if needed)

Developer Journey:
1. README.md (overview)
   ↓
2. THE_JOURNEY.md (architecture)
   ↓
3. src/ folder (source code)
   ↓
4. data/ folder (data structure)
   ↓
5. docs/RECOVERY.md (rebuild procedures)
```

---

## 📞 STILL CAN'T FIND SOMETHING?

1. **Check INDEX.md** - Complete navigation
2. **Use search** - Most text editors can search across files
3. **Look in docs/** - Detailed guides are there
4. **Check TROUBLESHOOTING.md** - Common questions answered

---

## 📂 SUMMARY

| What | Where |
|------|-------|
| Navigation hub | `INDEX.md` |
| Setup guide | `GETTING_STARTED.md` |
| Main program | `logos.py` |
| Bible data | `data/kjv.json` |
| Definitions | `data/strongs.json` |
| Source code | `src/` folder |
| Documentation | Root + `docs/` |
| Troubleshooting | `TROUBLESHOOTING.md` |
| Gospel message | `WHY.txt` |

---

*"Write the vision, and make it plain upon tables, that he may run that readeth it."*  
— Habakkuk 2:2

**Everything is organized. Everything is accessible. Everything is documented.**

---

**LOGOS ENGINE** | File Structure Guide  
Built Thanksgiving 2025 | **Soli Deo Gloria**
