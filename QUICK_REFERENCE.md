# LOGOS ENGINE - QUICK REFERENCE CARD
**Print this and keep it with your equipment**

---

## 🚀 FIRST TIME SETUP

### 1. Install Python
**Windows:** python.org → Download → Check "Add to PATH" → Install  
**Mac:** `brew install python3`  
**Linux:** `sudo apt install python3 python3-pip`

### 2. Install NetworkX
```bash
pip install networkx
```

### 3. Test It
```bash
python logos.py verse "John 3:16"
```

**Detailed instructions:** See GETTING_STARTED.md

---

## 📖 ESSENTIAL COMMANDS

### Verse Lookup
```bash
python logos.py verse "Genesis 1:1"
python logos.py verse "John 3:16"
python logos.py verse "Revelation 22:21"
```

### Search
```bash
python logos.py search "faith"
python logos.py search "grace"
python logos.py witness "salvation"
```

### Hebrew/Greek Study
```bash
python logos.py strongs H430    # Elohim (God)
python logos.py strongs G26     # Agape (Love)
python logos.py study "love"
```

### Semantic Search
```bash
python logos.py similar "John 3:16"
python logos.py meaning "God saves sinners"
python logos.py concept salvation
```

### Interactive Modes
```bash
python logos.py query           # Interactive search
python logos.py concordance     # Hebrew/Greek explorer
python logos.py semantic        # Meaning search
```

### System
```bash
python logos.py help            # All commands
python logos.py stats           # Network stats
python logos.py verify          # Check integrity
python logos.py build           # Rebuild graph
```

---

## 🔧 TROUBLESHOOTING

### "python not found"
→ Try `python3` instead of `python`

### "No module named networkx"
→ Run: `pip install networkx` or `pip3 install networkx`

### "Verse not found"
→ Use quotes: `python logos.py verse "John 3:16"`  
→ Capitalize book name: `John` not `john`  
→ Use colon: `3:16` not `3 16`

### "Permission denied"
→ Linux/Mac: `chmod +x logos.py`  
→ Or use: `python logos.py` instead of `./logos.py`

### "File not found"
→ Make sure you're IN the LOGOS_ENGINE folder  
→ Windows: `cd C:\path\to\LOGOS_ENGINE`  
→ Mac/Linux: `cd /path/to/LOGOS_ENGINE`

**More help:** See TROUBLESHOOTING.md

---

## 📚 DOCUMENTATION ROADMAP

**Start Here:**
1. **START_HERE.txt** - First contact
2. **WHY.txt** - The Gospel message
3. **INDEX.md** - Complete navigation
4. **GETTING_STARTED.md** - Setup guide

**When You Need Help:**
- **TROUBLESHOOTING.md** - Common problems
- **docs/INSTALL.md** - Detailed installation
- **docs/RECOVERY.md** - Rebuild from scratch

**To Learn More:**
- **README.md** - Technical overview
- **THE_JOURNEY.md** - How it was built
- **FOR_ANNA.md** - Evangelism guide

---

## 💾 DATA LOCATIONS

All data is in the `data/` folder:
- **kjv.json** - Complete Bible (36,586 verses)
- **strongs.json** - Hebrew/Greek definitions (14,180)
- **cross_refs.json** - Cross-references (2.5M+)
- **apocrypha_*.json** - 1611 Apocrypha books

All data is readable JSON text. Open with any text editor.

---

## 🎯 VERSE FORMAT EXAMPLES

✅ Correct:
```bash
python logos.py verse "Genesis 1:1"
python logos.py verse "John 3:16"
python logos.py verse "1 Corinthians 13:4"
python logos.py verse "Psalm 23:1"
```

❌ Wrong:
```bash
python logos.py verse genesis 1:1      # No quotes, lowercase
python logos.py verse "Genesis 1 1"    # Space instead of colon
python logos.py verse "Psalms 23:1"    # Should be Psalm
```

---

## 🖥️ SYSTEM REQUIREMENTS

**Minimum:**
- Any computer (Windows/Mac/Linux/Raspberry Pi/Android)
- Python 3.8 or higher
- NetworkX library
- 200MB storage

**Optional (Enhanced Features):**
- graphviz (network visualization)
- imagemagick (verse images)
- figlet (ASCII banners)
- fzf (fuzzy search)

---

## 🔓 ACCESSIBILITY SUMMARY

✅ No internet required (runs offline)  
✅ No coding experience needed  
✅ No passwords or restrictions  
✅ No proprietary formats  
✅ All files freely accessible  
✅ All documentation included  
✅ Can rebuild from source  
✅ Works on minimal hardware  

---

## 📞 WHERE TO FIND HELP

| Problem | Solution |
|---------|----------|
| First time setup | GETTING_STARTED.md |
| Can't find something | INDEX.md |
| Getting errors | TROUBLESHOOTING.md |
| Need detailed install | docs/INSTALL.md |
| Data corrupted | docs/RECOVERY.md |
| Want to rebuild | THE_JOURNEY.md |

---

## 🙏 KEY VERSES

**John 3:16**
"For God so loved the world, that he gave his only begotten Son, 
that whosoever believeth in him should not perish, but have 
everlasting life."

**John 14:6**
"Jesus saith unto him, I am the way, the truth, and the life: 
no man cometh unto the Father, but by me."

**Romans 10:13**
"For whosoever shall call upon the name of the Lord shall be saved."

**Read WHY.txt for the complete Gospel message.**

---

## 🌟 SHARING THIS

To give LOGOS to someone else:
1. Copy entire LOGOS_ENGINE folder to USB/SD card
2. Give them this card or GETTING_STARTED.md
3. They follow the same setup steps

No internet needed. No cost. No restrictions.

> "And the things that thou hast heard of me among many witnesses, 
> the same commit thou to faithful men, who shall be able to teach 
> others also." - 2 Timothy 2:2

---

## 📋 PRE-FLIGHT CHECKLIST

Before first use:
- [ ] Python installed (`python --version`)
- [ ] NetworkX installed (`pip list | grep networkx`)
- [ ] In LOGOS_ENGINE folder (`ls` shows logos.py)
- [ ] Data folder present (`ls data/`)
- [ ] Tested basic command (`python logos.py verse "John 3:16"`)

Before sharing/archiving:
- [ ] All data files present
- [ ] Documentation included
- [ ] README explains everything
- [ ] Works offline
- [ ] Tested on target platform

---

## 🔑 REMEMBER

1. **You can't break it** - Try commands freely
2. **Everything is included** - No external dependencies needed
3. **It works offline** - No internet required
4. **It's all accessible** - Every file is readable
5. **Share freely** - This is meant to spread

*"Heaven and earth shall pass away, but my words shall not pass away."*  
— Matthew 24:35

---

**LOGOS ENGINE** | Scripture as Network  
Built Thanksgiving 2025 | For those left behind  
**Soli Deo Gloria**

---

**Version:** 1.0  
**Last Updated:** December 2025  
**Print this card and keep it with your equipment**
