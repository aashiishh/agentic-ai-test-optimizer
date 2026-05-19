# Agentic AI Unit Test Coverage Optimizer

This repository is the Java Spring Boot sample microservice for the hackathon MVP.

The current version proves the no-cost foundation before any OpenAI or AWS Bedrock API key is used:

- runs JUnit tests
- generates JaCoCo coverage
- creates a simple coverage report
- identifies the weakest class
- prepares a dry-run LLM prompt for future AI-generated tests
- uploads reports through GitHub Actions

## Current Baseline

- Line coverage: 74.29%
- Branch coverage: 42.86%
- Weakest class: `com.hackathon.orders.OrderDiscountService`

This intentional coverage gap gives the future AI agent a clear before/after improvement target.

## Local Verification

```bash
./mvnw test
python3 scripts/coverage_summary.py
python3 scripts/ai_test_agent_dry_run.py
```

## Documentation

See [docs/README.md](docs/README.md) for architecture diagrams, CI flow, and the future AI agent workflow.
