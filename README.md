# Agentic AI Unit Test Coverage Optimizer

This repository is the Java Spring Boot sample microservice for the hackathon MVP.

The current version proves the no-cost foundation before any OpenAI or AWS Bedrock API key is used:

- runs JUnit tests
- generates JaCoCo coverage
- creates a simple coverage report
- identifies the weakest class
- prepares a dry-run LLM prompt for future AI-generated tests
- uploads reports through GitHub Actions

## Coverage Improvement Demo

Initial baseline:

- Line coverage: 74.29%
- Branch coverage: 42.86%

After manual AI-mode test generation:

- Line coverage: 88.57%
- Branch coverage: 100.00%
- Improved class: `com.hackathon.orders.OrderDiscountService`

This demonstrates the before/after workflow that will later be automated through an LLM API.

## Local Verification

```bash
./mvnw test
python3 scripts/coverage_summary.py
python3 scripts/ai_test_agent_dry_run.py
./mvnw verify -Pcoverage-check
```

## Documentation

See [docs/README.md](docs/README.md) for architecture diagrams, CI flow, and the future AI agent workflow.
