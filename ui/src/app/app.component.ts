import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { ReportService } from './report.service';
import { ReportSummary, ReportsDashboardResponse } from './report.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  dashboard = signal<ReportsDashboardResponse | null>(null);
  selectedReportId = signal<string>('llm-suggestions');
  loading = signal(true);
  error = signal('');

  selectedReport = computed<ReportSummary | null>(() => {
    const dashboard = this.dashboard();
    if (!dashboard) {
      return null;
    }
    return dashboard.reports.find((report) => report.id === this.selectedReportId())
      ?? dashboard.reports[0]
      ?? null;
  });

  constructor(private readonly reportService: ReportService) {
    this.loadDashboard();
  }

  selectReport(report: ReportSummary): void {
    this.selectedReportId.set(report.id);
  }

  refresh(): void {
    this.loadDashboard();
  }

  private loadDashboard(): void {
    this.loading.set(true);
    this.error.set('');
    this.reportService.getDashboard().subscribe({
      next: (dashboard) => {
        this.dashboard.set(dashboard);
        if (!dashboard.reports.some((report) => report.id === this.selectedReportId())) {
          this.selectedReportId.set(dashboard.reports[0]?.id ?? '');
        }
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Unable to load reports from Spring Boot. Start the backend on port 8080 and refresh.');
        this.loading.set(false);
      }
    });
  }
}
