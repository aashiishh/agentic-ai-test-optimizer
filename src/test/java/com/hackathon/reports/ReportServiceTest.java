package com.hackathon.reports;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ReportServiceTest {

    @TempDir
    Path reportDirectory;

    @Test
    void dashboardReadsCoverageReportMetrics() throws IOException {
        Files.writeString(reportDirectory.resolve("coverage-summary.md"), """
                # AI Test Coverage Report

                ## Coverage Summary

                - Line coverage: 90.24%
                - Branch coverage: 100.00%
                - Instruction coverage: 92.45%
                """);

        ReportsDashboardResponse dashboard = new ReportService(reportDirectory.toString()).dashboard();

        assertEquals(4, dashboard.overview().size());
        assertEquals("90.24%", dashboard.overview().get(0).value());
        assertTrue(dashboard.reports().stream().anyMatch(report -> report.id().equals("coverage") && report.available()));
    }

    @Test
    void reportByIdReturnsEmptyForUnknownReport() {
        ReportService reportService = new ReportService(reportDirectory.toString());

        assertTrue(reportService.reportById("missing").isEmpty());
    }
}
