# Engineering Manager AI Tool

Expert-level architectural and technical advisory powered by OpenAI.

## Setup

### 1. Set Environment Variables

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_MODEL="gpt-4o"  # Optional, defaults to gpt-4o
```

Or add to Railway environment variables:
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - Model to use (default: `gpt-4o`)

### 2. Available Models

- `gpt-4o` - Best balance (recommended)
- `gpt-4-turbo` - Fast and capable
- `gpt-4` - Most capable (slower, more expensive)
- `gpt-3.5-turbo` - Cheapest (not recommended for complex advice)

## Usage

### From MCP Tool (Cursor)

The tool is automatically available in Cursor as `consult_engineering_manager`.

**Simple question:**
```
consult_engineering_manager(
    question="Should I use microservices for my application?"
)
```

**With project context:**
```
consult_engineering_manager(
    question="Should I use microservices?",
    project_context="Team: 5 developers, Expected users: 10K, Budget: $500/month, Timeline: 3 months"
)
```

**Continue conversation:**
```
consult_engineering_manager(
    question="We have experience with Node.js and React",
    conversation_history='[{"role":"user","content":"Should I use microservices?"},{"role":"assistant","content":"Let me ask..."}]'
)
```

## How It Works

1. **User asks technical question** via Cursor
2. **Tool loads** Engineering Manager system prompt
3. **Makes direct HTTP call** to OpenAI API (no libraries)
4. **Returns expert guidance** with clarifying questions or detailed recommendations
5. **Client manages state** (conversation history passed by Cursor)

## Features

- ✅ **Stateless** - No server-side storage needed
- ✅ **Direct API calls** - No external dependencies (uses urllib)
- ✅ **Configurable** - Set model and API key via env vars
- ✅ **Client-managed history** - Cursor handles conversation continuity
- ✅ **Sliding window** - Keeps last 10 messages to avoid token limits

## Cost Estimation

**Per consultation (average 4-6 exchanges):**

| Model | Input (5K tokens) | Output (2K tokens) | Total/Session |
|-------|-------------------|--------------------:|---------------|
| gpt-4o | $0.0125 | $0.012 | ~$0.025 |
| gpt-4-turbo | $0.025 | $0.015 | ~$0.040 |
| gpt-4 | $0.15 | $0.12 | ~$0.270 |

**Monthly estimate (100 consultations):** $2.50 - $27 depending on model

## Error Handling

The tool handles:
- ❌ Missing API key → Returns error message
- ❌ Network failures → Returns timeout error
- ❌ Invalid JSON history → Starts fresh conversation
- ❌ Token limit exceeded → Truncates to last 10 messages
- ❌ API errors → Returns detailed error from OpenAI

## Prompt Engineering

The system prompt (`engineering-manager-prompt.md`) defines:
- Senior EM/CTO role with FAANG experience
- Four-phase response framework (Clarify → Analyze → Propose → Implement)
- Best practices enforcement (cost, scale, resilience, maintainability)
- Anti-patterns to flag
- Communication style (direct, pragmatic, specific)

## Development

**Test locally:**
```bash
python -c "from ai_em.engineering_manager_tool import consult_engineering_manager; print(consult_engineering_manager('Should I use Redis or Memcached?'))"
```

**Update prompt:**
Edit `engineering-manager-prompt.md` - changes take effect immediately (no restart needed).

## Troubleshooting

**Error: "OPENAI_API_KEY environment variable not set"**
→ Set the environment variable before starting the server

**Error: "Network Error: [Errno 11001] getaddrinfo failed"**
→ Check internet connection and OpenAI API status

**Error: "OpenAI API Error (429): Rate limit exceeded"**
→ You've hit OpenAI rate limits, wait or upgrade plan

**Tool not appearing in Cursor:**
→ Restart Cursor or reload MCP server configuration

