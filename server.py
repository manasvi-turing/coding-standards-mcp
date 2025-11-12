"""
MCP Server for Coding Standards
Provides access to coding standards and best practices for various languages and frameworks
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Import Engineering Manager AI tool
from ai_em.engineering_manager_tool import (
    consult_engineering_manager as em_consult,
    TOOL_DESCRIPTION as EM_TOOL_DESC
)

# Create MCP server with instructions
mcp = FastMCP(
    "Coding Standards",
    instructions="""You are a coding assistant that ALWAYS checks and applies team coding standards.

IMPORTANT: Before generating ANY code, you MUST:
1. ALWAYS apply the mandatory general standards above
2. Identify the language/framework being used
3. Call get_coding_standard() to fetch language-specific standards
4. Apply all relevant standards to code you generate

Available language-specific standards: python, java, nodejs, react_and_nextjs, vanilla_js
"""
)

# Path to coding standards directory
STANDARDS_DIR = Path(__file__).parent / "coding-standards"


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content"""
    frontmatter = {}
    body = content
    
    # Check if content starts with ---
    if content.startswith('---\n'):
        # Find the closing ---
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            body = match.group(2)
            
            # Parse simple key: value pairs (no YAML library needed for simple cases)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert boolean strings to actual booleans
                    if value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    
                    frontmatter[key] = value
    
    return frontmatter, body


def get_available_standards() -> dict:
    """Scan and return available coding standards with descriptions
    
    Only includes standards with status: active
    Includes mandatory flag (defaults to False if not present)
    """
    standards = {
        "general": [],
        "languages": {},
        "frameworks": {}
    }
    
    if not STANDARDS_DIR.exists():
        return standards
    
    # Get general standards (files at root level)
    for file in STANDARDS_DIR.glob("*.md"):
        content = file.read_text()
        frontmatter, _ = parse_frontmatter(content)
        
        # Only include if status is active
        if frontmatter.get("status") == "active":
            standards["general"].append({
                "name": file.stem,
                "description": frontmatter.get("description", "No description"),
                "mandatory": frontmatter.get("mandatory", False)
            })
    
    # Get language/framework specific standards (subdirectories)
    for subdir in STANDARDS_DIR.iterdir():
        if subdir.is_dir():
            files = list(subdir.glob("*.md"))
            if files:
                category_standards = []
                for file in files:
                    content = file.read_text()
                    frontmatter, _ = parse_frontmatter(content)
                    
                    # Only include if status is active
                    if frontmatter.get("status") == "active":
                        category_standards.append({
                            "name": file.stem,
                            "description": frontmatter.get("description", "No description"),
                            "mandatory": frontmatter.get("mandatory", False)
                        })
                
                # Only add category if it has active standards
                if category_standards:
                    standards["languages"][subdir.name] = category_standards
    
    return standards


@mcp.prompt()
def coding_standards_prompt() -> str:
    """
    Prompt that reminds AI to check and apply coding standards.
    This will be available in Cursor's prompt library.
    """
    return """Before writing code, always:
1. Check the relevant coding standards using get_coding_standard()
2. Apply the standards to your code
3. Follow the team's best practices

Available standards: Python, Java, Node.js, React/Next.js, Vanilla JS, General, Debugging
"""


@mcp.tool()
def list_coding_standards() -> str:
    """
    List all available coding standards by language and framework with descriptions.
    Use this tool first to see what standards are available.
    
    ⚠️ IMPORTANT: Standards marked as MANDATORY apply to ALL code, with NO EXCEPTIONS.
    Language-specific standards apply based on the technology being used.
    """
    standards = get_available_standards()
    
    result = ["# Available Coding Standards\n"]
    result.append("## 🚨 MANDATORY STANDARDS (Apply to ALL code - NO EXCEPTIONS)\n")
    result.append("| Category | Standard | Description | Example Call |")
    result.append("|----------|----------|-------------|--------------|")
    
    # Collect all mandatory standards (from general and languages)
    mandatory_found = False
    
    # Check general standards for mandatory ones
    if standards["general"]:
        for std in standards["general"]:
            if std.get("mandatory", False):
                name = std["name"]
                desc = std["description"]
                result.append(f"| `general` ⚠️ | `{name}` | **[MANDATORY]** {desc} | `get_coding_standard('general', '{name}')` |")
                mandatory_found = True
    
    # Check language/framework standards for mandatory ones
    if standards["languages"]:
        for lang, files in sorted(standards["languages"].items()):
            for file in files:
                if file.get("mandatory", False):
                    name = file["name"]
                    desc = file["description"]
                    result.append(f"| `{lang}` ⚠️ | `{name}` | **[MANDATORY]** {desc} | `get_coding_standard('{lang}', '{name}')` |")
                    mandatory_found = True
    
    if not mandatory_found:
        result.append("| - | - | No mandatory standards configured | - |")
    
    result.append("\n## 📚 Language/Framework Specific Standards (Apply based on technology used)\n")
    result.append("| Category | Standard | Description | Example Call |")
    result.append("|----------|----------|-------------|--------------|")
    
    # Add non-mandatory standards
    specific_found = False
    
    # Add non-mandatory general standards
    if standards["general"]:
        for std in standards["general"]:
            if not std.get("mandatory", False):
                name = std["name"]
                desc = std["description"]
                result.append(f"| `general` | `{name}` | {desc} | `get_coding_standard('general', '{name}')` |")
                specific_found = True
    
    # Add non-mandatory language/framework standards
    if standards["languages"]:
        for lang, files in sorted(standards["languages"].items()):
            for file in files:
                if not file.get("mandatory", False):
                    name = file["name"]
                    desc = file["description"]
                    result.append(f"| `{lang}` | `{name}` | {desc} | `get_coding_standard('{lang}', '{name}')` |")
                    specific_found = True
    
    if not specific_found:
        result.append("| - | - | No language-specific standards configured | - |")
    
    return "\n".join(result)


