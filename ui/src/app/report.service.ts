import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ReportsDashboardResponse } from './report.model';

@Injectable({ providedIn: 'root' })
export class ReportService {
  constructor(private readonly http: HttpClient) {}

  getDashboard(): Observable<ReportsDashboardResponse> {
    return this.http.get<ReportsDashboardResponse>('/api/reports');
  }
}
