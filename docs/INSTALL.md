# LOGOS ENGINE - Complete Installation Guide

**Assumes nothing. Start here if you have no technical background.**

---

## What You Need

### Minimum Requirements
- A computer (any of these):
  - Windows PC or laptop
  - Mac
  - Linux computer
  - Raspberry Pi
  - Android phone with Termux app
- 200MB free storage
- No internet required (if you have this archive)

### Recommended
- 500MB+ storage
- Keyboard (phone touchscreen works but is slower)

---

## Installation By Platform

Choose your platform below:

---

## WINDOWS

### Step 1: Install Python

1. If you have internet:
   - Go to python.org
   - Click "Download Python 3.x.x"
   - Run the installer
   - **IMPORTANT**: Check "Add Python to PATH" at the bottom of the installer
   - Click "Install Now"

2. If you have no internet:
   - Look for a file called `python-3.x.x.exe` in this archive
   - Run it and follow the same steps above

### Step 2: Open Command Prompt

1. Press Windows key + R
2. Type `cmd` and press Enter
3. A black window will appear - this is where you type commands

### Step 3: Navigate to LOGOS_ENGINE

If LOGOS_ENGINE is on a USB drive (E:), type:
```
E:
cd LOGOS_ENGINE
```

If it's in your Documents folder:
```
cd Documents\LOGOS_ENGINE
```

### Step 4: Install Required Package

```
pip install networkx
```

If no internet, this may already be included. Skip if you get an error.

### Step 5: Test It

```
python logos.py verse "John 3:16"
```

You should see:
```
For God so loved the world, that he gave his only begotten Son, that whosoever
believeth in him should not perish, but have everlasting life.
```

**You're ready. Skip to "Using LOGOS ENGINE" below.**

---

## MAC

### Step 1: Open Terminal

1. Press Command + Space
2. Type "Terminal" and press Enter

### Step 2: Check if Python is installed

```
python3 --version
```

If you see "Python 3.x.x", continue to Step 4.
If not, you need to install Python.

### Step 3: Install Python (if needed)

If you have internet:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

If no internet, look for Python installer in this archive.

### Step 4: Navigate to LOGOS_ENGINE

```
cd /path/to/LOGOS_ENGINE
```

For example, if on a USB drive:
```
cd /Volumes/USB_DRIVE/LOGOS_ENGINE
```

### Step 5: Install Required Package

```
pip3 install networkx
```

### Step 6: Test It

```
python3 logos.py verse "John 3:16"
```

**You're ready. Skip to "Using LOGOS ENGINE" below.**

---

## LINUX

### Step 1: Open Terminal

Usually: Ctrl + Alt + T

### Step 2: Install Python (if needed)

Debian/Ubuntu:
```
sudo apt update
sudo apt install python3 python3-pip
```

Fedora:
```
sudo dnf install python3 python3-pip
```

Arch:
```
sudo pacman -S python python-pip
```

### Step 3: Navigate to LOGOS_ENGINE

```
cd /path/to/LOGOS_ENGINE
```

### Step 4: Install Required Package

```
pip3 install networkx
```

### Step 5: Test It

```
python3 logos.py verse "John 3:16"
```

**You're ready. Skip to "Using LOGOS ENGINE" below.**

---

## RASPBERRY PI

Same as Linux above, but start with:

### Step 1: Flash SD Card

If starting fresh:
1. Download Raspberry Pi Imager (or use pre-flashed SD if included)
2. Flash "Raspberry Pi OS Lite" to SD card
3. Insert SD, connect power, keyboard, monitor

### Step 2: Initial Setup

```
sudo apt update
sudo apt install python3 python3-pip
```

### Step 3: Copy LOGOS_ENGINE

From USB drive:
```
cp -r /media/pi/USB_DRIVE/LOGOS_ENGINE ~/LOGOS_ENGINE
cd ~/LOGOS_ENGINE
```

### Step 4: Install and Test

```
pip3 install networkx
python3 logos.py verse "John 3:16"
```

**You're ready.**

---

## ANDROID (Termux)

### Step 1: Install Termux

If you have internet:
- Install from F-Droid (f-droid.org) - NOT Google Play (outdated)

If no internet:
- Look for `termux.apk` in this archive
- Enable "Install from unknown sources" in Settings
- Install the APK

### Step 2: Open Termux and Setup

```
pkg update
pkg install python
pip install networkx
```

### Step 3: Setup Storage Access

```
termux-setup-storage
```

Grant permission when prompted.

### Step 4: Copy LOGOS_ENGINE

If LOGOS_ENGINE is in your phone's Download folder:
```
cp -r ~/storage/shared/Download/LOGOS_ENGINE ~/LOGOS_ENGINE
cd ~/LOGOS_ENGINE
```

