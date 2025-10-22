---
description: Essential development process guidelines for documentation, code tracking, and project organization
status: active
mandatory: false
---

# Development Process & Documentation Standards

## 1. Project Documentation Structure

### **MUST HAVE: Wiki Folder**

Every project MUST include a `wiki/` folder at the root level with the following structure:

```
project-root/
├── wiki/
│   ├── index.md                    # Central hub with links to all docs
│   ├── technical-details/          # Function registry and technical specs
│   │   ├── function-registry.json  # Master registry of all functions
│   │   ├── api-endpoints.md        # API documentation
│   │   └── architecture.md         # System architecture
│   ├── guides/                     # How-to guides and tutorials
│   │   ├── setup.md
│   │   ├── deployment.md
│   │   └── troubleshooting.md
│   ├── decisions/                  # Architecture Decision Records (ADRs)
│   │   ├── 001-database-choice.md
│   │   └── 002-auth-strategy.md
│   ├── changelog/                  # Detailed change logs
│   │   └── 2025-10.md
│   └── notes/                      # Development notes and TODOs
│       └── pending-improvements.md
├── src/
└── tests/
```

### **Index.md - The Central Hub**

The `wiki/index.md` MUST:
- Link to ALL documentation files
- Be updated whenever a new document is created
- Include a table of contents
- Provide quick navigation to key resources

**Template:**
```markdown
# Project Wiki

## 📚 Quick Links
- [Setup Guide](guides/setup.md)
- [Architecture Overview](technical-details/architecture.md)
- [API Documentation](technical-details/api-endpoints.md)
- [Function Registry](technical-details/function-registry.json)

## 📖 Guides
- [Setup & Installation](guides/setup.md)
- [Deployment Process](guides/deployment.md)
- [Troubleshooting](guides/troubleshooting.md)

## 🏗️ Technical Details
- [System Architecture](technical-details/architecture.md)
- [Function Registry](technical-details/function-registry.json)
- [Database Schema](technical-details/database-schema.md)

## 🎯 Architecture Decisions
- [ADR 001: Database Choice](decisions/001-database-choice.md)
- [ADR 002: Authentication Strategy](decisions/002-auth-strategy.md)

## 📝 Notes & TODOs
- [Pending Improvements](notes/pending-improvements.md)
- [Known Issues](notes/known-issues.md)

## 📅 Changelog
- [October 2025](changelog/2025-10.md)

---
Last Updated: 2025-10-21
```

## 2. Function Documentation & Tracking System

### **Function Signature IDs**

Every function MUST have:
1. A unique Function Signature ID (FSID)
2. Comprehensive docstring
3. Entry in `function-registry.json`

### **Function Format:**

```python
# FSID: USR-AUTH-001
def authenticate_user(username: str, password: str) -> AuthToken:
    """
    Authenticates a user with username and password.
    
    FSID: USR-AUTH-001
    
    Args:
        username (str): User's unique username
        password (str): User's password (will be hashed)
    
    Returns:
        AuthToken: JWT token for authenticated session
    
    Raises:
        InvalidCredentialsError: If username/password is incorrect
        UserLockedError: If account is locked
    
    Dependencies:
        - hash_password() [FSID: SEC-HASH-001]
        - verify_hash() [FSID: SEC-HASH-002]
        - generate_token() [FSID: SEC-TOK-001]
    
    Related:
        See wiki/technical-details/authentication.md
    """
    # Implementation
```

**FSID Naming Convention:**
```
[MODULE]-[CATEGORY]-[NUMBER]

Examples:
- USR-AUTH-001  (User Authentication #1)
- API-PAYM-001  (API Payment #1)
- DB-MIGR-001   (Database Migration #1)
- UTL-LOG-001   (Utility Logging #1)
- SEC-HASH-001  (Security Hashing #1)
```

### **Function Registry (function-registry.json)**

Maintain a JSON file tracking ALL functions:

