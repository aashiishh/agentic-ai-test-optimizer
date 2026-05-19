#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path


REPORT_DIR = Path("ai-test-reports")
COVERAGE_SUMMARY = REPORT_DIR / "coverage-summary.md"
MANUAL_INSTRUCTIONS = REPORT_DIR / "manual-agent-instructions.md"
BEFORE_SNAPSHOT = REPORT_DIR / "manual-agent-before.json"
GITHUB_STEP_SUMMARY = os.environ.get("GITHUB_STEP_SUMMARY")
SUMMARY_FILE = REPORT_DIR / "github-actions-summary.md"


def read_text(path):
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def find_metric(content, label):
    match = re.search(rf"- {re.escape(label)}: (.+)", content)
    return match.group(1).strip() if match else "N/A"


def load_target():
    if BEFORE_SNAPSHOT.exists():
        data = json.loads(BEFORE_SNAPSHOT.read_text(encoding="utf-8"))
        return data.get("target", {})

    instructions = read_text(MANUAL_INSTRUCTIONS)
    class_match = re.search(r"- Class: `(.+)`", instructions)
    source_match = re.search(r"- Source: `(.+)`", instructions)
    test_match = re.search(r"- Test: `(.+)`", instructions)
    return {
        "class_name": class_match.group(1) if class_match else "N/A",
        "source": source_match.group(1) if source_match else "N/A",
        "test": test_match.group(1) if test_match else "N/A",
    }


def build_summary():
    coverage = read_text(COVERAGE_SUMMARY)
    target = load_target()

    line = find_metric(coverage, "Line coverage")
    branch = find_metric(coverage, "Branch coverage")
    instruction = find_metric(coverage, "Instruction coverage")

    return "\n".join([
        "# Agentic AI Test Optimizer Summary",
        "",
        "## Coverage",
        "",
        f"- Line coverage: {line}",
        f"- Branch coverage: {branch}",
        f"- Instruction coverage: {instruction}",
        "",
        "## Selected AI Target",
        "",
        f"- Class: `{target.get('class_name', 'N/A')}`",
        f"- Source: `{target.get('source', 'N/A')}`",
        f"- Test: `{target.get('test', 'N/A')}`",
        "",
        "## Generated Artifacts",
        "",
        "- `ai-test-reports/coverage-summary.md`",
        "- `ai-test-reports/manual-agent-instructions.md`",
        "- `ai-test-reports/llm-test-generation-prompt.md`",
        "- `target/site/jacoco/index.html`",
        "",
        "## Next Manual AI Step",
        "",
        "1. Download the workflow artifact.",
        "2. Open `ai-test-reports/llm-test-generation-prompt.md`.",
        "3. Paste it into ChatGPT Pro.",
        "4. Add or update the generated JUnit test file.",
        "5. Run `python3 scripts/ai_test_agent.py --mode manual --phase verify`.",
        "",
    ])


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    summary = build_summary()
    SUMMARY_FILE.write_text(summary, encoding="utf-8")

    if GITHUB_STEP_SUMMARY:
        with Path(GITHUB_STEP_SUMMARY).open("a", encoding="utf-8") as file:
            file.write(summary)

    print(f"Wrote {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
