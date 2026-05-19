package com.hackathon.reports;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class ReportService {

    private static final Pattern BULLET_METRIC = Pattern.compile("- ([^:]+): ([^\\n]+)");

    private final Path reportDirectory;

    public ReportService(@Value("${app.reports.directory:ai-test-reports}") String reportDirectory) {
        this.reportDirectory = Path.of(reportDirectory);
    }

    public ReportsDashboardResponse dashboard() {
        List<ReportSummary> reports = List.of(
                readReport("coverage", "Coverage Summary", "Coverage", "coverage-summary.md"),
                readReport("llm-suggestions", "LLM Suggestions", "AI Suggestions", "llm-test-suggestions.md"),
                readReport("manual-comparison", "Manual AI Comparison", "Before/After", "manual-ai-comparison.md"),
                readReport("agent-plan", "Agent Dry Run Plan", "Planning", "agent-dry-run-plan.md")
        );

        List<MetricCard> overview = new ArrayList<>();
        findMetric(reports, "coverage", "Line coverage").ifPresent(overview::add);
        findMetric(reports, "coverage", "Branch coverage").ifPresent(overview::add);
        findMetric(reports, "coverage", "Instruction coverage").ifPresent(overview::add);
        overview.add(new MetricCard("Reports available", String.valueOf(reports.stream().filter(ReportSummary::available).count()), "Generated artifacts exposed to UI"));

        List<String> highlights = List.of(
                "Suggest-only LLM mode is working and does not modify code automatically.",
                "Coverage reports are generated from JaCoCo and exposed through Spring Boot.",
                "Next backend milestone is auto-apply mode with verification and PR creation."
        );

        return new ReportsDashboardResponse(overview, reports, highlights);
    }

    public Optional<ReportSummary> reportById(String id) {
        return dashboard().reports().stream()
                .filter(report -> report.id().equals(id))
                .findFirst();
    }

    private Optional<MetricCard> findMetric(List<ReportSummary> reports, String reportId, String label) {
        return reports.stream()
                .filter(report -> report.id().equals(reportId))
                .flatMap(report -> report.metrics().stream())
                .filter(metric -> metric.label().equals(label))
                .findFirst();
    }

    private ReportSummary readReport(String id, String title, String type, String filename) {
        Path path = reportDirectory.resolve(filename);
        if (!Files.exists(path)) {
            return new ReportSummary(id, title, type, path.toString(), false, "", List.of());
        }

        try {
            String content = Files.readString(path);
            return new ReportSummary(id, title, type, path.toString(), true, content, extractMetrics(content));
        } catch (IOException exception) {
            return new ReportSummary(id, title, type, path.toString(), false, "", List.of(
                    new MetricCard("Read error", exception.getClass().getSimpleName(), "Report file could not be loaded")
            ));
        }
    }

    private List<MetricCard> extractMetrics(String content) {
        Map<String, String> details = Map.of(
                "Line coverage", "JaCoCo line coverage",
                "Branch coverage", "JaCoCo branch coverage",
                "Instruction coverage", "JaCoCo instruction coverage",
                "Target class", "Selected class for agent work",
                "Class", "Selected class for agent work",
                "Scope", "Agent selection mode"
        );

        List<MetricCard> metrics = new ArrayList<>();
        Matcher matcher = BULLET_METRIC.matcher(content);
        while (matcher.find()) {
            String label = matcher.group(1).trim();
            if (details.containsKey(label)) {
                String value = matcher.group(2).replace("`", "").trim();
                metrics.add(new MetricCard(label, value, details.get(label)));
            }
        }
        return metrics;
    }
}
