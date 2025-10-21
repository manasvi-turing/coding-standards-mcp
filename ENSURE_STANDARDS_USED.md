# How to Ensure Coding Standards Are Always Applied

## ✅ What We've Set Up

Your MCP server now has **built-in instructions** that tell the AI to always check standards before coding!

### 1. Server Instructions
The MCP server includes instructions that are automatically sent to the AI:
```
"Before generating ANY code, you MUST:
1. Identify the language/framework being used
2. Call get_coding_standard() to fetch relevant standards
3. Apply those standards to all code you generate"
```

### 2. MCP Prompt
Added a prompt that's available in Cursor's prompt library that you can invoke.

---

## 🎯 How It Works

### Automatic (Once Server is Running)

1. **Start your server:**
   ```bash
   cd coding-standards-mcp
   uv run server.py
   ```

2. **Restart Cursor**

3. **Start coding** - The AI will automatically:
   - Detect what language you're using
   - Fetch the relevant standards
   - Apply them to generated code

### Manual Trigger (When You Want to Be Explicit)

Ask the AI:
- "Check the coding standards for this"
- "Apply our Python standards"
- "Show me the coding standards for React"
- "Follow our team's coding standards"

---

## 🔧 Additional Ways to Reinforce

### Option 1: Cursor Rules (.cursorrules)

Create a `.cursorrules` file in your project root:

```
# .cursorrules
Before writing any code, always check and apply team coding standards using the coding-standards MCP server.

For Python: Follow PEP 8, use type hints, write docstrings
For JavaScript/TypeScript: Follow our established patterns
For React: Follow component structure guidelines

Always call get_coding_standard() before generating code.
```

### Option 2: Workspace Instructions

In Cursor Settings → Workspace → Add instruction:
```
Always use the coding-standards MCP server to check standards before writing code.
Call get_coding_standard() with the appropriate language before generating code.
```

### Option 3: Project README

Add to your project README:
```markdown
## AI Coding Standards

This project uses MCP to enforce coding standards.
The AI assistant will automatically check standards before generating code.

To manually check standards: Ask "Show me the [language] coding standards"
```

---

## 🎯 Verification

### Test if it's working:

1. Start the server: `uv run server.py`
2. In Cursor, ask: "Write a Python function to read a JSON file"
3. The AI should:
   - Call `get_coding_standard('python')`
   - Apply those standards (type hints, docstrings, etc.)
   - Generate code following your rules

### Check Server Connection:

In Cursor, look for:
- 🟢 Green dot next to MCP servers in status bar
- MCP tools available when you type `@`
- Coding Standards server listed in MCP panel

---

## 💡 Best Practices

### 1. Keep Standards Updated
```bash
vim coding-standards-mcp/coding-standards/python/standards.md
# Server picks up changes automatically
```

### 2. Be Specific in Standards
Instead of: "Follow best practices"
Write: "Use type hints for all function parameters and return values"

### 3. Use Examples
Add code examples in your standards:
```python
# Good
def process_data(items: List[str]) -> Dict[str, int]:
    """Process items and return counts."""
    ...

# Bad
def process_data(items):
    ...
```

### 4. Team Alignment
Share standards with team:
```bash
# After updates, commit and push
git add coding-standards-mcp/coding-standards/
git commit -m "Update Python coding standards"
git push
```

---

## 🚀 For Production (Railway)

When you deploy to Railway:

1. Deploy your server
2. Get the Railway URL
3. Update everyone's mcp.json:
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

Now the ENTIRE TEAM uses the same standards automatically! 🎉

---

## ✅ Summary

**With the server running:**
- ✅ AI automatically has instructions to check standards
- ✅ Tools are available to fetch standards
- ✅ Prompt reminder is available
- ✅ Standards are centralized and easy to update

**Your job:**
1. Keep server running (or deploy to Railway)
2. Update standards as needed
3. Let the AI do the rest!

**The AI will now automatically apply your team's coding standards to all generated code.** 🎯

