# TROUBLESHOOTING GUIDE
## Common Problems and Solutions

**Having trouble? Start here.**

---

## 🔍 QUICK DIAGNOSIS

### 1. Can't find Python?
→ [Python Not Found](#python-not-found)

### 2. Can't install networkx?
→ [NetworkX Installation Issues](#networkx-installation-issues)

### 3. Can't find files?
→ [File Not Found Errors](#file-not-found-errors)

### 4. Verse lookups not working?
→ [Verse Format Problems](#verse-format-problems)

### 5. Permission errors?
→ [Permission Denied](#permission-denied)

### 6. Graph not building?
→ [Graph Build Issues](#graph-build-issues)

### 7. Commands don't work?
→ [Command Not Working](#command-not-working)

### 8. Data seems corrupted?
→ [Data Corruption](#data-corruption)

---

## 🐍 PYTHON NOT FOUND

### Problem:
When you type `python` you get:
```
'python' is not recognized as an internal or external command
```
or
```
python: command not found
```

### Solutions:

#### Solution 1: Try python3 instead
Many systems use `python3` instead of `python`:
```bash
python3 logos.py verse "John 3:16"
```

#### Solution 2: Python not installed
**Windows:**
1. Go to python.org
2. Download Python 3.x
3. Run installer
4. **CHECK "Add Python to PATH"**
5. Click "Install Now"

**Mac:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Solution 3: PATH not set (Windows)
1. Search for "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Click "Edit"
5. Click "New"
6. Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X`
7. Click "OK" on all windows
8. Close and reopen Command Prompt

---

## 📦 NETWORKX INSTALLATION ISSUES

### Problem:
```
No module named 'networkx'
```

### Solutions:

#### Solution 1: Install with pip
```bash
pip install networkx
```

If that doesn't work, try:
```bash
pip3 install networkx
```

#### Solution 2: Install with user flag
```bash
pip install --user networkx
```

#### Solution 3: Use Python module command
```bash
python -m pip install networkx
```
or
```bash
python3 -m pip install networkx
```

#### Solution 4: Upgrade pip first
```bash
python -m pip install --upgrade pip
pip install networkx
```

#### Solution 5: No internet access
If you have no internet:
1. On a computer WITH internet, download networkx:
   ```bash
   pip download networkx
   ```
2. Copy the downloaded `.whl` file to your offline computer
3. Install from the file:
   ```bash
   pip install networkx-3.x-py3-none-any.whl
   ```

---

## 📁 FILE NOT FOUND ERRORS

### Problem:
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/kjv.json'
```

### Solutions:

#### Solution 1: Wrong directory
Make sure you're IN the LOGOS_ENGINE folder:

**Windows:**
```bash
cd C:\path\to\LOGOS_ENGINE
dir
```
You should see `logos.py` in the list.

**Mac/Linux:**
```bash
cd /path/to/LOGOS_ENGINE
ls
```
You should see `logos.py` in the list.

#### Solution 2: Verify data folder exists
```bash
# Windows
dir data

# Mac/Linux
ls data/
```

You should see files like:
- kjv.json
- strongs.json
- cross_refs.json

#### Solution 3: Files missing - redownload
If data files are missing:
1. Download the repository again from GitHub
2. Make sure to extract ALL files from the ZIP
3. Don't just copy logos.py - copy the ENTIRE folder

---

## 📖 VERSE FORMAT PROBLEMS

### Problem:
```
Verse not found: john 3 16
```

### Solutions:

#### Correct Format:
```bash
python logos.py verse "John 3:16"
```

#### Important Rules:
1. **Use quotes** around the verse reference
2. **Capitalize** the book name: `John` not `john`
3. **Use colon** between chapter and verse: `3:16` not `3 16`
4. **Book names:**
   - Use `Psalm` not `Psalms` for single psalm
   - Use `1 Corinthians` not `First Corinthians`
   - Use `Song of Solomon` not `Song of Songs`

#### Examples:
```bash
✅ python logos.py verse "Genesis 1:1"
✅ python logos.py verse "1 Corinthians 13:4"
✅ python logos.py verse "Psalm 23:1"
✅ python logos.py verse "Revelation 22:21"

❌ python logos.py verse genesis 1:1       (no quotes, lowercase)
❌ python logos.py verse "Genesis 1 1"     (space instead of colon)
❌ python logos.py verse "Psalms 23:1"     (should be Psalm)
```

---

## 🔒 PERMISSION DENIED

### Problem:
```
PermissionError: [Errno 13] Permission denied
```

### Solutions:

#### Solution 1: Make script executable (Linux/Mac)
```bash
chmod +x logos.py
```

#### Solution 2: Run with Python explicitly
Instead of:
```bash
./logos.py verse "John 3:16"
```

Use:
```bash
python logos.py verse "John 3:16"
```

#### Solution 3: Output folder permissions
If error is about output folder:
```bash
# Linux/Mac
mkdir -p output
chmod 755 output

# Windows
mkdir output
```

#### Solution 4: Running on USB drive (Windows)
If running from USB and getting permission errors:
1. Copy entire LOGOS_ENGINE folder to your hard drive
2. Try running from there instead

---

## 🕸️ GRAPH BUILD ISSUES

### Problem:
```
Error building graph
```
or graph keeps rebuilding every time.

### Solutions:

#### Solution 1: Clear and rebuild
```bash
# Remove old graph
# Windows
del output\logos_graph.gpickle

# Mac/Linux
rm output/logos_graph.gpickle

# Rebuild
python logos.py build
```

#### Solution 2: Verify data files
```bash
python logos.py verify
```

This checks if all data files are intact.

#### Solution 3: Check disk space
Make sure you have at least 500MB free space.

**Windows:**
```bash
wmic logicaldisk get size,freespace,caption
```

**Mac/Linux:**
```bash
df -h
```

#### Solution 4: Memory issues
If your computer has limited RAM (less than 2GB):
1. Close other programs
2. Try building graph:
   ```bash
   python logos.py build
   ```
3. Be patient - it may take several minutes

---

## ⚙️ COMMAND NOT WORKING

### Problem:
Command gives unexpected results or errors.

### Solutions:

#### Solution 1: Check command syntax
```bash
python logos.py help
```
This shows all available commands with correct syntax.

#### Solution 2: Check Python version
```bash
python --version
```
or
```bash
python3 --version
```

Need Python 3.8 or higher. If you have Python 2.x:
- Install Python 3.x
- Use `python3` instead of `python`

#### Solution 3: Update networkx
```bash
pip install --upgrade networkx
```

#### Solution 4: Try in interactive mode
Instead of:
```bash
python logos.py search "grace"
```

Try:
```bash
python logos.py query
```
Then type your search when prompted.

---

## 💾 DATA CORRUPTION

### Problem:
Data files seem corrupted or missing.

### Solutions:

#### Solution 1: Verify integrity
```bash
python logos.py verify
```

This checks all data files for corruption.

#### Solution 2: Diagnose specific file
```bash
python logos.py diagnose data/kjv.json
```

#### Solution 3: Redownload repository
1. Backup any custom changes
2. Download fresh copy from GitHub
3. Extract all files
4. Try again

#### Solution 4: Rebuild from source
If you have the XML source files:
```bash
python build_strongs.py
python build_cross_refs.py
python logos.py build
```

See `docs/RECOVERY.md` for complete rebuild instructions.

---

## 🖥️ PLATFORM-SPECIFIC ISSUES

### WINDOWS

#### Issue: Windows Defender blocking
**Solution:**
1. Add LOGOS_ENGINE folder to exclusions
2. Windows Security → Virus & threat protection → Manage settings
3. Exclusions → Add an exclusion → Folder
4. Select LOGOS_ENGINE folder

#### Issue: Long path names
**Solution:**
Move LOGOS_ENGINE closer to root:
```bash
C:\LOGOS_ENGINE
```
instead of:
```bash
C:\Users\Name\Documents\Projects\Bible\LOGOS_ENGINE
```

### MAC

#### Issue: "malicious software" warning
**Solution:**
1. System Preferences → Security & Privacy
2. Click "Allow Anyway" for logos.py
3. Or right-click logos.py → Open

#### Issue: Command not found after installing Python
**Solution:**
Add to PATH in `.bash_profile` or `.zshrc`:
```bash
export PATH="/usr/local/bin:$PATH"
```

### LINUX

#### Issue: pip not found
**Solution:**
```bash
sudo apt install python3-pip  # Ubuntu/Debian
sudo dnf install python3-pip  # Fedora
sudo pacman -S python-pip     # Arch
```

### ANDROID (Termux)

#### Issue: Storage permission denied
**Solution:**
```bash
termux-setup-storage
```
Allow when phone prompts.

#### Issue: Package not found
**Solution:**
Update repositories:
```bash
pkg update
pkg upgrade
```

---

## 🔧 ADVANCED TROUBLESHOOTING

### Enable Debug Mode

Add `--debug` to any command:
```bash
python logos.py --debug verse "John 3:16"
```

### Check Python environment
```bash
python -m pip list
```
Look for `networkx` in the list.

### Verify file integrity manually

Check if data files are valid JSON:

**Windows:**
```bash
type data\kjv.json | findstr "{"
```

**Mac/Linux:**
```bash
head data/kjv.json
```

Should show valid JSON starting with `{` or `[`.

---

## 🆘 STILL STUCK?

### Self-Help Resources

1. **Read the code** - It's well-commented:
   ```bash
   # Windows
   type logos.py
   
   # Mac/Linux  
   less logos.py
   ```

2. **Check session logs** - See how it was built:
   - `docs/SESSION_LOG_NOV26_2025.md`
   - `docs/SESSION_LOG_NOV27_2025.md`
   - `docs/SESSION_LOG_NOV29_2025.md`

3. **Recovery documentation** - `docs/RECOVERY.md`

4. **Build logs** - Check `THE_JOURNEY.md` for architecture

### Systematic Approach

1. **Isolate the problem**
   - Does Python work? → `python --version`
   - Does networkx work? → `python -c "import networkx"`
   - Are files present? → `ls data/`
   - Is graph built? → `ls output/`

2. **Test incrementally**
   - Start with simplest command: `python logos.py help`
   - Then try: `python logos.py stats`
   - Then try: `python logos.py verse "John 3:16"`

3. **Check assumptions**
   - Am I in the right folder?
   - Did I extract ALL files?
   - Is Python 3.x installed?
   - Do I have internet (if needed)?

---

## 📋 DIAGNOSTIC CHECKLIST

Run through this list:

- [ ] Python installed? (`python --version` or `python3 --version`)
- [ ] NetworkX installed? (`pip list | grep networkx`)
- [ ] In LOGOS_ENGINE folder? (`ls` shows logos.py)
- [ ] Data folder exists? (`ls data/`)
- [ ] KJV data present? (`ls data/kjv.json`)
- [ ] Output folder exists? (`mkdir output` if not)
- [ ] Sufficient disk space? (Need 500MB+)
- [ ] Correct command syntax? (`python logos.py help`)
- [ ] Using quotes around verse references?
- [ ] Using correct book names?

---

## 💡 PREVENTION TIPS

1. **Always use quotes** for verse references
2. **Always specify full path** if running from outside LOGOS_ENGINE
3. **Keep backup** of working data folder
4. **Document custom changes** you make
5. **Test after any changes** with `python logos.py verse "John 3:16"`

---

## 🙏 WHEN ALL ELSE FAILS

Remember:

1. **The Word of God endures forever** - This tool is just a tool
2. **You can read the data files directly** - They're plain text JSON
3. **The Gospel is simple** - See WHY.txt
4. **You're not alone** - Find other believers

*"If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."* - James 1:5

---

**Still need help? Check:**
- [INDEX.md](INDEX.md) - Complete navigation
- [GETTING_STARTED.md](GETTING_STARTED.md) - Basic setup
- [docs/INSTALL.md](docs/INSTALL.md) - Detailed installation
- [docs/RECOVERY.md](docs/RECOVERY.md) - Rebuild from scratch

---

**Prepared in advance for your success | Soli Deo Gloria**