def _get_coding_standard_impl(category: str, name: Optional[str] = None) -> str:
    """Helper function to get coding standards (not exposed as tool)"""
    if not STANDARDS_DIR.exists():
        return f"Error: Standards directory not found at {STANDARDS_DIR}"
    
    # Handle general standards
    if category == "general":
        if name:
            file_path = STANDARDS_DIR / f"{name}.md"
        else:
            file_path = STANDARDS_DIR / "general.md"
        
        if file_path.exists():
            return file_path.read_text()
        else:
            available = [f.stem for f in STANDARDS_DIR.glob("*.md")]
            return f"Standard not found. Available general standards: {', '.join(available)}"
    
    # Handle language/framework specific standards
    category_dir = STANDARDS_DIR / category
    if not category_dir.exists():
        available = [d.name for d in STANDARDS_DIR.iterdir() if d.is_dir()]
        return f"Category '{category}' not found. Available categories: {', '.join(available)}"
    
    if name:
        file_path = category_dir / f"{name}.md"
        if file_path.exists():
            return file_path.read_text()
        else:
            available = [f.stem for f in category_dir.glob("*.md")]
            return f"Standard '{name}' not found in '{category}'. Available: {', '.join(available)}"
    else:
        # Return all standards in the category
        files = list(category_dir.glob("*.md"))
        if not files:
            return f"No standards found in category '{category}'"
        
        result = [f"# {category.replace('_', ' ').title()} Coding Standards\n"]
        for file in files:
            result.append(f"## {file.stem}\n")
            result.append(file.read_text())
            result.append("\n---\n")
        
        return "\n".join(result)


@mcp.tool()
def get_coding_standard(category: str, name: Optional[str] = None) -> str:
    """
    Get coding standards for a specific language or framework.
    
    Args:
        category: The category (e.g., 'general', 'python', 'react_and_nextjs', 'java', 'nodejs')
        name: Optional specific standard name (e.g., 'debugging', 'testing'). 
              If not provided, returns the main standard file or all files in the category.
    
    Examples:
        - get_coding_standard('general') - Get general coding standards
        - get_coding_standard('python') - Get Python coding standards
        - get_coding_standard('general', 'debugging') - Get debugging standards
    """
    return _get_coding_standard_impl(category, name)


@mcp.tool()
def get_standards_for_project(languages: List[str]) -> str:
    """
    Get all relevant coding standards for a project using multiple languages/frameworks.
    
    Args:
        languages: List of languages/frameworks used in the project 
                  (e.g., ['python', 'react_and_nextjs', 'nodejs'])
    
    Returns combined standards for all specified languages plus general standards.
    """
    result = ["# Project Coding Standards\n"]
    
    # Always include general standards
    general = _get_coding_standard_impl("general")
    if not general.startswith("Error"):
        result.append("## General Standards\n")
        result.append(general)
        result.append("\n---\n")
    
    # Add standards for each language
    for lang in languages:
        lang_std = _get_coding_standard_impl(lang)
        if not lang_std.startswith("Error") and not lang_std.startswith("Category"):
            result.append(f"## {lang.replace('_', ' ').title()} Standards\n")
            result.append(lang_std)
            result.append("\n---\n")
    
    return "\n".join(result)


