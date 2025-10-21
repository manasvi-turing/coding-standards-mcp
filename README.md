# Coding Standards MCP Server

> **Automatically enforces team coding standards in AI-assisted development**

## 🎯 Purpose

This MCP server provides coding standards to AI assistants (like Cursor) so they automatically follow your team's best practices when generating code.

**What it does:**
- ✅ Stores your team's coding standards for multiple languages
- ✅ Automatically provides standards to AI when coding
- ✅ Ensures consistent code across your team
- ✅ Centralizes standards - update once, apply everywhere

**Languages supported:**
- Python, Java, Node.js, React/Next.js, Vanilla JS
- General coding practices
- Debugging guidelines

---

## 🚀 How to Use

### Quick Start (Local)

**1. Start the server:**
```bash
# Local development
uv run server.py

# Or with plain Python
python server.py
```

**2. Configure Cursor**

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "coding-standards": {
      "name": "Coding Standards",
      "description": "Team coding standards",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**3. Restart Cursor**

Done! The AI will now automatically apply your coding standards.

---

### Production (Railway)

**1. Deploy to Railway:**
```bash
railway init
railway up
```

**2. Share config with team:**
```json
{
  "mcpServers": {
    "coding-standards": {
      "name": "Coding Standards",
      "description": "Team coding standards",
      "url": "https://your-app.railway.app/sse"
    }
  }
}
```

Everyone on your team now uses the same standards! 🎉

---

## 🔍 Test with Inspector (Optional)

Want to see and test all tools visually?

```bash
# Run with MCP Inspector
npx @modelcontextprotocol/inspector uv run ./server.py
```

**Inspector will be available at:** `http://localhost:6274/`

**In the inspector frontend, use:**
- Transport: `SSE`
- URL: `http://localhost:8000/sse`
- Connection Type: `Via Proxy`

This gives you a web UI to test all tools interactively!

---

## 📝 Customize Standards

Edit the markdown files in `coding-standards/`:

```bash
# Edit existing standards
vim coding-standards/python/standards.md

# Add new language
mkdir coding-standards/golang
echo "# Go Standards" > coding-standards/golang/standards.md
```

Changes are picked up automatically!

---

## ✨ How It Works

**Automatic Enforcement:**

1. You start writing code in Cursor
2. AI detects the language (e.g., Python)
3. AI automatically fetches your Python standards
4. AI generates code following YOUR rules

**Manual Usage:**

Ask the AI:
- "Show me the Python coding standards"
- "List all available coding standards"
- "What are our debugging practices?"

---

## 📋 Available Tools

The MCP server provides:

- `list_coding_standards()` - Lists all available standards
- `get_coding_standard(category, name)` - Gets specific standards
- `get_standards_for_project([languages])` - Gets multi-language standards

---

## 🔧 Files & Structure

```
ai-sdlc/
├── server.py                    # MCP server
├── coding-standards/            # Your standards
│   ├── general.md              # General practices
│   ├── debugging.md            # Debugging guidelines
│   ├── python/standards.md
│   ├── java/standards.md
│   ├── nodejs/standards.md
│   ├── react_and_nextjs/standards.md
│   └── vanilla_js/standards.md
├── Procfile                     # Railway config
├── railway.json                 # Railway config
└── pyproject.toml              # Python config
```

---

## 💡 Tips

**Keep server running:**
```bash
# Local development
uv run server.py

# Production
Deploy to Railway (one-time setup)
```

**Update standards:**
```bash
# Edit any .md file in coding-standards/
# Server picks up changes automatically
git commit & push to share with team
```

**Verify it's working:**
In Cursor, ask: "Write a Python function to read JSON"
The AI should use type hints, docstrings, and your standards!

---

## 🆘 Troubleshooting

**Server not connecting?**
1. Check server is running: `lsof -i :8000`
2. Verify mcp.json syntax
3. Restart Cursor completely (⌘+Q, not just reload)

**Standards not applied?**
1. Ensure server is running
2. Look for 🟢 in Cursor status bar
3. Try explicitly: "Use our Python coding standards"

**Update not reflected?**
- Server picks up file changes automatically
- If deployed, push changes and redeploy

---

## 📚 More Info

- **Setup**: See `SHARE_WITH_TEAM.md` for team onboarding
- **Enforcement**: See `ENSURE_STANDARDS_USED.md` for advanced options
- **Deployment**: Just `railway up` in this directory

---

**Questions?** The server is self-documenting - ask the AI to list standards or show you specific guidelines!

🚀 **Now your AI follows YOUR team's rules automatically!**
