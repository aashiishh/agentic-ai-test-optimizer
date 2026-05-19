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
python3 scripts/ai_test_agent.py --mode manual --phase prepare
python3 scripts/github_summary.py
./mvnw verify -Pcoverage-check
```

## Run The Local Demo App

Start the Spring Boot app:

```bash
./mvnw spring-boot:run
```

Try the order discount endpoint:

```bash
curl "http://localhost:8080/orders/discount?amount=1000&tier=PLATINUM&coupon=true"
```

Expected response:

```text
750.00
```

More examples:

```bash
curl "http://localhost:8080/orders/discount?amount=1000&tier=GOLD&coupon=false"
curl "http://localhost:8080/orders/discount?amount=999.99&tier=SILVER&coupon=true"
```

## Manual AI Agent Mode

Prepare the prompt for ChatGPT Pro:

```bash
python3 scripts/ai_test_agent.py --mode manual --phase prepare
```

Prefer changed production classes when Git history is available:

```bash
python3 scripts/ai_test_agent.py --mode manual --phase prepare --scope changed --base-ref HEAD~1
```

After adding the generated tests, verify coverage improvement:

```bash
python3 scripts/ai_test_agent.py --mode manual --phase verify
```

The CI workflow also generates `ai-test-reports/github-actions-summary.md`, which appears directly in the GitHub Actions run summary and can be posted as a PR comment.

## LLM Suggest-Only Mode

This mode calls an OpenAI-compatible chat completions API and writes recommendations to `ai-test-reports/llm-test-suggestions.md`. It does not change source code or test code automatically.

Required from your side:

- `LLM_API_KEY`: API key from the selected provider
- `LLM_MODEL`: model name to use, optional because the script has a default
- `LLM_BASE_URL`: API base URL, optional for OpenAI because the script has a default

Run:

```bash
export LLM_API_KEY="your-api-key"
export LLM_MODEL="gpt-4o-mini"
python3 scripts/ai_test_agent.py --mode llm --phase suggest --scope changed --base-ref HEAD~1
```

## Documentation

See [docs/README.md](docs/README.md) for architecture diagrams, CI flow, and the future AI agent workflow.