### Step 5: Test It

```
python logos.py verse "John 3:16"
```

**You're ready.**

---

## Using LOGOS ENGINE

### Basic Commands

Get help:
```
python logos.py help
```

Look up a verse:
```
python logos.py verse "Genesis 1:1"
python logos.py verse "John 3:16"
python logos.py verse "Revelation 22:21"
```

Search for a word:
```
python logos.py search "grace"
python logos.py search "faith"
python logos.py search "love"
```

Find three witnesses on a topic:
```
python logos.py witness "salvation"
python logos.py witness "resurrection"
```

### Hebrew/Greek Study

Look up a Strong's number:
```
python logos.py strongs H430    # Hebrew word for "God" (Elohim)
python logos.py strongs G26     # Greek word for "love" (agape)
```

Study a word's Hebrew/Greek roots:
```
python logos.py study "love"
python logos.py study "faith"
```

### Semantic Search (Find by Meaning)

Find verses similar to another verse:
```
python logos.py similar "John 3:16"
python logos.py similar "Romans 8:28"
```

Search by theological meaning:
```
python logos.py meaning "God saves sinners"
python logos.py meaning "eternal life through faith"
```

Search by theological concept:
```
python logos.py concept salvation
python logos.py concept redemption
python logos.py concept grace
```

### Interactive Modes

Start interactive query mode:
```
python logos.py query
```

Start interactive concordance mode:
```
python logos.py concordance
```

Start interactive semantic search:
```
python logos.py semantic
```

### Network Graph Statistics

See how the Scripture network is connected:
```
python logos.py stats
```

---

## Troubleshooting

### "python not found"
Try `python3` instead of `python`:
```
python3 logos.py verse "John 3:16"
```

### "No module named networkx"
Install it:
```
pip install networkx
```
or:
```
pip3 install networkx
```

### "Permission denied"
On Linux/Mac, try:
```
chmod +x logos.py
```

### "File not found"
Make sure you're in the LOGOS_ENGINE directory:
```
cd /path/to/LOGOS_ENGINE
ls
```
You should see `logos.py` in the file list.

### Verse not found
Check the format: `"Book Chapter:Verse"`
- Correct: `"John 3:16"`
- Correct: `"1 Corinthians 13:4"`
- Correct: `"Psalm 23:1"` (not Psalms for single psalm)

### Nothing works
Read RECOVERY.md for how to rebuild from source data.

---

## What's In This Archive

```
LOGOS_ENGINE/
├── START_HERE.txt        # Read this first
├── WHY.txt               # Why this exists (the Gospel)
├── README.md             # Technical overview
├── logos.py              # Main program
├── docs/
│   ├── INSTALL.md        # This file
│   ├── RECOVERY.md       # Rebuild from scratch
│   ├── HARDWARE_KIT.md   # Physical equipment guide
│   └── FARADAY_ROOM_GUIDE.md  # EMP protection
├── src/
│   ├── loader.py         # Data loading
│   ├── graph.py          # Network graph
│   ├── query.py          # Search functions
│   ├── concordance.py    # Hebrew/Greek tools
│   ├── semantic.py       # Meaning-based search
│   └── api.py            # Bible API (if online)
├── data/
│   ├── kjv.json          # Complete KJV Bible (36,586 verses)
│   ├── strongs.json      # Hebrew/Greek definitions
│   ├── cross_refs.json   # Cross-references
│   └── ...               # Additional data files
└── output/
    └── logos_graph.gpickle  # Prebuilt network graph
```

---

## Copying This Archive

### To USB Drive

Windows:
```
xcopy LOGOS_ENGINE E:\LOGOS_ENGINE /E /I
```

Mac/Linux:
```
cp -r LOGOS_ENGINE /Volumes/USB_DRIVE/
```

### To Another Computer

Copy the entire LOGOS_ENGINE folder by any means:
- USB drive
- SD card
- Bluetooth
- Direct cable transfer
- Burn to CD/DVD

The entire archive is self-contained. No internet needed.

---

## Sharing This

"And the things that thou hast heard of me among many witnesses, the same
commit thou to faithful men, who shall be able to teach others also."
  - 2 Timothy 2:2

Copy freely. Share widely. This is meant to spread.

---

## Getting Help

If the original builders are unavailable and you have questions:

1. Read the code - it's written to be understandable
2. Read the Bible - it interprets itself
3. Pray - "If any of you lack wisdom, let him ask of God" (James 1:5)
4. Find other believers - you're not alone

---

*"Write the vision, and make it plain upon tables, that he may run that
readeth it."* - Habakkuk 2:2
