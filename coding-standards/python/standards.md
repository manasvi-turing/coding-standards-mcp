---
description: Python coding standards, style guide, and best practices
---

# Python Coding Standards

[Template - Fill in your Python coding standards here]

## Style Guide
- Follow PEP 8
- Use type hints
- Document functions with docstrings

## Best Practices
- Use virtual environments
- Keep dependencies minimal
- Write unit tests

## Code Structure
- Organize code into modules
- Use proper package structure
- Separate concerns

## Common Patterns
- Context managers for resources
- List comprehensions over loops
- Generator expressions for large datasets

## Environment and Dependency Management

* Always initialize environments with **`uv init`**.
* Add dependencies with **`uv add <package>`**.
* Run code using **`uv run <command>`**.
* Treat **`uv` as the standard virtual environment manager**; no raw `pip install` or global installs.