@mcp.tool()
def consult_engineering_manager(
    question: str,
    project_context: Optional[str] = None,
    conversation_history: Optional[str] = None
) -> str:
    """
    Consult Senior Engineering Manager AI for architectural and technical decisions.
    
    Use this when you need expert guidance on:
    - System architecture and design patterns
    - Technology stack selection and trade-offs
    - Scalability and performance optimization
    - Cost optimization strategies (cloud, infrastructure)
    - Best practices for large-scale distributed systems
    - Microservices vs monolith decisions
    - Database selection and design
    - DevOps, CI/CD, and deployment strategies
    
    ⚠️ IMPORTANT - HANDLING CLARIFYING QUESTIONS:
    
    The EM will often ask clarifying questions. You MUST handle this properly:
    
    ✅ OPTION 1: Multi-turn conversation (preferred for complex decisions)
       - First call: Get clarifying questions from EM
       - Ask user for answers to those specific questions
       - Second call: Provide answers using conversation_history parameter
       - EM provides tailored recommendations
    
    ✅ OPTION 2: Fast Path with explicit assumptions (when user wants quick guidance)
       - Include "ASSUMPTIONS:" keyword in project_context
       - List explicit assumptions about team, scale, budget, timeline, experience
       - EM will provide immediate conditional guidance based on stated assumptions
       - Example: "ASSUMPTIONS: Small team (3 devs), MVP phase, budget <$500/month, 
                   familiar with SQL, need to ship in 2 weeks"
    
    ❌ OPTION 3: DO NOT proceed without guidance (defeats the purpose!)
       - DO NOT ignore clarifying questions and make your own decisions
       - DO NOT call the tool and then not use its advice
       - That defeats the entire purpose of expert consultation
    
    🚨 MANDATORY: TODO Generation & Pre-Flight Checklist
    
    When the EM provides a STRUCTURED ACTION PLAN (with REQUIRED_TODOS), you MUST:
    
    1. **Create TODOs BEFORE implementing**:
       - Call todo_write() with all items from REQUIRED_TODOS
       - Mark the first TODO as "in_progress", rest as "pending"
       - Include priority and time estimates in TODO content
    
    2. **Present Pre-Flight Checklist to user**:
       ```
       📋 Pre-Flight Checklist (from Engineering Manager)
       
       The EM recommended I build:
       ✓ [Component 1]
       ✓ [Component 2]
       ✓ [Component 3]
       
       Success criteria:
       - [Criterion 1]
       - [Criterion 2]
       
       Implementation order:
       1. [Step 1] (blocks [Step 2, 3])
       2. [Step 2]
       3. [Step 3]
       
       Estimated timeline: X hours
       
       Proceeding with implementation...
       ```
    
    3. **Follow the IMPLEMENTATION_ORDER** provided by EM
       - Don't skip foundational steps
       - Respect blocking dependencies
       - Complete critical tasks first
    
    4. **Check off items as you complete them**
       - Update TODOs to "completed" when done
       - Verify SUCCESS_CRITERIA are met before marking complete
    
    ⚠️ If you skip TODO generation or ignore the action plan, you are misusing this tool!
    
    Args:
        question: The technical question or problem to discuss
        project_context: Optional project details. For FAST PATH, prefix with "ASSUMPTIONS:" 
                        followed by explicit constraints (team size, scale, budget, timeline, 
                        experience level, tech familiarity)
        conversation_history: Optional JSON string of previous messages for multi-turn conversations
    
    Examples:
        # Example 1: Multi-turn (get clarifying questions first)
        response1 = consult_engineering_manager(
            question="Should I use microservices?"
        )
        # EM asks: team size? scale? budget? etc.
        # Ask user these questions, then:
        response2 = consult_engineering_manager(
            question="Team: 5 devs, 10K users expected, $1K/month budget",
            conversation_history='[{"role":"user","content":"Should I use microservices?"},{"role":"assistant","content":"..."}]'
        )
        
        # Example 2: Fast path with assumptions (immediate guidance)
        response = consult_engineering_manager(
            question="Should I use PostgreSQL or MongoDB?",
            project_context="ASSUMPTIONS: Small team (3 devs), relational data model, 
                            team familiar with SQL, MVP phase, budget <$500/month, 
                            need to ship in 4 weeks"
        )
        # EM provides immediate conditional recommendations
        
        # Example 3: With context (EM may still ask some questions)
        response = consult_engineering_manager(
            question="How should I handle real-time updates?",
            project_context="Building analytics dashboard, Python FastAPI + React, 
                            500 concurrent users, updates every 2 seconds"
        )
    """
    return em_consult(question, project_context, conversation_history)


if __name__ == "__main__":
    import os
    
    # Run as HTTP server with SSE (for local and remote deployment)
    port = int(os.getenv("PORT", 8002))
    
    print(f"🚀 Starting Coding Standards MCP Server")
    print(f"📡 HTTP Server: http://0.0.0.0:{port}")
    print(f"🔌 SSE Endpoint: http://0.0.0.0:{port}/sse")
    print(f"\nPress Ctrl+C to stop")
    
    mcp.run(transport="sse", port=port, host="0.0.0.0")

