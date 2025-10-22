---
description: Node.js coding standards, patterns, and best practices
status: active
---

# Node.js Coding Standards

[Template - Fill in your Node.js coding standards here]

## Project Structure
- Organize by feature/module
- Separate concerns
- Use proper middleware

## Best Practices
- Handle errors properly
- Use async/await
- Validate input data

## Security
- Sanitize user input
- Use environment variables
- Implement rate limiting

## Performance
- Use connection pooling
- Implement caching
- Optimize database queries

## Environment and Dependency Management

* Always use **Yarn** as the package manager.
* Install dependencies with **`yarn add <package>`**.
* Run scripts with **`yarn <script>`**.
* Avoid mixing **npm** and **yarn** to ensure deterministic builds.