# Coding Standards MCP Server

> **Automatically enforces team coding standards in AI-assisted development**

## 🎯 What This Does

Your AI assistant (Cursor, Claude, etc.) will automatically follow your team's coding standards when generating code.

**Benefits:**
- ✅ Consistent code across your entire team
- ✅ No more reminding AI about your standards
- ✅ Centralized standards - update once, apply everywhere
- ✅ Works with Python, Java, Node.js, React, and more

📖 **[Read the blog post: From AI Coding Chaos to Team Standards](wiki/Blog.md)** - Learn about the challenges with file-based standards and why MCP might be the ideal solution for teams (as of now, landscape changing very fast).

---

## 🚀 How to Use

### Step 1: Add MCP Server to Cursor

Edit `~/.cursor/mcp.json` (create if it doesn't exist):

```json
{
  "mcpServers": {
    "coding-standards": {
      "name": "Coding Standards",
      "description": "IMPORTANT: Before generating ANY code, ALWAYS check this server for coding standards. Provides mandatory team coding standards, style guides, best practices, and patterns for Python, Java, Node.js, React/Next.js, JavaScript, general coding, and debugging. Call get_coding_standard() with the language name before writing code to ensure compliance with team standards. And always use the engineering manager ai tool to get the coding standards before writing code.",
      "url": "https://web-production-ad318.up.railway.app/sse"
    }
  }
}
```

### Step 2: Restart Cursor

Close and reopen Cursor. That's it! 🎉

---

## ✨ How It Works

**Automatic Mode (Recommended):**

Just start coding! The AI will:
1. Detect the language you're using
2. Automatically fetch your team's standards
3. Generate code that follows YOUR rules

**Manual Mode:**

Ask the AI:
- *"Show me the Python coding standards"*
- *"List all available coding standards"*
- *"What are our React best practices?"*

---

## 📋 Available Standards

The server provides standards for:

| Category | Standards Available |
|----------|-------------------|
| **Mandatory** | Code complexity (applies to ALL code) |
| **General** | Debugging, development process, server operations |
| **Python** | General Python, FastAPI |
| **Node.js** | General Node.js, Express.js |
| **React** | React & Next.js |

Ask the AI: *"List all available coding standards"* to see the full list with descriptions.

---

## 🔧 Available MCP Tools

The AI can use these tools:

- `list_coding_standards()` - See all standards (mandatory vs optional)
- `get_coding_standard(category, name)` - Get specific standards
- `get_standards_for_project([languages])` - Get multi-language standards

You don't need to call these manually - the AI knows when to use them!

---

## 💡 Quick Tips

**Want the AI to follow a specific standard?**
```
"Use our FastAPI standards to create a new API endpoint"
```

**Check what standards apply to your current code?**
```
"What coding standards should I follow for this Python project?"
```

**See all standards at once?**
```
"Show me all our team's coding standards"
```

---

## 🔄 Standards Update Automatically

When standards are updated on the server, your AI automatically gets the latest version. No configuration needed!

---

# 👨‍💻 Development Guide

> **For developers who maintain or deploy this server**

## 📁 Project Structure

```
ai-sdlc/
├── server.py                           # MCP server implementation
├── coding-standards/                   # Standards directory
│   ├── code_complexity.md             # Mandatory for all code
│   ├── debugging.md                   # General debugging
│   ├── development_process.md         # Process guidelines
│   ├── server_operations.md           # Server ops
│   ├── python/
│   │   ├── fastapi.md                 # FastAPI standards
│   │   └── general.md                 # Python standards
│   ├── nodejs/
│   │   ├── expressjs.md               # Express.js standards
│   │   └── general.md                 # Node.js standards
│   ├── react_and_nextjs/
│   │   └── general.md                 # React/Next.js standards
│   └── vanilla_js/
│       └── general.md                 # Vanilla JS standards
├── requirements.txt                    # Python dependencies
├── pyproject.toml                     # Python project config
├── uv.lock                            # UV lock file
├── Procfile                           # Railway deployment config
└── railway.json                       # Railway configuration
```

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- UV (recommended) or pip

### Setup & Run

**Option 1: Using UV (Recommended)**
```bash
# Clone the repo
git clone <your-repo-url>
cd ai-sdlc

# Run server (UV handles dependencies automatically)
uv run server.py
```

**Option 2: Using pip**
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

The server will start on `http://localhost:8000/sse`

### Local MCP Configuration

For local development, use this in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "coding-standards": {
      "name": "Coding Standards (Local)",
      "description": "Local development coding standards server",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## 📝 Adding/Editing Standards

### Standard File Format

Each standard file uses YAML frontmatter:

```markdown
---
description: Brief description of the standard
status: active
mandatory: false
---

# Your Standard Title

[Your content here...]
```

### Frontmatter Fields

| Field | Required | Values | Purpose |
|-------|----------|--------|---------|
| `description` | ✅ | text | Shows in listings |
| `status` | ✅ | `active` / other | Only `active` standards are visible |
| `mandatory` | ❌ | `true` / `false` | If `true`, applies to ALL code (defaults to `false`) |

### Adding a New Standard

**1. Create the file:**
```bash
# For language-specific standard
mkdir -p coding-standards/golang
touch coding-standards/golang/general.md

# For general standard
touch coding-standards/testing.md
```

**2. Add frontmatter and content:**
```markdown
---
description: Go coding standards and best practices
status: active
mandatory: false
---

# Go Coding Standards

## Code Organization
...
```

**3. Test:**
```bash
# Restart server (changes are auto-detected)
# Ask AI: "List all coding standards"
```

### Making a Standard Mandatory

Edit the frontmatter:
```yaml
---
description: Must follow for ALL code
status: active
mandatory: true  # ← This makes it mandatory
---
```

Mandatory standards appear in the "🚨 MANDATORY STANDARDS" table and apply to ALL code, regardless of language.

## 🧪 Testing

### Manual Testing

```bash
# Start server
uv run server.py

# In another terminal, test the endpoint
curl http://localhost:8000/sse
```

### Testing with MCP Inspector

```bash
# Install and run inspector
npx @modelcontextprotocol/inspector
```

Open `http://localhost:6274/` and configure:
- Transport: `SSE`
- URL: `http://localhost:8000/sse`
- Connection Type: `Via Proxy`

Test all MCP tools visually!

### Testing in Cursor

1. Configure local MCP server in `~/.cursor/mcp.json`
2. Restart Cursor
3. Ask: *"List all coding standards"*
4. Verify output matches your files

## 🔍 MCP Server Implementation

### Key Functions

**`parse_frontmatter(content: str)`**
- Parses YAML frontmatter from markdown
- Converts boolean strings to Python booleans

**`get_available_standards()`**
- Scans `coding-standards/` directory
- Filters by `status: active`
- Returns dict with general and language-specific standards

**`list_coding_standards()`** (MCP Tool)
- Lists all active standards
- Separates mandatory vs language-specific
- Returns formatted markdown table

**`get_coding_standard(category, name)`** (MCP Tool)
- Fetches specific standard content
- Returns full markdown content

**`get_standards_for_project(languages)`** (MCP Tool)
- Gets standards for multiple languages
- Always includes general standards
- Returns combined markdown

## 📊 Monitoring

Check server health:
```bash
# Railway logs
railway logs

# Or visit your app URL
curl https://your-app.railway.app/sse
```

## 🐛 Troubleshooting

### Standards not showing up?
- Check `status: active` in frontmatter
- Verify file is in correct directory
- Restart server

### MCP not working in Cursor?
- Verify `~/.cursor/mcp.json` syntax
- Check URL is correct
- Restart Cursor completely

### Server not starting?
- Check Python version (3.11+)
- Verify all dependencies installed
- Check port 8000 is available

---

## 📚 Learn More

**[From AI Coding Chaos to Team Standards](wiki/Blog.md)** - Read our journey from file-based standards to MCP, including:
- The challenges with agents.md and .cursorrules
- Why AI agents ignore file-based rules
- How MCP solves team-scale standards enforcement
- Real-world implementation guide

**[Research Documentation](wiki/research/)** - Deep dive into our findings:
- [agents.md reliability issues](wiki/research/01-agents-md-reliability-issues.md) - Community reports and root causes
- [MCP architecture advantages](wiki/research/02-mcp-architecture-advantages.md) - Technical comparison and benefits
- [Key statistics and quotes](wiki/research/03-key-statistics-and-quotes.md) - Data points and evidence

---

**Questions?** Open an issue or ask the AI to help you use the coding standards! 🚀
