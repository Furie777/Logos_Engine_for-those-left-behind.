# Contributing to LOGOS ENGINE

Thank you for your interest in contributing to LOGOS ENGINE!

---

## Philosophy

This project is built with a specific purpose: to preserve and make Scripture accessible when infrastructure fails. Contributions should align with this mission.

**Core Principles:**
- Offline-first operation
- Minimal dependencies
- Cross-platform compatibility
- Self-contained and recoverable
- Educational and accessible

---

## Ways to Contribute

### 1. Report Issues

Found a bug? Let us know!

**When reporting, please include:**
- Operating system (Windows/Mac/Linux/etc.)
- Python version (`python --version`)
- Command you ran
- Error message (full text)
- What you expected to happen

### 2. Improve Documentation

Documentation improvements are always welcome:
- Clarify confusing sections
- Add examples
- Fix typos
- Translate to other languages
- Add platform-specific tips

### 3. Add Features

Before adding features, consider:
- Does it align with the offline-first mission?
- Does it add dependencies? (Minimize these)
- Will it work across all platforms?
- Is it self-documenting?

**Good feature examples:**
- Better error messages
- Additional search capabilities
- Performance improvements
- Data verification improvements
- Recovery mechanisms

**Features to avoid:**
- Cloud/internet dependencies
- Platform-specific tools
- Heavy dependencies
- Opaque/complex algorithms

### 4. Test on Different Platforms

Testing is valuable! Try:
- Different operating systems
- Different Python versions
- Low-resource devices (Raspberry Pi, old phones)
- Different terminal emulators
- Offline scenarios

### 5. Share Use Cases

How are you using LOGOS ENGINE? Share:
- Interesting queries
- Scripture study patterns
- Educational applications
- Integration examples

---

## Setup for Development

```bash
# Clone the repository
git clone https://github.com/Furie777/Logos_Engine_for-those-left-behind..git
cd Logos_Engine_for-those-left-behind.

# Install dependencies
pip3 install -r requirements.txt

# Build the graph
python3 logos.py build

# Test your changes
python3 logos.py verse "John 3:16"
python3 logos.py search "grace"
python3 logos.py stats
```

---

## Code Style

**Python:**
- Follow PEP 8 where practical
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and simple
- Prefer clarity over cleverness

**Shell Scripts:**
- Use POSIX-compatible syntax when possible
- Add comments for non-obvious commands
- Handle errors gracefully
- Test on multiple shells (bash, zsh, sh)

**Batch Scripts:**
- Keep it simple
- Use echo for user feedback
- Check for errors after each critical step
- Test on Windows 10 and 11

---

## Testing Changes

Before submitting:

1. **Test basic commands:**
   ```bash
   python3 logos.py verse "Genesis 1:1"
   python3 logos.py search "faith"
   python3 logos.py strongs H430
   python3 logos.py stats
   ```

2. **Test setup scripts:**
   ```bash
   # Linux/Mac
   bash setup.sh
   
   # Windows (in cmd)
   setup.bat
   ```

3. **Test on clean environment:**
   ```bash
   # Create fresh virtual environment
   python3 -m venv test_env
   source test_env/bin/activate
   pip install networkx
   python3 logos.py verse "John 3:16"
   ```

4. **Check for errors:**
   - No Python exceptions
   - Clear error messages
   - Graceful handling of missing files

---

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

**Commit Message Format:**
```
Brief summary of change (50 chars or less)

Longer explanation if needed:
- What changed
- Why it changed
- Any breaking changes
```

---

## Adding New Commands

If adding a new command to `logos.py`:

1. Add the command logic to appropriate file in `src/`
2. Add command handler in `logos.py` main()
3. Add usage to docstring at top of `logos.py`
4. Update README.md Commands section
5. Test the command
6. Add example to `example_usage.py` if it's an API feature

---

## Dependencies

Keep dependencies minimal. Only add if:
- Essential for core functionality
- Cross-platform compatible
- Well-maintained
- Small footprint

**Required dependency:** networkx

**Optional dependencies should:**
- Degrade gracefully if not installed
- Show clear installation instructions
- Be documented in requirements.txt as comments

---

## Documentation Standards

**For users:**
- Assume no technical background
- Provide copy-paste examples
- Explain why, not just how
- Include troubleshooting

**For developers:**
- Explain the algorithm/approach
- Link to resources
- Document edge cases
- Add inline comments for complex logic

---

## Questions?

Open an issue with the "question" label. We're here to help!

---

## License

By contributing, you agree that your contributions will be freely given and freely shared, in the spirit of the project.

> "Freely ye have received, freely give." - Matthew 10:8

---

## Special Note

This project was built as an act of faith and love. Contributions should be in the same spirit - helping others come to knowledge of the truth.

---

*"And the things that thou hast heard of me among many witnesses, the same commit thou to faithful men, who shall be able to teach others also."* - 2 Timothy 2:2
