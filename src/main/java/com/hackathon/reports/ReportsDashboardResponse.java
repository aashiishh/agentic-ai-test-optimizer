package com.hackathon.reports;

import java.util.List;

public record ReportsDashboardResponse(
        List<MetricCard> overview,
        List<ReportSummary> reports,
        List<String> highlights
) {
}
