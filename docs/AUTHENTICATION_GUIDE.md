# Authentication Guide for GitHub Access

This guide helps you set up secure authentication for pushing to this repository.

## ⚠️ CRITICAL SECURITY RULES

**NEVER do any of the following:**

1. **NEVER share your tokens or SSH private keys with anyone** - not even trusted friends, family, or AI assistants
2. **NEVER commit tokens, passwords, or keys to any repository** - they become permanently searchable in git history
3. **NEVER paste tokens in chat messages, emails, or documents** - these can be logged, cached, or recovered
4. **NEVER store tokens in plain text files** in your project directory
5. **NEVER include tokens in screenshots or screen recordings**

## Why This Matters

Once a token or secret is exposed:
- **Git history is permanent** - even deleted commits can be recovered
- **Search engines index public repos** - exposed tokens become searchable forever
- **Attackers actively scan** GitHub for exposed credentials
- **Recovery is nearly impossible** - you must assume the token is compromised

---

## Setting Up Authentication (The Safe Way)

### Option 1: GitHub Personal Access Token (PAT)

**Creating a token:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → **Tokens (classic)**
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Phone Access - Logos Engine")
4. Select expiration (shorter is safer)
5. Select scopes: `repo` (for full repository access)
6. Click "Generate token"

**Storing the token securely:**

- ✅ Use a password manager (1Password, Bitwarden, etc.)
- ✅ Use your device's secure credential storage
- ✅ Memorize it if possible, then delete any copies
- ❌ Do NOT save in notes apps, text files, or documents
- ❌ Do NOT email or message it to yourself

**Using the token:**

When git asks for your password, use the token instead. Your username is your GitHub username.

```
Username: your-github-username
Password: [paste your token here - then clear clipboard immediately]
```

### Option 2: SSH Keys

**Generate a key (on your device):**

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- When asked for a passphrase, **use a strong one** - this protects the key if your device is compromised
- This creates two files:
  - `~/.ssh/id_ed25519` - **PRIVATE KEY** (never share this)
  - `~/.ssh/id_ed25519.pub` - Public key (safe to share)

**Add public key to GitHub:**

1. Copy your PUBLIC key: `cat ~/.ssh/id_ed25519.pub`
2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste the public key and save

---

## If You Accidentally Expose a Token

**Act immediately:**

1. **Revoke the token** in GitHub Settings → Personal access tokens → Delete
2. **Generate a new token** with a different value
3. **Review your account** for any unauthorized activity
4. If committed to a repo, consider the entire git history compromised

---

## Security Checklist

Before using any authentication method, verify:

- [ ] Token/key is stored in a secure password manager or device keychain
- [ ] No copies exist in text files, notes, or documents
- [ ] Token has the minimum required permissions
- [ ] Token has an expiration date set
- [ ] You have not shared the token with anyone
- [ ] The token does not appear in any repository files

---

## For AI Assistants (Claude, etc.)

**Important:** AI assistants should **never** ask for or receive your tokens, passwords, or private keys. They can:

- ✅ Help you understand the process
- ✅ Explain commands and concepts
- ✅ Troubleshoot issues based on error messages
- ❌ They should NEVER receive your actual credentials

If an AI asks for your token or key, **do not provide it**.

---

## Summary

| Do | Don't |
|----|-------|
| Use password managers | Store tokens in plain text |
| Set token expiration | Create tokens that never expire |
| Use minimum permissions | Give tokens full access |
| Revoke unused tokens | Leave old tokens active |
| Verify secure storage | Trust "hidden" storage |

---

*Your security protects not just you, but everyone who depends on this repository.*
