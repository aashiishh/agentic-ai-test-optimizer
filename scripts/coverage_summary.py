#!/usr/bin/env python3
import csv
from pathlib import Path


REPORT_DIR = Path("ai-test-reports")
JACOCO_CSV = Path("target/site/jacoco/jacoco.csv")
SUMMARY = REPORT_DIR / "coverage-summary.md"


def ratio(covered, missed):
    total = covered + missed
    return None if total == 0 else covered / total


def percent(value):
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def main():
    if not JACOCO_CSV.exists():
        raise SystemExit(f"JaCoCo CSV not found: {JACOCO_CSV}")

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

            rows.append({
                "class": f'{row["PACKAGE"]}.{row["CLASS"]}',
                "line": ratio(line_covered, line_missed),
                "branch": ratio(branch_covered, branch_missed),
            })

    REPORT_DIR.mkdir(exist_ok=True)
    lowest = sorted(rows, key=lambda item: (item["line"] or 0, item["branch"] or 1))[:5]

    content = [
        "# AI Test Coverage Report",
        "",
        "This report is generated from JaCoCo coverage data. It can be used for baseline or after-test-generation comparisons.",
        "",
        "## Coverage Summary",
        "",
        f"- Line coverage: {percent(ratio(totals['line_covered'], totals['line_missed']))}",
        f"- Branch coverage: {percent(ratio(totals['branch_covered'], totals['branch_missed']))}",
        f"- Instruction coverage: {percent(ratio(totals['instruction_covered'], totals['instruction_missed']))}",
        "",
        "## Weakest Classes",
        "",
        "| Class | Line Coverage | Branch Coverage |",
        "| --- | ---: | ---: |",
    ]

    for item in lowest:
        content.append(f"| `{item['class']}` | {percent(item['line'])} | {percent(item['branch'])} |")

    content.extend([
        "",
        "## Next Agent Step",
        "",
        "When an LLM API key is available, the agent will read changed source files, generate missing JUnit tests, rerun coverage, and update this report with before/after metrics.",
        "",
    ])

    SUMMARY.write_text("\n".join(content), encoding="utf-8")
    print(f"Wrote {SUMMARY}")


if __name__ == "__main__":
    main()
