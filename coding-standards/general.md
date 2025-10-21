# Coding Guidelines

Adhere to these standards for all generated code.

---

### 1. Key Principles

* **Write simple, readable code** (KISS, Write for the Reviewer).
* **Do not repeat yourself** (DRY).
* **Follow all SOLID principles**.

---

### 2. Quantifiable Metrics

| Metric                    | Guideline   | Hard Limit    | Rationale                                                                   |
| :------------------------ | :---------- | :------------ | :-------------------------------------------------------------------------- |
| **Function Length**       | < 80 lines  | **120 lines** | Promotes SRP; function should fit on one screen.                            |
| **Class / Module Length** | < 400 lines | **600 lines** | Promotes SRP and high cohesion.                                             |
| **Cyclomatic Complexity** | < 7         | **10**        | Measures logical complexity; high values are hard to test and reason about. |
| **Function Parameters**   | < 3         | **4**         | Reduces cognitive load; use an object/struct for more complex data.         |
| **Nesting Depth**         | < 3 levels  | **4 levels**  | Deeply nested code is difficult to read and follow.                         |

---

### 3. Practical Rules

* **Error Handling:** Use specific, structured errors. No empty `catch` blocks.
* **Security:** Sanitize all external inputs. No hardcoded secrets.

---

### 4. Server and Debugging Rules

#### Server Control Scripts

* Always create scripts for **start, stop, and status** of the server.
* Ensure the server runs as a **background process**, so you can interact with it using tools like **curl** or **wget** to test API calls and verify functionality.

#### Debugging Endpoint

* Implement a dedicated **debug/logging endpoint** in the backend.
* This endpoint should allow the frontend to **send logs or debugging information** to the backend, so you can easily **inspect, console log, and evaluate behavior** during development.

---

### 5. Environment and Dependency Management

#### Python Projects

* Always initialize environments with **`uv init`**.
* Add dependencies with **`uv add <package>`**.
* Run code using **`uv run <command>`**.
* Treat **`uv` as the standard virtual environment manager**; no raw `pip install` or global installs.

#### Node.js Projects

* Always use **Yarn** as the package manager.
* Install dependencies with **`yarn add <package>`**.
* Run scripts with **`yarn <script>`**.
* Avoid mixing **npm** and **yarn** to ensure deterministic builds.

---