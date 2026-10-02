# GETTING STARTED - For Complete Beginners
## No Coding Experience Needed!

**This guide assumes you know NOTHING about programming or computers beyond basic use.**

---

## 🎯 What You're About to Do

You're going to:
1. Get this program onto your computer
2. Install one free tool (Python)
3. Run simple commands to study the Bible

**Total time:** 10-20 minutes  
**Skill level required:** None - if you can type, you can do this

---

## 📱 CHOOSE YOUR DEVICE

Click one of these based on what you're using:

- **[I have a Windows computer](#windows-10-minutes)**
- **[I have a Mac](#mac-10-minutes)**
- **[I have Linux](#linux-15-minutes)**
- **[I have an Android phone](#android-phone-20-minutes)**
- **[I have a Raspberry Pi](#raspberry-pi-15-minutes)**

---

## 💻 WINDOWS (10 minutes)

### Step 1: Get This Program (2 minutes)

**If you're reading this on GitHub (the website):**
1. Look for a green button that says **"Code"** near the top
2. Click it
3. Click **"Download ZIP"**
4. After download, find the ZIP file (usually in your Downloads folder)
5. Right-click the ZIP file
6. Click **"Extract All"**
7. Choose where to extract (Desktop is fine)

**If you already have these files:**
- You're done with Step 1! Move to Step 2.

### Step 2: Install Python (5 minutes)

Python is a free program that makes LOGOS work.

1. Press the Windows key on your keyboard (bottom left, between Ctrl and Alt)
2. Type: `cmd`
3. Press Enter
4. A black window appears - type: `python --version`
5. Press Enter

**If you see "Python 3.x.x":**
- Python is installed! Skip to Step 3.

**If you see an error:**
1. Open your web browser
2. Go to: https://www.python.org
3. Click the big yellow button that says **"Download Python"**
4. Wait for download
5. Find the downloaded file (python-3.x.x.exe)
6. Double-click it
7. **IMPORTANT:** Check the box that says **"Add Python to PATH"**
8. Click **"Install Now"**
9. Wait for installation
10. Click **"Close"** when done

### Step 3: Install One Small Library (2 minutes)

1. Press Windows key + R
2. Type: `cmd`
3. Press Enter (black window opens)
4. Type exactly: `pip install networkx`
5. Press Enter
6. Wait for it to finish (you'll see "Successfully installed...")

### Step 4: Test It! (1 minute)

1. In the same black window, type: `cd Desktop\LOGOS_ENGINE`
   - (Or wherever you extracted the files)
2. Press Enter
3. Type: `python logos.py verse "John 3:16"`
4. Press Enter

**You should see:**
```
For God so loved the world, that he gave his only begotten Son, 
that whosoever believeth in him should not perish, but have 
everlasting life.
```

**🎉 It works! Go to [What Now?](#what-now)**

---

## 🍎 MAC (10 minutes)

### Step 1: Get This Program (2 minutes)

Same as Windows Step 1 above.

### Step 2: Open Terminal (1 minute)

Terminal is where you type commands on Mac.

1. Press Command + Space (⌘ + Space)
2. Type: `terminal`
3. Press Enter
4. A window opens with white or black background

### Step 3: Check Python (2 minutes)

1. In Terminal, type: `python3 --version`
2. Press Enter

**If you see "Python 3.x.x":**
- You have Python! Skip to Step 5.

**If you see an error:**
- Continue to Step 4.

### Step 4: Install Python (5 minutes - if needed)

1. In Terminal, type this EXACTLY (copy and paste):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Press Enter
3. Wait (it might ask for your password)
4. When done, type: `brew install python3`
5. Press Enter
6. Wait for installation

### Step 5: Install Library (2 minutes)

1. In Terminal, type: `pip3 install networkx`
2. Press Enter
3. Wait for "Successfully installed..."

### Step 6: Test It! (1 minute)

1. Type: `cd Desktop/LOGOS_ENGINE`
   - (Or wherever you put the files)
2. Press Enter
3. Type: `python3 logos.py verse "John 3:16"`
4. Press Enter

**You should see the verse text!**

**🎉 It works! Go to [What Now?](#what-now)**

---

## 🐧 LINUX (15 minutes)

### Step 1: Get This Program (2 minutes)

Same as Windows Step 1 above.

### Step 2: Open Terminal (1 minute)

Usually: Press Ctrl + Alt + T

### Step 3: Install Python (5 minutes)

**For Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**For Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**For Arch:**
```bash
sudo pacman -S python python-pip
```

Type your password when asked.

### Step 4: Install Library (2 minutes)

```bash
pip3 install networkx
```

### Step 5: Test It! (1 minute)

```bash
cd ~/Desktop/LOGOS_ENGINE
python3 logos.py verse "John 3:16"
```

**🎉 It works! Go to [What Now?](#what-now)**

---

## 📱 ANDROID PHONE (20 minutes)

You need an app called Termux. It's a terminal for Android.

### Step 1: Install Termux (5 minutes)

**IMPORTANT:** Don't use Google Play Store (the version there is broken).

1. On your phone, open your browser
2. Go to: f-droid.org
3. Download F-Droid
4. Install F-Droid (you might need to allow "unknown sources" in Settings)
5. Open F-Droid
6. Search for "Termux"
7. Install Termux

### Step 2: Setup Termux (5 minutes)

1. Open Termux
2. Type: `pkg update`
3. Press Enter (wait for it to finish)
4. Type: `pkg install python`
5. Press Enter (wait for installation)
6. Type: `pip install networkx`
7. Press Enter

### Step 3: Get Files on Your Phone (5 minutes)

**If you downloaded the ZIP:**
1. Extract the ZIP using any file manager app
2. Move LOGOS_ENGINE folder to your Downloads folder

**In Termux:**
1. Type: `termux-setup-storage`
2. Press Enter
3. Allow storage permission when phone asks
4. Type: `cp -r ~/storage/shared/Download/LOGOS_ENGINE ~/LOGOS_ENGINE`
5. Press Enter

### Step 4: Test It! (1 minute)

```bash
cd ~/LOGOS_ENGINE
python logos.py verse "John 3:16"
```

**🎉 It works! Go to [What Now?](#what-now)**

---

## 🥧 RASPBERRY PI (15 minutes)

Same as Linux instructions above, but first make sure your Pi is set up:

```bash
sudo apt update
sudo apt install python3 python3-pip
cd ~
# Copy LOGOS_ENGINE folder to your Pi
cd LOGOS_ENGINE
pip3 install networkx
python3 logos.py verse "John 3:16"
```

---

## 🎓 WHAT NOW?

### Your First Commands

Now that it works, try these:

#### Look up any verse:
```bash
python logos.py verse "Genesis 1:1"
python logos.py verse "John 14:6"
python logos.py verse "Revelation 22:21"
```

#### Search for a word:
```bash
python logos.py search "love"
python logos.py search "faith"
python logos.py search "grace"
```

#### Find three witnesses on a topic:
```bash
python logos.py witness "salvation"
python logos.py witness "resurrection"
```

#### Study Hebrew/Greek words:
```bash
python logos.py strongs H430    (Hebrew word for "God")
python logos.py strongs G26     (Greek word for "love")
```

#### See all commands:
```bash
python logos.py help
```

---

## 📖 Learn More

Now that you're up and running:

1. **Read WHY.txt** - Understand the Gospel
2. **Read README.md** - See all available commands
3. **Read docs/INSTALL.md** - More detailed installation info
4. **Explore!** - Try different commands

---

## 🆘 COMMON PROBLEMS

### "python not found"
**Solution:** Try `python3` instead:
```bash
python3 logos.py verse "John 3:16"
```

### "No module named networkx"
**Solution:** Install it:
```bash
pip install networkx
```
or:
```bash
pip3 install networkx
```

### "Permission denied"
**Solution (Linux/Mac only):**
```bash
chmod +x logos.py
```

### "File not found"
**Solution:** Make sure you're in the LOGOS_ENGINE folder:
```bash
cd /path/to/LOGOS_ENGINE
ls
```
You should see `logos.py` in the list.

### Nothing works at all
**Solution:** Read the detailed installation guide:
- Open `docs/INSTALL.md` and follow it carefully
- Each platform has specific instructions

---

## 💡 REMEMBER

- You don't need internet after installation
- You don't need to pay anything
- You don't need coding experience
- You can't break anything by trying commands
- All Scripture is in the `data` folder if you want to read the files directly

---

## 🤝 SHARING WITH OTHERS

Want to give this to someone else?

1. Copy the entire LOGOS_ENGINE folder to:
   - USB drive
   - SD card
   - Send via Bluetooth
   - Burn to CD/DVD
   - Email (if small enough)

2. Give them this file: `GETTING_STARTED.md`

3. They follow the same steps!

---

## 📞 NEED MORE HELP?

1. Read the troubleshooting guide: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check the full documentation: [INDEX.md](INDEX.md)
3. Read about recovery if data is corrupted: `docs/RECOVERY.md`

---

*"If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him."* - James 1:5

**You can do this. Take it one step at a time.**

---

**Prepared for you in advance | Soli Deo Gloria**
