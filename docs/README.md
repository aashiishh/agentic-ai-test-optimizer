# Agentic AI Unit Test Coverage Optimizer

## MVP Goal

Build a GitHub Actions based agent workflow for a Java Spring Boot microservice that measures current unit test coverage, identifies weak classes, and prepares the system for AI-generated JUnit tests.

The current phase intentionally runs without an LLM API key. It establishes the engineering foundation: tests, coverage, reporting, and CI.

## Phase 0: Before LLM API Usage

- Java Spring Boot sample service is available.
- JUnit 5 tests can run locally and in CI.
- JaCoCo generates coverage reports.
- A baseline Markdown report is generated under `ai-test-reports/`.
- A dry-run AI agent generates the future LLM prompt without calling any paid API.
- GitHub Actions uploads coverage artifacts.
- The LLM test-generation step is represented as a future extension point.

## High-Level Architecture

```mermaid
flowchart LR
    DEV[Developer Push or PR] --> GHA[GitHub Actions]
    GHA --> TEST[Maven Test Runner]
    TEST --> JACOCO[JaCoCo Coverage]
    JACOCO --> REPORT[Baseline Report Generator]
    REPORT --> DRYRUN[AI Agent Dry Run]
    DRYRUN --> ARTIFACT[GitHub Artifact]
    DRYRUN --> FUTURE[Future AI Test Agent]
    FUTURE -. requires API key later .-> LLM[LLM Provider]
    FUTURE -. opens PR later .-> PR[Generated Test PR]
```

## CI Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant Maven as Maven/JUnit
    participant Report as Report Generator

    Dev->>GH: Push code or open PR
    GH->>CI: Trigger workflow
    CI->>Maven: Run ./mvnw test
    Maven-->>CI: Test result and JaCoCo files
    CI->>Report: Parse target/site/jacoco/jacoco.csv
    Report-->>CI: ai-test-reports/coverage-summary.md
    CI->>Report: Generate dry-run LLM prompt
    CI-->>GH: Upload coverage artifact
```

## Future Agent Workflow

```mermaid
flowchart TD
    A[Detect changed Java files] --> B[Find related tests]
    B --> C[Read source, tests, coverage gaps]
    C --> D[Generate LLM prompt]
    D --> E[Call LLM API]
    E --> F[Write generated JUnit tests]
    F --> G[Run Maven tests]
    G --> H{Tests pass?}
    H -- No --> I[Send failures back for repair]
    I --> E
    H -- Yes --> J[Run JaCoCo again]
    J --> K{Coverage improved?}
    K -- Yes --> L[Open PR with tests and report]
    K -- No --> M[Publish suggestions only]
```

## Local Commands

Run tests and generate JaCoCo:

```bash
./mvnw test
```

Generate the baseline AI report:

```bash
python3 scripts/coverage_summary.py
```

Generate the no-cost AI agent dry run:

```bash
python3 scripts/ai_test_agent_dry_run.py
```

Run the repeatable manual AI agent flow:

```bash
python3 scripts/ai_test_agent.py --mode manual --phase prepare
python3 scripts/ai_test_agent.py --mode manual --phase verify
```

Optional strict 80 percent coverage gate. In the current baseline this may fail, which is useful for the demo because the future AI agent should raise coverage above this threshold:

```bash
./mvnw verify -Pcoverage-check
```

## Next Milestone

The manual AI-mode flow is now proven: the dry-run prompt identified a weak class, additional JUnit tests were added, and the project passed the strict 80 percent coverage gate.

Next, add the AI test agent provider interface. The first paid provider can be OpenAI API or AWS Bedrock, while the current manual provider keeps the same workflow available with ChatGPT Pro.
