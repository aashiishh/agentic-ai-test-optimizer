package com.hackathon.reports;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ReportControllerTest {

    @Test
    void dashboardDelegatesToReportService() {
        ReportController controller = new ReportController(new ReportService("ai-test-reports"));

        ReportsDashboardResponse response = controller.dashboard();

        assertEquals(4, response.reports().size());
    }

    @Test
    void reportReturnsNotFoundForUnknownId() {
        ReportController controller = new ReportController(new StubReportService());

        ResponseStatusException exception = assertThrows(
                ResponseStatusException.class,
                () -> controller.report("missing")
        );

        assertEquals(HttpStatus.NOT_FOUND, exception.getStatusCode());
    }

    private static class StubReportService extends ReportService {
        StubReportService() {
            super("ai-test-reports");
        }

        @Override
        public ReportsDashboardResponse dashboard() {
            return new ReportsDashboardResponse(List.of(), List.of(), List.of());
        }
    }
}