```json
{
  "functions": [
    {
      "fsid": "USR-AUTH-001",
      "name": "authenticate_user",
      "file": "src/auth/authentication.py",
      "line_number": 45,
      "purpose": "Primary user authentication function handling username/password validation",
      "parameters": {
        "username": "string - User's unique identifier",
        "password": "string - User's plaintext password (hashed internally)"
      },
      "returns": "AuthToken object containing JWT and metadata",
      "dependencies": [
        "SEC-HASH-001",
        "SEC-HASH-002", 
        "SEC-TOK-001"
      ],
      "called_by": [
        "API-AUTH-001",
        "API-LOGIN-001"
      ],
      "regression_impact": "HIGH - Changes affect all login flows, API authentication, and session management",
      "breaking_changes_risk": "HIGH",
      "test_coverage": "95%",
      "last_modified": "2025-10-15",
      "status": "stable",
      "pending_notes": [
        "TODO: Add support for OAuth2",
        "TODO: Implement rate limiting",
        "SECURITY: Review password validation strength"
      ],
      "related_docs": [
        "wiki/technical-details/authentication.md",
        "wiki/guides/security-best-practices.md"
      ],
      "version_history": [
        {
          "date": "2025-10-15",
          "change": "Added account locking after failed attempts",
          "author": "dev@team.com"
        },
        {
          "date": "2025-09-01",
          "change": "Initial implementation",
          "author": "dev@team.com"
        }
      ]
    },
    {
      "fsid": "SEC-HASH-001",
      "name": "hash_password",
      "file": "src/security/crypto.py",
      "line_number": 12,
      "purpose": "Hash passwords using bcrypt with configurable salt rounds",
      "parameters": {
        "password": "string - Plaintext password to hash",
        "salt_rounds": "int - Number of bcrypt rounds (default: 12)"
      },
      "returns": "string - Hashed password",
      "dependencies": [],
      "called_by": [
        "USR-AUTH-001",
        "USR-REG-001",
        "USR-PASS-RESET-001"
      ],
      "regression_impact": "CRITICAL - Changes affect all password operations",
      "breaking_changes_risk": "CRITICAL",
      "test_coverage": "100%",
      "last_modified": "2025-08-20",
      "status": "stable",
      "pending_notes": [
        "SECURITY: Consider migrating to Argon2"
      ],
      "related_docs": [
        "wiki/technical-details/security.md"
      ],
      "version_history": [
        {
          "date": "2025-08-20",
          "change": "Increased default salt rounds from 10 to 12",
          "author": "security@team.com"
        }
      ]
    }
  ],
  "metadata": {
    "last_updated": "2025-10-21",
    "total_functions": 2,
    "high_risk_functions": 2,
    "coverage_average": "97.5%"
  }
}
```

## 3. Regression Impact Levels

Define impact levels for every function:

| Level | Description | Examples |
|-------|-------------|----------|
| **CRITICAL** | Breaking this breaks the entire system | Authentication, database connections, core APIs |
| **HIGH** | Breaking this breaks major features | Payment processing, user management, email system |
| **MEDIUM** | Breaking this breaks specific features | Notifications, analytics, search |
| **LOW** | Breaking this has minimal impact | UI helpers, formatting utilities, logging |

## 4. DO's and DON'Ts

### **✅ DO:**

#### Documentation
- ✅ **Create wiki/ folder** in every project
- ✅ **Update index.md** when adding ANY new document
- ✅ **Assign FSID** to every function
- ✅ **Maintain function-registry.json** as source of truth
- ✅ **Document dependencies** between functions
- ✅ **Track regression impact** for all critical functions
- ✅ **Write Architecture Decision Records (ADRs)** for major choices
- ✅ **Keep changelog** updated monthly
- ✅ **Add inline comments** for complex logic
- ✅ **Link code to wiki docs** in function docstrings

#### Code Organization
- ✅ **Use consistent FSID naming** across the project
- ✅ **Group related functions** by FSID prefix
- ✅ **Version control** the function registry
- ✅ **Review pending notes** weekly
- ✅ **Mark deprecated functions** clearly with FSID

#### Process
- ✅ **Update function registry BEFORE merging** code
- ✅ **Run dependency check** before modifying high-impact functions
- ✅ **Document breaking changes** immediately
- ✅ **Cross-reference** between code, tests, and wiki
- ✅ **Backup function registry** before major refactors

### **❌ DON'T:**

- ❌ **Skip wiki folder** - "We'll add it later" never happens
- ❌ **Forget to update index.md** - Leads to orphaned docs
- ❌ **Duplicate FSIDs** - Causes confusion and tracking issues
- ❌ **Ignore regression impact** - Leads to production bugs
- ❌ **Leave pending notes** indefinitely - Convert to tickets
- ❌ **Delete functions without updating registry** - Breaks dependency tracking
- ❌ **Change critical functions without impact analysis**
- ❌ **Skip docstrings** - "Code is self-documenting" is a myth
- ❌ **Use generic TODOs** - Use pending_notes in registry instead
- ❌ **Keep outdated documentation** - Delete or archive old docs

## 5. Automation Scripts

### **Auto-Update Index Script**

```python
# FSID: UTL-WIKI-001
def update_wiki_index():
    """
    Automatically scans wiki/ folder and updates index.md
    with links to all markdown files.
    
    FSID: UTL-WIKI-001
    
    Run this after creating any new wiki document.
    """
    # Implementation to scan and update index.md
```

### **Function Registry Validator**

```python
# FSID: UTL-REG-001
def validate_function_registry():
    """
    Validates function-registry.json for:
    - Duplicate FSIDs
    - Missing required fields
    - Broken dependency references
    - Outdated line numbers
    
    FSID: UTL-REG-001
    
    Run in CI/CD before deployment.
    """
    # Implementation
```

### **Dependency Graph Generator**

```python
# FSID: UTL-DEP-001
def generate_dependency_graph():
    """
    Creates visual dependency graph from function-registry.json
    showing which functions depend on each other.
    
    FSID: UTL-DEP-001
    
    Outputs: wiki/technical-details/dependency-graph.png
    """
    # Implementation
```

