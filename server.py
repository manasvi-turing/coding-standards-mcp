"""
MCP Server for Coding Standards
Provides access to coding standards and best practices for various languages and frameworks
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP

# Create MCP server with instructions
mcp = FastMCP(
    "Coding Standards",
    instructions="""You are a coding assistant that ALWAYS checks and applies team coding standards.

IMPORTANT: Before generating ANY code, you MUST:
1. Identify the language/framework being used
2. Call get_coding_standard() to fetch relevant standards
3. Apply those standards to all code you generate

Available standards: python, java, nodejs, react_and_nextjs, vanilla_js, general, debugging
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
                    frontmatter[key.strip()] = value.strip()
    
    return frontmatter, body


def get_available_standards() -> dict:
    """Scan and return available coding standards with descriptions"""
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
        standards["general"].append({
            "name": file.stem,
            "description": frontmatter.get("description", "No description")
        })
    
    # Get language/framework specific standards (subdirectories)
    for subdir in STANDARDS_DIR.iterdir():
        if subdir.is_dir():
            files = list(subdir.glob("*.md"))
            if files:
                standards["languages"][subdir.name] = []
                for file in files:
                    content = file.read_text()
                    frontmatter, _ = parse_frontmatter(content)
                    standards["languages"][subdir.name].append({
                        "name": file.stem,
                        "description": frontmatter.get("description", "No description")
                    })
    
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
    """
    standards = get_available_standards()
    
    result = ["# Available Coding Standards\n"]
    result.append("| Category | Standard | Description | Example Call |")
    result.append("|----------|----------|-------------|--------------|")
    
    # Add general standards
    if standards["general"]:
        for std in standards["general"]:
            name = std["name"] if isinstance(std, dict) else std
            desc = std.get("description", "No description") if isinstance(std, dict) else "No description"
            result.append(f"| `general` | `{name}` | {desc} | `get_coding_standard('general', '{name}')` |")
    
    # Add language/framework standards
    if standards["languages"]:
        for lang, files in sorted(standards["languages"].items()):
            for file in files:
                name = file["name"] if isinstance(file, dict) else file
                desc = file.get("description", "No description") if isinstance(file, dict) else "No description"
                result.append(f"| `{lang}` | `{name}` | {desc} | `get_coding_standard('{lang}', '{name}')` |")
    
    result.append("")
    result.append("---")
    result.append("")
    result.append("**Quick Examples:**")
    result.append("- General: `get_coding_standard('general', 'debugging')`")
    result.append("- Python: `get_coding_standard('python', 'standards')`")
    result.append("- React: `get_coding_standard('react_and_nextjs', 'standards')`")
    
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


if __name__ == "__main__":
    import os
    
    # Run as HTTP server with SSE (for local and remote deployment)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Coding Standards MCP Server")
    print(f"📡 HTTP Server: http://0.0.0.0:{port}")
    print(f"🔌 SSE Endpoint: http://0.0.0.0:{port}/sse")
    print(f"\nPress Ctrl+C to stop")
    
    mcp.run(transport="sse", port=port, host="0.0.0.0")

