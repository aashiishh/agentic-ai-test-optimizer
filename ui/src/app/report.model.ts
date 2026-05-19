export interface MetricCard {
  label: string;
  value: string;
  detail: string;
}

export interface ReportSummary {
  id: string;
  title: string;
  type: string;
  path: string;
  available: boolean;
  content: string;
  metrics: MetricCard[];
}

export interface ReportsDashboardResponse {
  overview: MetricCard[];
  reports: ReportSummary[];
  highlights: string[];
}
