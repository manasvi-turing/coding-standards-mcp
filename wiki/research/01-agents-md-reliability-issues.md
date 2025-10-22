# Research: agents.md and .cursorrules Reliability Issues

## Overview
This document compiles research findings on the widespread issue of AI coding agents ignoring `agents.md` files and `.cursorrules` configurations across various platforms.

---

## Key Finding: AI Agents Frequently Ignore Rule Files

### 1. agents.md Not Automatically Included in Context

**Source:** [Cursor Forum - agents.md not included in AI context](https://forum.cursor.com/t/agents-md-not-included-in-ai-context/138480)

**Issue:**
- `AGENTS.md` file is not automatically included in AI chat context
- AI agent ignores instructions specified in the file
- Users must manually attach the file to each chat session

**Quote:**
> "The `AGENTS.md` file is not automatically included in AI chats, leading to the AI ignoring its instructions."

**Workaround:**
- Manual inclusion by explicitly referencing/attaching the file during interactions
- Temporary solution, not scalable for team workflows

---

### 2. Cursor Frequently Ignores .cursorrules

**Source:** [Cursor Forum - Cursor just ignores rules](https://forum.cursor.com/t/cursor-just-ignores-rules/69188)

**Issue:**
- Users report AI consistently ignores established rules
- Partial application: AI uses some parts (like greetings) but ignores substantive rules
- Non-deterministic behavior

**Quote:**
> "The AI consistently uses the greeting in my rules but ignores the rest, suggesting a partial application of the rules."

**Community Observations:**
- Multiple users reporting same issue
- Inconsistent rule adherence across sessions
- Configuration appears correct but still fails

---

### 3. Agent Doesn't Understand Its Own Rule System

**Source:** [Cursor Forum - Agent doesn't know how its own rule system works](https://forum.cursor.com/t/cursor-agent-does-not-even-know-how-its-own-rule-system-works/138394)

**Issue:**
- Agent creates `.md` files instead of `.mdc` files
- Misplaces frontmatter sections
- Doesn't follow its own rule file format

**Quote:**
> "A user noted that the agent often creates `.md` files instead of `.mdc` files and misplaces the frontmatter section, leading to inconsistent rule application."

**Impact:**
- Even when users configure rules correctly, agent generates incorrect rule files
- Self-perpetuating problem

---

## Technical Root Causes

### 1. Context Window Management

**Source:** [Cursor Documentation](https://docs.cursor.com/en/context)

**Explanation:**
- Large language models lack memory between completions
- Rules must be included at start of model's context
- AI decides what to include/exclude based on perceived relevance

**Quote:**
> "Rules are essential because large language models lack memory between completions. By including rules at the start of the model's context, they provide consistent guidance for code generation and workflow assistance."

**Problem:**
- If AI doesn't see rules as relevant, it deprioritizes them
- Context window fills with other content
- Rules get dropped or ignored

---

### 2. .mdc File Configuration Complexity

**Sources:**
- [Cursor Forum - Procedural Programming](https://forum.cursor.com/t/procedural-programming/132291)
- [GitHub Gist - Cursor Rules Deep Dive](https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6)

**Required Frontmatter:**
```mdc
---
description: "Comprehensive explanation of rule's purpose"
globs: ["*.test.ts", "*.test.js"]
alwaysApply: false
---
```

**Configuration Issues:**
- `description`: Must be detailed enough for AI to understand when to apply
- `globs`: File patterns must match exactly
- `alwaysApply`: 
  - `false` = conditional (often ignored)
  - `true` = always applied (forces inclusion)

**Problem:**
- Complex configuration with many failure points
- Users often misconfigure without realizing
- Even correct configuration doesn't guarantee compliance

---

### 3. Non-Deterministic LLM Behavior

**Source:** [Cursor Forum - Cursor just ignores rules](https://forum.cursor.com/t/cursor-just-ignores-rules/69188)

**Issue:**
- Large language models inherently non-deterministic
- Same prompt may yield different results
- Rule adherence varies even with identical configuration

**Quote:**
> "The non-deterministic nature of large language models means that some variability in rule adherence may persist."

**Impact:**
- No 100% guarantee of rule application
- Frustrating for developers expecting consistent behavior
- Requires constant monitoring and manual intervention

---

## Community Workarounds

### 1. The "AlwaysApply" Hammer

**Source:** [Dev.to - Force Cursor AI to Follow Rules](https://dev.to/ultrawideturbodevs/how-to-force-cursor-ai-agents-into-always-following-project-rules-using-auto-rule-2ilk)

**Approach:**
- Set `alwaysApply: true` in all rule files
- Forces rule inclusion regardless of context

**Configuration:**
```mdc
---
description: "Must follow for all code"
globs: ["**/*"]
alwaysApply: true  # Force inclusion
---
```

**Limitations:**
- Still not 100% reliable
- Can overwhelm context window with too many rules
- May interfere with other context

---

### 2. Manual Attachment Pattern

**Source:** [Cursor Forum - agents.md not included](https://forum.cursor.com/t/agents-md-not-included-in-ai-context/138480)

**Approach:**
- Manually attach `agents.md` to every chat session
- Explicitly reference file in prompts

**Example Prompt:**
```
"Using the guidelines in agents.md (attached), please write..."
```

**Limitations:**
- Tedious and time-consuming
- Not scalable for teams
- Easy to forget
- Defeats purpose of automatic standards

---

### 3. Multiple Rule Files with Priorities

**Source:** [Medium - Why Your AI Agent is Ignoring You](https://sdrmike.medium.com/cursor-rules-why-your-ai-agent-is-ignoring-you-and-how-to-fix-it-5b4d2ac0b1b0)

**Approach:**
- Create multiple `.mdc` files with specific purposes
- Use naming conventions (e.g., `001-critical.mdc`, `002-style.mdc`)
- Provide very detailed descriptions

**Example:**
```
.cursor/rules/
├── 001-mandatory-standards.mdc
├── 002-python-specific.mdc
└── 003-testing-guidelines.mdc
```

**Theory:**
- Numerical prefixes may influence priority (unofficial)
- Multiple specific rules better than one large rule
- More granular control

**Limitations:**
- Not officially documented
- Still relies on AI's context management
- Maintenance overhead increases

---

### 4. Auto-Rule Generation

**Source:** [Dev.to - Force Cursor AI to Follow Rules](https://dev.to/ultrawideturbodevs/how-to-force-cursor-ai-agents-into-always-following-project-rules-using-auto-rule-2ilk)

**Approach:**
- Automatically generate rules based on codebase analysis
- Create context-specific rules that AI finds more relevant
- Dynamic rule creation

**Benefits:**
- Rules more likely to be seen as relevant
- Adapts to project evolution
- Reduces manual configuration

**Limitations:**
- Requires additional tooling
- Complex setup
- May not capture team-specific preferences

---

## Cross-Platform Issues

### 1. Tool-Specific Formats

**Different tools, different approaches:**

| Tool | Configuration File | Format | Notes |
|------|-------------------|--------|-------|
| Cursor | `.cursorrules` or `.cursor/rules/*.mdc` | YAML frontmatter + Markdown | Frequent ignore issues |
| Gemini Code Assist | `GEMINI.md` | Markdown | Similar issues reported |
| GitHub Copilot | Content exclusion settings | JSON config | Different mechanism |
| Generic | `agents.md` | Markdown | No automatic inclusion |

**Problem:**
- No universal standard
- Each tool has own quirks
- Rules don't transfer between tools
- Teams using multiple tools need multiple configurations

---

### 2. File Exclusion vs Rule Inclusion

**Sources:**
- [Google Developers - .aiexclude](https://developers.google.com/gemini-code-assist/docs/create-aiexclude-file)
- [GitHub Docs - Content Exclusion](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot)

**Different approaches:**
- **Exclusion**: Tell AI what NOT to read (`.aiexclude`, `.gitignore`)
- **Inclusion**: Tell AI what rules TO follow (`agents.md`, `.cursorrules`)

**Observation:**
- Exclusion generally more reliable than inclusion
- AI better at ignoring files than following rules
- Suggests fundamental architecture issue

---

## Token Economics of Rule Files

### Current Approach: Always-Loaded Context

**Typical Setup:**
```
Every AI interaction includes:
- agents.md (5,000-15,000 tokens)
- Project rules (2,000-5,000 tokens)
- Context files (varies)
```

**Cost Calculation Example:**

Assumptions:
- 10 developers
- 100 AI requests per day per developer
- 10,000 tokens of coding standards

**Scenario 1: All requests load rules**
```
10 devs × 100 requests × 10,000 tokens = 10,000,000 tokens/day
At $0.015 per 1K tokens (Claude) = $150/day = $4,500/month
```

**Scenario 2: Only 30% need rules**
```
10 devs × 30 requests × 10,000 tokens = 3,000,000 tokens/day
At $0.015 per 1K tokens = $45/day = $1,350/month
```

**Waste: $3,150/month** from loading rules when not needed

**But actual waste is higher because:**
- AI often ignores loaded rules anyway
- You're paying for tokens that aren't being used
- Double waste: cost + ineffectiveness

---

## Impact Summary

### Developer Experience
- ❌ Frustration from inconsistent behavior
- ❌ Time wasted manually attaching files
- ❌ Constant monitoring required
- ❌ Loss of trust in AI coding assistants

### Team Productivity
- ❌ Code quality varies based on rule adherence
- ❌ Increased code review overhead
- ❌ More bugs from ignored standards
- ❌ Onboarding complexity

### Cost Impact
- ❌ Wasted tokens from always-loaded rules
- ❌ Wasted tokens from ignored rules (paid but not used)
- ❌ Developer time spent on workarounds
- ❌ Increased technical debt

---

## Research Conclusions

### The Core Problem

**File-based rule systems are fundamentally flawed:**

1. **Passive Inclusion**: Files are hints, not commands
2. **Context Competition**: Rules compete with code for context space
3. **No Enforcement**: AI decides what to follow
4. **Non-Deterministic**: Same config, different results
5. **Tool-Specific**: Rules don't transfer

### Why This Matters

From the original AI-SDLC journey:
- Teams solved 70k-line PR chaos with agents.md
- But created two new problems:
  - **Token inflation** (always loading large rule files)
  - **Reliability crisis** (AI ignores rules anyway)

### The Need for a Better Approach

The research suggests file-based rules are **architectural dead-ends**:
- More configuration complexity doesn't help
- Workarounds are band-aids, not solutions
- Need protocol-level approach, not file-based

**This sets up the case for MCP as a fundamental architectural improvement.**

---

## Sources Referenced

1. **Cursor Forum - agents.md not included in context**  
   https://forum.cursor.com/t/agents-md-not-included-in-ai-context/138480

2. **Cursor Forum - Cursor just ignores rules**  
   https://forum.cursor.com/t/cursor-just-ignores-rules/69188

3. **Cursor Forum - Agent doesn't know rule system**  
   https://forum.cursor.com/t/cursor-agent-does-not-even-know-how-its-own-rule-system-works/138394

4. **Cursor Forum - Procedural Programming**  
   https://forum.cursor.com/t/procedural-programming/132291

5. **Cursor Documentation - Context**  
   https://docs.cursor.com/en/context

6. **GitHub Gist - Cursor Rules Deep Dive**  
   https://gist.github.com/0xdevalias/f40bc5a6f84c4c5ad862e314894b2fa6

7. **Dev.to - Force Cursor to Follow Rules**  
   https://dev.to/ultrawideturbodevs/how-to-force-cursor-ai-agents-into-always-following-project-rules-using-auto-rule-2ilk

8. **Medium - Why AI Agent Ignores You**  
   https://sdrmike.medium.com/cursor-rules-why-your-ai-agent-is-ignoring-you-and-how-to-fix-it-5b4d2ac0b1b0

9. **Google Developers - .aiexclude**  
   https://developers.google.com/gemini-code-assist/docs/create-aiexclude-file

10. **GitHub Docs - Content Exclusion**  
    https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot

---

**Research Date:** October 22, 2025  
**Status:** Complete - Ready for blog synthesis