## 6. Integration with Development Workflow

### **Pre-Commit Checklist**
```bash
# Before committing:
1. Added FSID to new functions? ✓
2. Updated function-registry.json? ✓
3. Updated wiki/index.md if added docs? ✓
4. Marked regression impact? ✓
5. Added pending notes? ✓
6. Cross-referenced related docs? ✓
```

### **Code Review Checklist**
```bash
# Reviewers check:
1. FSID present and unique? ✓
2. Function registry entry complete? ✓
3. Regression impact assessed? ✓
4. Dependencies documented? ✓
5. Wiki docs updated? ✓
6. Breaking changes flagged? ✓
```

### **CI/CD Integration**
```yaml
# .github/workflows/validate-docs.yml
name: Validate Documentation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Function Registry
        run: python scripts/validate_registry.py
      
      - name: Check FSID Uniqueness
        run: python scripts/check_fsid_duplicates.py
      
      - name: Verify Wiki Index
        run: python scripts/verify_wiki_index.py
      
      - name: Generate Dependency Graph
        run: python scripts/generate_dep_graph.py
```

## 7. Benefits of This System

### **For Developers:**
- ✅ Know exactly what breaks when you change a function
- ✅ Find all related code instantly via FSID
- ✅ Understand dependencies without reading entire codebase
- ✅ Track TODOs systematically, not in scattered comments

### **For Teams:**
- ✅ Onboard new developers faster with comprehensive docs
- ✅ Review changes with confidence (impact is documented)
- ✅ Reduce production bugs from unexpected side effects
- ✅ Maintain institutional knowledge even when people leave

### **For Projects:**
- ✅ Self-documenting codebase
- ✅ Easier refactoring (know all dependencies)
- ✅ Better test coverage planning (high-impact functions prioritized)
- ✅ Audit trail of all changes and decisions

## 8. Real-World Example

### **Before (Chaotic):**
```python
def process_payment(amount, user_id):
    # TODO: add error handling
    # NOTE: this might break if currency changes
    # FIXME: check with Bob about tax calculation
    pass
```

**Problems:**
- No unique identifier
- TODOs scattered and forgotten
- Impact unknown
- Dependencies unclear
- No central tracking

### **After (Systematic):**

**Code:**
```python
# FSID: API-PAYM-001
def process_payment(amount: Decimal, user_id: str, currency: str = "USD") -> PaymentResult:
    """
    Process a payment transaction for a user.
    
    FSID: API-PAYM-001
    
    Args:
        amount: Payment amount (must be positive)
        user_id: Unique user identifier
        currency: ISO currency code (default: USD)
    
    Returns:
        PaymentResult with transaction_id and status
    
    Dependencies:
        - validate_amount() [FSID: VAL-AMT-001]
        - calculate_tax() [FSID: FIN-TAX-001]
        - charge_gateway() [FSID: EXT-STRP-001]
    
    Related: wiki/technical-details/payment-flow.md
    """
    pass
```

**Registry Entry:**
```json
{
  "fsid": "API-PAYM-001",
  "name": "process_payment",
  "regression_impact": "CRITICAL",
  "pending_notes": [
    "TODO: Add retry logic for failed transactions - [Ticket #234]",
    "TODO: Support multi-currency - [Ticket #235]",
    "DISCUSS: Tax calculation accuracy with Finance team"
  ],
  "called_by": ["API-CHECKOUT-001", "API-SUBSCR-001"]
}
```

**Benefits:**
- ✅ Tracked in central system
- ✅ Impact clearly marked
- ✅ TODOs linked to tickets
- ✅ Dependencies documented
- ✅ Easy to find related code

## 9. Quick Start Guide

### **For New Projects:**
```bash
# 1. Create wiki structure
mkdir -p wiki/{technical-details,guides,decisions,changelog,notes}

# 2. Initialize index.md
echo "# Project Wiki" > wiki/index.md

# 3. Create function registry
echo '{"functions": [], "metadata": {}}' > wiki/technical-details/function-registry.json

# 4. Add to version control
git add wiki/
git commit -m "Initialize wiki structure"
```

### **For Existing Projects:**
```bash
# 1. Create wiki folder
mkdir -p wiki/technical-details

# 2. Generate function registry from existing code
python scripts/generate_initial_registry.py

# 3. Review and enrich with metadata
# Edit wiki/technical-details/function-registry.json

# 4. Start using FSIDs for new functions
```

---

## Summary

**This system ensures:**
1. 📚 **All documentation is centralized and linked** (wiki/)
2. 🔍 **Every function is tracked and identifiable** (FSID)
3. 📊 **Impact of changes is known before making them** (regression_impact)
4. 📝 **TODOs and notes are systematically managed** (pending_notes)
5. 🔗 **Dependencies are clear and documented** (function registry)

**Result:** Maintainable, well-documented codebase that scales with your team! 🚀

