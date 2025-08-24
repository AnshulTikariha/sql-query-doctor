import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { QueryAnalysisResult } from '../models/query-analysis.model';

@Injectable({
  providedIn: 'root'
})
export class QueryAnalysisService {
  private readonly apiUrl = 'http://localhost:5001';
  private readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    })
  };

  constructor(private http: HttpClient) {}

  /**
   * Analyzes a SQL query by sending it to the backend API
   * @param query The SQL query to analyze
   * @returns Observable of the analysis result
   */
  analyzeQuery(query: string): Observable<QueryAnalysisResult> {
    const payload = { query };
    return this.http.post<QueryAnalysisResult>(
      `${this.apiUrl}/analyze-query`,
      payload,
      this.httpOptions
    );
  }

  /**
   * Health check endpoint to verify backend connectivity
   * @returns Observable of the health status
   */
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }
} 