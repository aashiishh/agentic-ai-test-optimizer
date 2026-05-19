#!/usr/bin/env python3
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


JACOCO_CSV = Path("target/site/jacoco/jacoco.csv")
REPORT_DIR = Path("ai-test-reports")
PROMPT_FILE = REPORT_DIR / "llm-test-generation-prompt.md"
INSTRUCTIONS_FILE = REPORT_DIR / "manual-agent-instructions.md"
RESULT_FILE = REPORT_DIR / "manual-agent-result.md"
SNAPSHOT_FILE = REPORT_DIR / "manual-agent-before.json"


def ratio(covered, missed):
    total = covered + missed
    return None if total == 0 else covered / total


def percent(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def points(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}"


def run(command):
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)


def capture(command):
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def class_to_source_path(class_name):
    return Path("src/main/java") / Path(*class_name.split(".")).with_suffix(".java")


def class_to_test_path(class_name):
    return Path("src/test/java") / Path(*f"{class_name}Test".split(".")).with_suffix(".java")


def source_path_to_class_name(path):
    source_root = Path("src/main/java")
    try:
        relative = Path(path).relative_to(source_root)
    except ValueError:
        return None

    if relative.suffix != ".java":
        return None

    return ".".join(relative.with_suffix("").parts)


def read_text(path):
    if not path.exists():
        return f"// File not found: {path}"
    return path.read_text(encoding="utf-8")


