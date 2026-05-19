#!/usr/bin/env python3
import csv
from pathlib import Path


JACOCO_CSV = Path("target/site/jacoco/jacoco.csv")
REPORT_DIR = Path("ai-test-reports")
PROMPT_FILE = REPORT_DIR / "llm-test-generation-prompt.md"
PLAN_FILE = REPORT_DIR / "agent-dry-run-plan.md"


def ratio(covered, missed):
    total = covered + missed
    return None if total == 0 else covered / total


def percent(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def class_to_source_path(class_name):
    return Path("src/main/java") / Path(*class_name.split(".")).with_suffix(".java")


def class_to_test_path(class_name):
    return Path("src/test/java") / Path(*f"{class_name}Test".split(".")).with_suffix(".java")


def read_text(path):
    if not path.exists():
        return f"// File not found: {path}"
    return path.read_text(encoding="utf-8")


def load_coverage_rows():
    if not JACOCO_CSV.exists():
        raise SystemExit(f"JaCoCo CSV not found: {JACOCO_CSV}. Run ./mvnw test first.")

    rows = []
    with JACOCO_CSV.open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            class_name = f'{row["PACKAGE"]}.{row["CLASS"]}'
            line = ratio(int(row["LINE_COVERED"]), int(row["LINE_MISSED"]))
            branch = ratio(int(row["BRANCH_COVERED"]), int(row["BRANCH_MISSED"]))
            rows.append({
                "class_name": class_name,
                "line": line,
                "branch": branch,
                "source": class_to_source_path(class_name),
                "test": class_to_test_path(class_name),
            })
    return sorted(rows, key=lambda item: (item["line"] or 0, item["branch"] or 1))


def build_prompt(target):
    source_text = read_text(target["source"])
    test_text = read_text(target["test"])

    return f"""# Unit Test Generation Prompt

You are an expert Java Spring Boot unit test engineer.

## Goal

Generate or improve JUnit 5 tests for the target class so that line and branch coverage improve while preserving existing behavior.

## Rules

- Use JUnit 5.
- Prefer deterministic tests.
- Do not call real AWS services, databases, queues, or network endpoints.
- Do not change production code unless the class is impossible to test safely.
- Keep tests focused on observable behavior.
- Return only Java test code and a short explanation of covered scenarios.

## Current Coverage

- Target class: `{target["class_name"]}`
- Line coverage: {percent(target["line"])}
- Branch coverage: {percent(target["branch"])}
- Source path: `{target["source"]}`
- Test path: `{target["test"]}`

## Source Code

```java
{source_text}
```

## Existing Test Code

```java
{test_text}
```
"""


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    rows = load_coverage_rows()
    target = rows[0]

    prompt = build_prompt(target)
    PROMPT_FILE.write_text(prompt, encoding="utf-8")

    plan = [
        "# AI Test Agent Dry Run Plan",
        "",
        "This dry run does not call an LLM API. It prepares the target context that will be sent to the model in the next phase.",
        "",
        "## Selected Target",
        "",
        f"- Class: `{target['class_name']}`",
        f"- Source: `{target['source']}`",
        f"- Test: `{target['test']}`",
        f"- Line coverage: {percent(target['line'])}",
        f"- Branch coverage: {percent(target['branch'])}",
        "",
        "## Next Automated Phase",
        "",
        "1. Send `llm-test-generation-prompt.md` to the configured LLM provider.",
        "2. Write the returned JUnit test to the target test path.",
        "3. Run `./mvnw test`.",
        "4. Regenerate coverage.",
        "5. Compare before/after metrics.",
        "6. Open a pull request if tests pass and coverage improves.",
        "",
    ]
    PLAN_FILE.write_text("\n".join(plan), encoding="utf-8")

    print(f"Wrote {PLAN_FILE}")
    print(f"Wrote {PROMPT_FILE}")


if __name__ == "__main__":
    main()
