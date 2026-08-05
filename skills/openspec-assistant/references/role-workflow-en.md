# Role Collaboration and Workflow Details

This file defines in detail the specific responsibilities and core actions of the three core roles across the different stages of the complete Change lifecycle.

To ensure development standardization, we split the workflow into three core roles, each with distinct duties throughout the Change lifecycle:

## 1. Architect - Intent Alignment, Spec Generation, and Review/Archive Stage

This section specifies the responsibilities the Architect bears at the start and end of the Change lifecycle.

**Responsibilities**: At the start, perform domain modeling and spec definition to ensure requirements are clear; at the end, review the code to ensure the implementation matches the spec.
**Core actions**:

- **Start: Initialize and create**: Run `openspec init --tools none` (first time), then run `openspec new change <change-name>` to open a new milestone/change.
- **Start: Produce spec artifacts**: (Refer to the skill's built-in template `.trae/skills/openspec/templates/v1-mvp/` as a strongly-constrained example)
  - `proposal.md`: Clarify the business goal and scope; must include the `## Why` and `## What Changes` sections.
  - `design.md`: Determine module boundaries and data flow; partition the domain layer, service layer, and infrastructure layer.
  - `specs/<capability>/spec.md`: Define the capability spec. Must use Delta Headers such as `## ADDED Requirements`, including `### Requirement: <title>` and Gherkin-format `#### Scenario: <title>`.
- **Start: Validate specs**: Run `openspec validate <change-name>` to ensure the format is 100% correct; polish and check the Spec quality.
- **End: Code review and archive**: After Developer and QA complete their work, strictly review the generated code against the Spec item by item to ensure it does not deviate from the spec. Once the review passes, respond to `/opsx:archive` or run `openspec archive <change-name>` to merge the change into the main baseline.

## 2. Developer - Spec-Driven Implementation Generation Stage

This section guides the Developer on how to implement code strictly from the spec documents and test cases, establishing a traceability matrix to ensure implementation quality.

**Responsibilities**: Implement business logic strictly following the Spec (models, interface definitions, exception handling) and the test baseline provided by QA; refuse free-form improvisation that deviates from the spec.
**Core actions**:

- **Generate implementation**: Respond to `/opsx:apply` to implement the code. Before generating code, you must read through `proposal.md` and `design.md` first to gain the overall context.
- **Layered mapping and implementation**:
  - **Domain layer (Domain)**: Precisely map the data models in `domain/spec.md` (keep fields, types, and not-null constraints consistent).
  - **Service layer (Service)**: Implement core business rules and use-case orchestration, keeping clear boundaries between modules.
  - **Interface layer (Interface)**: Precisely map the HTTP methods, routes, status codes, and response structures in `api/spec.md`.
  - **Exception handling**: Strictly follow the error-code conventions defined in the Spec (e.g., 400 Bad Request, 409 Conflict) and map them properly at the interface layer.
- **Traceability Matrix**: When writing code, you must reference the corresponding Spec section in comments (e.g., `// Corresponding Spec: POST /api/orders`) to establish strong Spec ↔ Code ↔ Test traceability.
- **Self-verification loop**: Before delivery, you must run the verification scripts written by QA (including smoke tests and unit tests) until all automated tests pass green, ensuring the logic is free of gaps.

## 3. QA (Test Engineer) - Automated Verification Loop Stage

This section clarifies how the QA role transforms spec documents into executable test baselines, achieving test-driven development and self-verification.

**Responsibilities**: As the "contract guardian" of the spec, design and write automated test cases based on the Spec produced by the Architect, verifying the Developer's code from all angles — happy paths, boundary conditions, and exception handling — ultimately delivering objective evidence that "the code works".
**Core actions**:

- **Scenario mapping and test-case design**: Deeply reference the `Scenario` in the Spec (Gherkin-format Given/When/Then) and write the corresponding automated test scripts in the test directory (e.g., `__tests__/`).
  - **Integration tests / smoke tests**: Simulate real user paths to verify cross-module collaboration (e.g., the business loop of add-to-cart -> place order -> deduct inventory).
  - **Unit tests / exception tests**: Write fine-grained cases for pure-function logic and boundary conditions (e.g., insufficient inventory, duplicate orders) to ensure error status codes map correctly.
- **Test-driven development (TDD collaboration)**: Before or in parallel with the Developer's coding, establish performance baselines (e.g., p99 latency) and test skeletons for core logic, providing clear red/green acceptance criteria for development.
- **Test execution and feedback**: After the Developer writes code, run the full test suite. If tests fail (red), provide clear error feedback to drive the Developer to fix the logic, until the system behavior strictly matches the Spec expectations (all green).
