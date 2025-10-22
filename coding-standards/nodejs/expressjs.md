---
description: Node.js + Express.js coding standards, patterns, and best practices
status: active
---

# Node.js + Express.js Coding Standards

## 1. Objective
Establish a **consistent, readable, and scalable** coding framework for Express.js projects based on a **top-down design** and **builder-style initialization** pattern.

This ensures that:
- The application’s **structure is clear from entrypoint downward**.
- Business logic and routes are **modular and easily testable**.
- **Middleware, routes, and dependencies** are loaded declaratively and predictably.

---

## 2. Architectural Mind Map

**Top-Down Flow**

```
server.js (entrypoint)
└── ApplicationBuilder
    ├── addConfig()
    ├── addMiddleware()
    ├── addRoutes()
    ├── addErrorHandlers()
    └── build()
        ├── Express app initialized
        ├── Middleware applied
        ├── Routes registered
        └── App returned
```

**Code Layers**
- `server.js` → Application initialization (top-level builder).
- `app/routes/` → Route definitions grouped by domain.
- `app/services/` → Business logic and controllers.
- `app/models/` → Data models (Sequelize, Mongoose, or TypeScript interfaces).
- `app/config/` → Configs, environment variables, settings.
- `app/middleware/` → Custom middleware (logging, auth, error handling).
- `app/utils/` → Shared utilities (logger, validators, helpers).

---

## 3. Folder Structure Standard

```plaintext
project-root/
│
├── app/
│   ├── config/
│   │   ├── index.js
│   │   ├── settings.js
│   │   └── env.js
│   │
│   ├── middleware/
│   │   ├── authMiddleware.js
│   │   ├── errorHandler.js
│   │   └── logger.js
│   │
│   ├── routes/
│   │   ├── userRoutes.js
│   │   ├── authRoutes.js
│   │   └── index.js
│   │
│   ├── services/
│   │   ├── userService.js
│   │   └── authService.js
│   │
│   ├── models/
│   │   ├── userModel.js
│   │   └── authModel.js
│   │
│   ├── utils/
│   │   └── logger.js
│   │
│   └── builder.js
│
└── server.js
````

---

## 4. Top-Down Application Pattern

### 4.1 server.js

```javascript
const { ApplicationBuilder } = require('./app/builder');

const app = new ApplicationBuilder()
  .addConfig()
  .addMiddleware()
  .addRoutes()
  .addErrorHandlers()
  .build();

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

---

### 4.2 builder.js

```javascript
const express = require('express');
const { userRoutes, authRoutes } = require('./routes');
const { registerMiddleware } = require('./middleware');
const { settings } = require('./config');

class ApplicationBuilder {
  constructor() {
    this.app = null;
  }

  addConfig() {
    this.app = express();
    this.app.set('appName', settings.APP_NAME);
    return this;
  }

  addMiddleware() {
    registerMiddleware(this.app);
    return this;
  }

  addRoutes() {
    this.app.use('/users', userRoutes);
    this.app.use('/auth', authRoutes);
    return this;
  }

  addErrorHandlers() {
    const { errorHandler } = require('./middleware/errorHandler');
    this.app.use(errorHandler);
    return this;
  }

  build() {
    return this.app;
  }
}

module.exports = { ApplicationBuilder };
```

---

## 5. Route Definition Standard

Each route file must:

* Export a **router object**.
* Group related endpoints logically.
* Keep routes concise (<= 100 lines recommended).
* Delegate logic to **service layer**.

```javascript
// app/routes/userRoutes.js
const express = require('express');
const { UserService } = require('../services/userService');

const router = express.Router();

router.post('/', async (req, res, next) => {
  try {
    const result = await UserService.createUser(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
```

---

## 6. Service Layer Convention

* Encapsulate business logic.
* Avoid direct DB/API calls from routes.
* Accept dependencies for DB/cache/auth via injection.

```javascript
// app/services/userService.js
class UserService {
  static async createUser(data) {
    // Example logic
    return { id: 1, name: data.name };
  }
}

module.exports = { UserService };
```

---

## 7. Configuration & Environment

Centralize configuration under `app/config/settings.js`:

```javascript
require('dotenv').config();

const settings = {
  APP_NAME: process.env.APP_NAME || 'ExpressApp',
  VERSION: process.env.VERSION || '1.0.0',
  ENV: process.env.NODE_ENV || 'development',
};

module.exports = { settings };
```

---

## 8. Middleware & Utilities

### Middleware Registration

```javascript
// app/middleware/index.js
const cors = require('cors');
const { requestLogger } = require('./logger');

function registerMiddleware(app) {
  app.use(cors());
  app.use(express.json());
  app.use(requestLogger);
}

module.exports = { registerMiddleware };
```

### Logger Utility

```javascript
// app/utils/logger.js
function requestLogger(req, res, next) {
  console.log(`${req.method} ${req.url}`);
  next();
}

module.exports = { requestLogger };
```

---

## 9. Error Handling Standard

```javascript
// app/middleware/errorHandler.js
function errorHandler(err, req, res, next) {
  console.error(err.stack);
  res.status(500).json({ message: 'Internal Server Error' });
}

module.exports = { errorHandler };
```

---

## 10. Testing & Maintainability

* Use **Jest** or **Mocha + Chai** for testing.
* Each route and service should have corresponding tests under `/tests`.
* Test **builder initialization** to ensure middleware and routes load properly.

```bash
npm run test
```

---

## 11. Key Coding Practices

| Principle                  | Rule                                                          |
| -------------------------- | ------------------------------------------------------------- |
| **Top-Down Readability**   | `server.js` must fully describe the system’s setup path.      |
| **Builder Pattern**        | App setup actions chained in a single builder.                |
| **Separation of Concerns** | Routes → Services → Models → Configs.                         |
| **Declarative Configs**    | No hard-coded values in routes/services.                      |
| **Dependency Injection**   | All external systems injected, not imported directly.         |
| **Extensibility**          | Adding new routes or middleware requires minimal code change. |

---

## 12. Future Enhancements

* Auto-discover and load routes dynamically.
* Add health-check endpoints in builder (`.addHealthCheck()`).
* Integrate structured JSON logging.
* Add plugin/extension points (`.addPlugins()`) for auth, caching, analytics.
* Generate API documentation (Swagger/OpenAPI) automatically.

---

## 13. Summary

* **Top-down entrypoint (`server.js`) defines full app flow.**
* **Builder encapsulates construction steps** for easy readability.
* **Routes, services, configs, and middleware** are modular and discoverable.
* **Consistency, clarity, and testability** are prioritized.
* Supports **scalability, maintainability, and CI/CD pipelines**.

---

### References

* [Express.js Official Docs](https://expressjs.com/)
* [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
* [Jest Testing](https://jestjs.io/)
* [Middleware Pattern in Express](https://expressjs.com/en/guide/writing-middleware.html)
---