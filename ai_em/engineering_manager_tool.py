"""
Engineering Manager AI Tool
Makes direct OpenAI API calls without external libraries
"""

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


def load_em_prompt() -> str:
    """Load Engineering Manager system prompt from markdown file"""
    # Look in ai-em folder (with hyphen) for the markdown file
    prompt_file = Path(__file__).parent.parent / "ai-em" / "engineering-manager-prompt.md"
    
    if not prompt_file.exists():
        return "You are a senior engineering manager and technical advisor."
    
    return prompt_file.read_text()


def call_openai_api(messages: list) -> str:
    """
    Make direct HTTP call to OpenAI API (no libraries needed)
    
    Args:
        messages: List of message dicts with 'role' and 'content'
    
    Returns:
        Assistant's response text
    
    Raises:
        Exception: If API call fails
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return """❌ ERROR: OpenAI API Key Not Configured

The Engineering Manager AI requires an OpenAI API key to function.

🔧 How to fix:

1. Create a .env file in the project root:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_MODEL=gpt-4o
   ```

2. Or set environment variables:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   export OPENAI_MODEL="gpt-4o"
   ```

3. Restart the MCP server:
   ```bash
   uv run server.py
   ```

🔑 Get your API key from: https://platform.openai.com/api-keys

⚠️ The Engineering Manager AI cannot provide guidance without this configuration.
"""
    
    model = os.getenv("OPENAI_MODEL", "gpt-4o")  # Default to gpt-4o
    
    # Prepare request
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    # Make HTTP POST request
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        
        # Parse common OpenAI errors and provide helpful guidance
        if e.code == 401:
            return f"""❌ ERROR: Invalid OpenAI API Key (HTTP 401)

Your API key is invalid or has been revoked.

🔧 How to fix:
1. Check your API key at: https://platform.openai.com/api-keys
2. Generate a new key if needed
3. Update your .env file with the new key
4. Restart the MCP server

Details: {error_body}
"""
        elif e.code == 429:
            return f"""❌ ERROR: OpenAI Rate Limit Exceeded (HTTP 429)

You've hit your API rate limit or quota.

🔧 How to fix:
1. Wait a few minutes and try again
2. Check your usage at: https://platform.openai.com/usage
3. Upgrade your plan if needed: https://platform.openai.com/settings/organization/billing
4. Consider using a cheaper model (set OPENAI_MODEL=gpt-4o-mini in .env)

Details: {error_body}
"""
        elif e.code == 500 or e.code == 503:
            return f"""❌ ERROR: OpenAI Service Unavailable (HTTP {e.code})

OpenAI's API is temporarily unavailable.

🔧 What to do:
1. Check OpenAI status: https://status.openai.com/
2. Wait a few minutes and try again
3. If problem persists, try again later

Details: {error_body}
"""
        else:
            return f"""❌ ERROR: OpenAI API Error (HTTP {e.code})

The OpenAI API returned an error.

Details: {error_body}

🔧 Troubleshooting:
1. Check your API key is valid
2. Verify you have credits: https://platform.openai.com/usage
3. Check OpenAI status: https://status.openai.com/
4. Review OpenAI docs: https://platform.openai.com/docs
"""
    
    except urllib.error.URLError as e:
        return f"""❌ ERROR: Network Connection Failed

Could not connect to OpenAI API.

Details: {str(e)}

🔧 How to fix:
1. Check your internet connection
2. Verify you can access https://api.openai.com
3. Check if you're behind a firewall or proxy
4. Try again in a few moments

If you're using a corporate network, you may need to configure proxy settings.
"""
    
    except json.JSONDecodeError as e:
        return f"""❌ ERROR: Invalid Response from OpenAI

Received malformed response from OpenAI API.

Details: {str(e)}

🔧 What to do:
1. Try the request again
2. Check OpenAI status: https://status.openai.com/
3. If problem persists, report to OpenAI support
"""
    
    except KeyError as e:
        return f"""❌ ERROR: Unexpected Response Format

The OpenAI API response was missing expected data.

Details: Missing key {str(e)}

🔧 What to do:
1. This might be a temporary API issue
2. Try the request again
3. Check OpenAI status: https://status.openai.com/
"""
    
    except Exception as e:
        return f"""❌ ERROR: Unexpected Error

An unexpected error occurred while calling the Engineering Manager AI.

Details: {type(e).__name__}: {str(e)}

🔧 What to do:
1. Try the request again
2. Check the logs for more details
3. Verify your .env configuration
4. Report this error if it persists

If you need immediate help, you can bypass the EM and make architectural decisions manually,
but we recommend consulting the EM for best results.
"""


def consult_engineering_manager(
    question: str,
    project_context: Optional[str] = None,
    conversation_history: Optional[str] = None
) -> str:
    """
    Consult the Engineering Manager AI for architectural and technical decisions.
    
    The EM will ask clarifying questions before providing solutions.
    Handles: architecture, tech stack, scalability, cost optimization, best practices.
    
    Args:
        question: The technical question or problem to discuss
        project_context: Optional project details (team size, scale, budget, tech stack, etc.)
        conversation_history: Optional JSON string of previous messages for continuity
                              Format: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    
    Returns:
        Engineering Manager's response with clarifying questions or detailed guidance
    
    Example:
        # First call
        response = consult_engineering_manager(
            question="Should I use microservices for my chat app?",
            project_context="Team: 5 developers, Expected users: 10K, Budget: $500/month"
        )
        
        # Continue conversation (client manages history)
        response = consult_engineering_manager(
            question="Latency should be <500ms, team knows Node.js",
            conversation_history='[{"role": "user", "content": "Should I use..."}, {"role": "assistant", "content": "..."}]'
        )
    """
    
    # Load Engineering Manager system prompt
    system_prompt = load_em_prompt()
    
    # Build messages list
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history if provided
    if conversation_history:
        try:
            history = json.loads(conversation_history)
            
            # Validate and add history
            if isinstance(history, list):
                # Keep last 10 messages to avoid token limits
                max_messages = 10
                if len(history) > max_messages:
                    history = history[-max_messages:]
                
                # Add valid messages
                for msg in history:
                    if isinstance(msg, dict) and "role" in msg and "content" in msg:
                        messages.append(msg)
        
        except (json.JSONDecodeError, TypeError, KeyError):
            # Invalid JSON, start fresh (ignore history)
            pass
    
    # Build current question with optional context
    current_question = question
    if project_context:
        current_question = f"""PROJECT CONTEXT:
{project_context}

QUESTION:
{question}"""
    
    # Add current question
    messages.append({"role": "user", "content": current_question})
    
    # Call OpenAI API
    response = call_openai_api(messages)
    
    return response


# Tool metadata for MCP registration
TOOL_NAME = "consult_engineering_manager"
TOOL_DESCRIPTION = """Consult Senior Engineering Manager AI for architectural and technical decisions.

Use this when you need expert guidance on:
- System architecture and design patterns
- Technology stack selection and trade-offs
- Scalability and performance optimization
- Cost optimization strategies (cloud, infrastructure)
- Best practices for large-scale distributed systems
- Microservices vs monolith decisions
- Database selection and design
- DevOps, CI/CD, and deployment strategies

The EM will ask clarifying questions before providing solutions to ensure recommendations fit your specific context."""

