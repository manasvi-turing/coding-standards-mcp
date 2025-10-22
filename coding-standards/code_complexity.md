---
description: Guidelines for managing code complexity and maintaining readable code
status: active
mandatory: true
---

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