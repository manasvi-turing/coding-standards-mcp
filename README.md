# Coding Standards MCP Server

MCP server that provides coding standards to AI assistants.

## Run Locally

### Start the server:
```bash
uv run server.py
# or
./START_SERVER.sh
```

Server starts on: `http://localhost:8000/sse`

### Test with Inspector (Visual UI):
```bash
uv run mcp dev server.py
# or
./START_INSPECTOR.sh
```

Opens a web interface to test all tools interactively!

## Deploy to Railway

```bash
railway init
railway up
```

## Configure in Cursor

**Local:**
```json
{
  "mcpServers": {
    "coding-standards": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**Production:**
```json
{
  "mcpServers": {
    "coding-standards": {
      "url": "https://your-app.railway.app/sse"
    }
  }
}
```

See `cursor-mcp-config.json` for copy-paste configs.

## Tools

- `list_coding_standards()` - List all standards
- `get_coding_standard(category, name)` - Get specific standard
- `get_standards_for_project([languages])` - Get multi-language standards

## Customize

Edit markdown files in the `coding-standards/` subdirectory.

Server auto-detects changes!

```bash
# Edit existing
vim coding-standards/python/standards.md

# Add new language
mkdir coding-standards/golang
echo "# Go Standards" > coding-standards/golang/standards.md
```
