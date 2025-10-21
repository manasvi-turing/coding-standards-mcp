# Add Coding Standards to Your Cursor AI

## What This Does

Your AI assistant will automatically use our team's coding standards when writing code.

## Setup (2 minutes)

### Step 1: Add to Cursor Config

Open or create: `~/.cursor/mcp.json`

**For Local (if server running locally):**
```json
{
  "mcpServers": {
    "coding-standards": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**For Production (after we deploy to Railway):**
```json
{
  "mcpServers": {
    "coding-standards": {
      "url": "https://REPLACE-WITH-RAILWAY-URL.railway.app/sse"
    }
  }
}
```

### Step 2: Restart Cursor

That's it! ✅

## Try It

Ask your AI:
- "Show me the Python coding standards"
- "What are our debugging practices?"
- Start coding - AI will automatically apply our standards

## Troubleshooting

**Where is mcp.json?**
- Mac/Linux: `~/.cursor/mcp.json`
- Windows: `C:\Users\YourName\.cursor\mcp.json`

**Create if it doesn't exist:**
```bash
echo '{"mcpServers":{}}' > ~/.cursor/mcp.json
```

Then add the coding-standards config.

**Not working?**
1. Check JSON syntax (use a JSON validator)
2. Make sure server URL is correct
3. Restart Cursor completely
4. Check Cursor logs for MCP errors

## Benefits

✅ Consistent code across team  
✅ AI follows your standards automatically  
✅ No need to repeatedly tell AI your preferences  
✅ Standards stay updated centrally  

---

Questions? Contact: [your contact info]

# Run MCP Server
npx @modelcontextprotocol/inspector uv run ./server.py 

# Inspector can be accessed here
http://localhost:6274/

# In the frontend, use the following settings
Transport: SSE
URL: http://localhost:8000/sse
Connection Type: Via Proxy