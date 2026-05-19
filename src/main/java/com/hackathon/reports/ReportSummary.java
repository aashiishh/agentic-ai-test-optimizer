package com.hackathon.reports;

import java.util.List;

public record ReportSummary(
        String id,
        String title,
        String type,
        String path,
        boolean available,
        String content,
        List<MetricCard> metrics
) {
}