def load_coverage():
    if not JACOCO_CSV.exists():
        raise SystemExit(f"JaCoCo CSV not found: {JACOCO_CSV}. Run ./mvnw test first.")

    totals = {
        "line_missed": 0,
        "line_covered": 0,
        "branch_missed": 0,
        "branch_covered": 0,
        "instruction_missed": 0,
        "instruction_covered": 0,
    }
    rows = []

    with JACOCO_CSV.open(newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            line_missed = int(row["LINE_MISSED"])
            line_covered = int(row["LINE_COVERED"])
            branch_missed = int(row["BRANCH_MISSED"])
            branch_covered = int(row["BRANCH_COVERED"])
            instruction_missed = int(row["INSTRUCTION_MISSED"])
            instruction_covered = int(row["INSTRUCTION_COVERED"])

            totals["line_missed"] += line_missed
            totals["line_covered"] += line_covered
            totals["branch_missed"] += branch_missed
            totals["branch_covered"] += branch_covered
            totals["instruction_missed"] += instruction_missed
            totals["instruction_covered"] += instruction_covered

            class_name = f'{row["PACKAGE"]}.{row["CLASS"]}'
            rows.append({
                "class_name": class_name,
                "line": ratio(line_covered, line_missed),
                "branch": ratio(branch_covered, branch_missed),
                "source": str(class_to_source_path(class_name)),
                "test": str(class_to_test_path(class_name)),
            })

    summary = {
        "line": ratio(totals["line_covered"], totals["line_missed"]),
        "branch": ratio(totals["branch_covered"], totals["branch_missed"]),
        "instruction": ratio(totals["instruction_covered"], totals["instruction_missed"]),
    }
    weakest = sorted(rows, key=lambda item: (item["line"] or 0, item["branch"] or 1))
    return summary, weakest


def get_changed_class_names(base_ref):
    commands = []
    if base_ref and not set(base_ref) == {"0"}:
        commands.append(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
        commands.append(["git", "diff", "--name-only", base_ref, "HEAD"])

    commands.append(["git", "diff", "--name-only", "HEAD~1", "HEAD"])

    for command in commands:
        try:
            output = capture(command)
        except subprocess.CalledProcessError:
            continue

        class_names = {
            class_name
            for line in output.splitlines()
            if (class_name := source_path_to_class_name(line))
        }
        if class_names:
            return class_names

    return set()


def select_target(weakest, scope, base_ref):
    if scope == "all":
        return weakest[0], []

    changed_class_names = get_changed_class_names(base_ref)
    changed_targets = [
        item for item in weakest
        if item["class_name"] in changed_class_names
    ]

    if changed_targets:
        return changed_targets[0], sorted(changed_class_names)

    print("No changed covered Java classes found; falling back to all covered classes.", file=sys.stderr)
    return weakest[0], sorted(changed_class_names)


def build_prompt(target):
    source_path = Path(target["source"])
    test_path = Path(target["test"])

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
- Source path: `{source_path}`
- Test path: `{test_path}`

## Source Code

```java
{read_text(source_path)}
```

## Existing Test Code

```java
{read_text(test_path)}
```
"""


def write_prepare_artifacts(summary, target, scope, changed_class_names):
    REPORT_DIR.mkdir(exist_ok=True)
    PROMPT_FILE.write_text(build_prompt(target), encoding="utf-8")
    SNAPSHOT_FILE.write_text(json.dumps({
        "summary": summary,
        "target": target,
        "scope": scope,
        "changed_classes": changed_class_names,
    }, indent=2), encoding="utf-8")

    instructions = [
        "# Manual AI Agent Instructions",
        "",
        "This mode uses ChatGPT Pro manually and does not call any paid API from CI/CD.",
        "",
        "## Selected Target",
        "",
        f"- Scope: `{scope}`",
        f"- Class: `{target['class_name']}`",
        f"- Source: `{target['source']}`",
        f"- Test: `{target['test']}`",
        f"- Line coverage: {percent(target['line'])}",
        f"- Branch coverage: {percent(target['branch'])}",
        "",
        "## Changed Classes Considered",
        "",
    ]

    if changed_class_names:
        instructions.extend(f"- `{class_name}`" for class_name in changed_class_names)
    else:
        instructions.append("- None detected; the agent fell back to all covered classes.")

    instructions.extend([
        "",
        "## Manual Steps",
        "",
        "1. Open `ai-test-reports/llm-test-generation-prompt.md`.",
        "2. Paste that prompt into ChatGPT Pro.",
        "3. Add the generated JUnit tests to the target test file.",
        "4. Run `python3 scripts/ai_test_agent.py --mode manual --phase verify`.",
        "5. Review `ai-test-reports/manual-agent-result.md`.",
        "",
    ])
    INSTRUCTIONS_FILE.write_text("\n".join(instructions), encoding="utf-8")


def write_verify_artifact(before, after_summary, after_target):
    before_summary = before["summary"]
    before_target = before["target"]

    line_delta = None
    if before_summary["line"] is not None and after_summary["line"] is not None:
        line_delta = after_summary["line"] - before_summary["line"]

    branch_delta = None
    if before_summary["branch"] is not None and after_summary["branch"] is not None:
        branch_delta = after_summary["branch"] - before_summary["branch"]

    result = [
        "# Manual AI Agent Result",
        "",
        "This report compares coverage before and after manually adding AI-suggested tests.",
        "",
        "## Before",
        "",
        f"- Line coverage: {percent(before_summary['line'])}",
        f"- Branch coverage: {percent(before_summary['branch'])}",
        f"- Instruction coverage: {percent(before_summary['instruction'])}",
        f"- Target class: `{before_target['class_name']}`",
        "",
        "## After",
        "",
        f"- Line coverage: {percent(after_summary['line'])}",
        f"- Branch coverage: {percent(after_summary['branch'])}",
        f"- Instruction coverage: {percent(after_summary['instruction'])}",
        f"- Current weakest class: `{after_target['class_name']}`",
        "",
        "## Improvement",
        "",
        f"- Line coverage delta: {points(line_delta)} percentage points",
        f"- Branch coverage delta: {points(branch_delta)} percentage points",
        "",
    ]
    RESULT_FILE.write_text("\n".join(result), encoding="utf-8")


def prepare(scope, base_ref):
    run(["./mvnw", "test"])
    summary, weakest = load_coverage()
    target, changed_class_names = select_target(weakest, scope, base_ref)
    write_prepare_artifacts(summary, target, scope, changed_class_names)
    run(["python3", "scripts/coverage_summary.py"])
    print(f"Wrote {PROMPT_FILE}")
    print(f"Wrote {INSTRUCTIONS_FILE}")
    print(f"Wrote {SNAPSHOT_FILE}")


def verify():
    if not SNAPSHOT_FILE.exists():
        raise SystemExit(f"Before snapshot not found: {SNAPSHOT_FILE}. Run prepare phase first.")

    before = json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
    run(["./mvnw", "test"])
    after_summary, weakest = load_coverage()
    run(["python3", "scripts/coverage_summary.py"])
    write_verify_artifact(before, after_summary, weakest[0])
    print(f"Wrote {RESULT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Agentic unit test coverage optimizer")
    parser.add_argument("--mode", choices=["manual"], default="manual")
    parser.add_argument("--phase", choices=["prepare", "verify"], default="prepare")
    parser.add_argument("--scope", choices=["all", "changed"], default="all")
    parser.add_argument("--base-ref", default=None)
    args = parser.parse_args()

    if args.phase == "prepare":
        prepare(args.scope, args.base_ref)
    else:
        verify()


if __name__ == "__main__":
    main()
