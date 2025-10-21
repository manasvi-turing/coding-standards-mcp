---
description: Best practices for server operations, error handling, security, and process management
---

# Server Operations & Developer Experience

## 1. Error Handling & Security

* **Error Handling:** Use specific, structured errors. No empty `catch` blocks.
* **Error Responses:** Return consistent error format with `status`, `message`, and `details` fields.
* **Security:** Sanitize all external inputs. No hardcoded secrets.
* **Secrets Management:** Use environment variables or secret managers. Never commit `.env` files.

## 2. Server Control & Process Management

* **Control Scripts:** Always create scripts for **start, stop, restart, and status** of the server.
* **Background Process:** Ensure the server runs as a **background process** for easy testing with **curl**, **wget**, or Postman.
* **Process ID File:** Store PID in a `.pid` file for reliable process management.
* **Graceful Shutdown:** Implement proper cleanup (close DB connections, finish pending requests) on SIGTERM/SIGINT.

## 3. Development Experience Essentials

### Health & Monitoring
* **Health Check Endpoint:** Implement `/health` or `/ping` endpoint that returns service status.
* **Status Endpoint:** Add `/status` with detailed info (version, uptime, dependencies status).
* **Readiness Check:** Separate `/ready` endpoint to verify all dependencies (DB, cache, etc.) are available.

### Logging & Debugging
* **Structured Logging:** Use JSON format for logs with timestamp, level, message, and context.
* **Log Levels:** Support DEBUG, INFO, WARN, ERROR with environment-based configuration.
* **Request Logging:** Log all incoming requests with method, path, status code, and duration.
* **Debug Endpoint:** Create `/debug/logs` endpoint to send frontend logs to backend for inspection.
* **Correlation IDs:** Add unique request IDs to trace requests across services.

### Development Tools
* **Hot Reload:** Enable auto-restart on code changes during development (e.g., nodemon, uvicorn --reload).
* **CORS Configuration:** Configure CORS properly with environment-specific settings.
* **Port Management:** Check port availability before starting; provide clear error if port is in use.
* **Environment Modes:** Support explicit `development`, `staging`, and `production` modes.

### API Development
* **API Documentation:** Auto-generate docs (Swagger/OpenAPI for REST, GraphQL Playground).
* **Request Validation:** Validate all inputs at the API boundary with clear error messages.
* **Response Formatting:** Return consistent response structure across all endpoints.
* **Versioning:** Include API version in URL or headers (`/api/v1/...`).

## 4. Local Development Setup

* **Quick Start Script:** Create `setup.sh` or `setup.py` that installs dependencies and sets up environment.
* **Sample Environment:** Provide `.env.example` with all required environment variables documented.
* **Database Seeding:** Include scripts to seed development database with test data.
* **Container Support:** Provide `docker-compose.yml` for local development with all dependencies.
* **Localhost Testing:** Document how to test endpoints locally with example curl commands.

## 5. Operational Best Practices

* **Configuration Management:** Externalize all config; never hardcode URLs, ports, or credentials.
* **Connection Pooling:** Use connection pools for databases and external services.
* **Timeouts:** Set reasonable timeouts for all external calls to prevent hanging.
* **Rate Limiting:** Implement rate limiting to prevent abuse and resource exhaustion.
* **Circuit Breakers:** Add circuit breakers for external service calls to fail fast.
* **Metrics & Telemetry:** Expose basic metrics (requests/sec, error rate, latency percentiles).

