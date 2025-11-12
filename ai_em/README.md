# Engineering Manager AI Tool

Expert-level architectural and technical advisory powered by OpenAI.

## 🚀 Quick Setup

### 1. Set Environment Variables

**Locally:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_MODEL="gpt-4o"  # Optional, defaults to gpt-4o
```

**Railway:**
Add these environment variables in your Railway project:
- `OPENAI_API_KEY` = `sk-your-api-key-here`
- `OPENAI_MODEL` = `gpt-4o` (optional)

### 2. Restart MCP Server

```bash
uv run server.py
```

That's it! The tool is now available in Cursor.

---

## 📖 Usage Examples

### Basic Question

In Cursor, ask:
> "Should I use microservices for my application?"

Cursor's AI will automatically call `consult_engineering_manager` and relay the expert advice.

### With Project Context

> "I'm building a real-time chat app. Team has 5 developers, expecting 10K concurrent users, budget is $500/month. Should I use WebSockets or a managed service?"

The Engineering Manager will:
1. Ask clarifying questions (latency requirements, tech stack experience, etc.)
2. Provide 2-4 options with pros/cons and costs
3. Give specific recommendations based on your answers
4. Provide implementation roadmap

---

## 🎯 What It Helps With

- **Architecture decisions** - Microservices vs monolith, service boundaries, API design
- **Technology selection** - Databases, message queues, caching layers, frameworks
- **Scalability** - Load balancing, horizontal scaling, sharding strategies
- **Cost optimization** - Cloud costs, instance sizing, managed vs self-hosted
- **Best practices** - Security, observability, CI/CD, testing strategies
- **Trade-off analysis** - Speed vs quality, cost vs performance, build vs buy

---

## 🔧 How It Works

1. **Client-side state**: Cursor manages conversation history
2. **Stateless server**: No storage needed, fully scalable
3. **Direct API calls**: Uses `urllib` (no external dependencies)
4. **Sliding window**: Keeps last 10 messages to avoid token limits
5. **Smart truncation**: Preserves conversation context while staying under limits

---

## 💰 Cost Estimate

**Per consultation (4-6 exchanges):**

| Model | Cost/Session |
|-------|--------------|
| gpt-4o (recommended) | ~$0.025 |
| gpt-4-turbo | ~$0.040 |
| gpt-4 | ~$0.270 |

**Monthly estimate (100 consultations):** $2.50 - $27 depending on model

---

## 🛠️ Technical Details

**Module:** `ai_em.engineering_manager_tool`  
**Tool Name:** `consult_engineering_manager`  
**Transport:** Direct HTTP to OpenAI API  
**Dependencies:** None (uses stdlib `urllib`)  
**State:** Client-managed (stateless server)  

**Parameters:**
- `question` (required): Your technical question
- `project_context` (optional): Project details for better recommendations
- `conversation_history` (optional): JSON string of previous messages

**Returns:** Engineering Manager's response as markdown text

---

## 🔍 Prompt Location

The system prompt is in: `ai-em/engineering-manager-prompt.md`

**Note:** The prompt file is in `ai-em/` (with hyphen) while the Python module is in `ai_em/` (with underscore). This is intentional - Python module names can't have hyphens, but we keep the prompt in the original folder for consistency.

---

## ✅ Testing

**Test if it's working:**

1. Start the server: `uv run server.py`
2. Check server logs - should show "Starting MCP server..."
3. In Cursor, ask: "List all available MCP tools"
4. Should see `consult_engineering_manager` in the list
5. Ask: "Should I use PostgreSQL or MongoDB?"
6. Should get a response with clarifying questions

**Manual test:**
```python
python3 -c "
from ai_em.engineering_manager_tool import consult_engineering_manager
import os
os.environ['OPENAI_API_KEY'] = 'sk-your-key'
print(consult_engineering_manager('Should I use Redis or Memcached?'))
"
```

---

## 🐛 Troubleshooting

**"OPENAI_API_KEY environment variable not set"**
→ Set the env var before starting the server

**"Import 'ai_em.engineering_manager_tool' could not be resolved"**
→ Make sure `ai_em/__init__.py` exists (not `ai-em/__init__.py`)

**"OpenAI API Error (401): Unauthorized"**
→ Check your API key is valid

**"OpenAI API Error (429): Rate limit exceeded"**
→ You've hit OpenAI rate limits, wait or upgrade plan

**Tool not appearing in Cursor:**
→ Restart Cursor and check MCP server is running

**Empty or error responses:**
→ Check server logs for detailed error messages
→ Verify internet connectivity
→ Test with a simple question first

---

## 📚 Examples of Good Questions

✅ **Architecture:**
- "Should I use microservices for a 10K user SaaS app?"
- "How should I structure my monolith to prepare for future scaling?"

✅ **Technology:**
- "PostgreSQL vs MongoDB for my e-commerce platform?"
- "Which message queue: RabbitMQ, Kafka, or AWS SQS?"

✅ **Scalability:**
- "How do I handle 100K concurrent WebSocket connections?"
- "What caching strategy for a read-heavy social media app?"

✅ **Cost:**
- "How can I reduce my AWS bill for this architecture?"
- "Self-hosted Kubernetes vs managed EKS - which is cheaper?"

✅ **Trade-offs:**
- "Build a custom auth system or use Auth0?"
- "GraphQL vs REST for my mobile app backend?"

---

## 🎓 How the EM Responds

### Phase 1: Clarification
Asks 5-10 questions about:
- Scale (users, requests/sec, data volume)
- Budget constraints
- Team size and skill level
- Timeline and urgency
- Existing infrastructure

### Phase 2: Analysis
Summarizes:
- Key constraints
- Critical considerations
- Red flags and risks

### Phase 3: Solutions
Provides 2-4 options with:
- Approach description
- Specific tech stack
- Pros and cons
- Cost estimate
- Time to production
- When to choose this option

### Phase 4: Implementation
After you choose, provides:
- Phased roadmap (week-by-week)
- Critical path items
- Technical debt to track
- Metrics to monitor
- Exit criteria

---

## 🔄 Updating the Prompt

Want to customize the Engineering Manager's behavior?

1. Edit `ai-em/engineering-manager-prompt.md`
2. Changes take effect immediately (no server restart needed)
3. Test with a new question in Cursor

---

## 🚀 Next Steps

1. Set your `OPENAI_API_KEY` environment variable
2. Restart the MCP server
3. Ask Cursor a technical question
4. Get expert-level guidance!

**Happy building!** 🎉

