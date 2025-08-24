import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatExpansionModule } from '@angular/material/expansion';

import { QueryAnalysisService } from '../../services/query-analysis.service';
import { QueryAnalysisResult } from '../../models/query-analysis.model';

@Component({
  selector: 'app-query-optimizer',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatDividerModule,
    MatSnackBarModule,
    MatExpansionModule
  ],
  template: `
    <div class="query-optimizer">
      <!-- Input Section -->
      <mat-card class="input-section">
        <mat-card-header>
          <mat-card-title>
            <mat-icon>code</mat-icon>
            SQL Query Doctor
          </mat-card-title>
          <mat-card-subtitle>
            Paste your SQL query below and click "Analyze Query" to get optimization suggestions
          </mat-card-subtitle>
        </mat-card-header>
        
        <mat-card-content>
          <label class="custom-label">SQL Query</label>
          <textarea
            [(ngModel)]="sqlQuery"
            placeholder="SELECT * FROM users WHERE id = 1"
            rows="8"
            class="sql-textarea"
            [disabled]="isAnalyzing">
          </textarea>
          
          <div class="button-container">
            <button
              mat-raised-button
              color="primary"
              (click)="analyzeQuery()"
              [disabled]="!sqlQuery.trim() || isAnalyzing"
              class="analyze-button">
              <mat-icon>search</mat-icon>
              Analyze Query
            </button>
            
            <button
              mat-stroked-button
              (click)="clearQuery()"
              [disabled]="isAnalyzing"
              class="clear-button">
              <mat-icon>clear</mat-icon>
              Clear
            </button>
          </div>
        </mat-card-content>
      </mat-card>

      <!-- Loading Spinner -->
      <div *ngIf="isAnalyzing" class="loading-container">
        <mat-spinner diameter="50"></mat-spinner>
        <p>Analyzing your SQL query...</p>
      </div>

      <!-- Results Section -->
      <div *ngIf="analysisResult && !isAnalyzing" class="results-section">
        <!-- Errors -->
        <mat-card *ngIf="analysisResult.errors && analysisResult.errors.length > 0" class="error-card">
          <mat-card-header>
            <mat-card-title class="error-title">
              <mat-icon class="error-icon">error</mat-icon>
              Query Errors
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="error-list">
              <div *ngFor="let error of analysisResult.errors" class="error-item">
                <mat-icon class="error-bullet">cancel</mat-icon>
                <span>{{ error }}</span>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Warnings -->
        <mat-card *ngIf="analysisResult.warnings && analysisResult.warnings.length > 0" class="warning-card">
          <mat-card-header>
            <mat-card-title class="warning-title">
              <mat-icon class="warning-icon">warning</mat-icon>
              Detected Issues / Bad Practices
            </mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="warning-list">
              <div *ngFor="let warning of analysisResult.warnings" class="warning-item">
                <mat-icon class="warning-bullet">info</mat-icon>
                <span>{{ warning }}</span>
              </div>
            </div>
          </mat-card-content>
        </mat-card>

        <!-- Optimized Query -->
        <mat-card class="optimized-card">
          <mat-card-header>
            <mat-card-title class="optimized-title">
              <mat-icon class="optimized-icon">auto_fix_high</mat-icon>
              Optimized SQL Query
            </mat-card-title>
            <mat-card-subtitle *ngIf="isQueryOptimized()">
              ✨ Query has been optimized based on detected issues
            </mat-card-subtitle>
          </mat-card-header>
          <mat-card-content>
            <div class="optimized-query-container">
              <pre class="optimized-query">{{ analysisResult.optimized_query }}</pre>
              <button
                mat-icon-button
                (click)="copyToClipboard(analysisResult.optimized_query)"
                class="copy-button"
                matTooltip="Copy to clipboard">
                <mat-icon>content_copy</mat-icon>
              </button>
            </div>
            
            <!-- Show optimization summary if query was actually changed -->
            <div *ngIf="isQueryOptimized()" class="optimization-summary">
              <mat-expansion-panel>
                <mat-expansion-panel-header>
                  <mat-panel-title>
                    <mat-icon>info</mat-icon>
                    Optimization Summary
                  </mat-panel-title>
                </mat-expansion-panel-header>
                <div class="summary-content">
                  <p><strong>Original Query:</strong></p>
                  <pre class="original-query">{{ sqlQuery }}</pre>
                  <p><strong>Changes Made:</strong></p>
                  <ul>
                    <li *ngFor="let warning of analysisResult.warnings">
                      {{ warning }}
                    </li>
                  </ul>
                </div>
              </mat-expansion-panel>
            </div>
          </mat-card-content>
        </mat-card>
      </div>

      <!-- No Results Message -->
      <div *ngIf="!analysisResult && !isAnalyzing && hasSearched" class="no-results">
        <mat-card>
          <mat-card-content class="text-center">
            <mat-icon class="no-results-icon">search_off</mat-icon>
            <h3>No Analysis Results</h3>
            <p>Try entering a valid SQL query to see optimization suggestions.</p>
          </mat-card-content>
        </mat-card>
      </div>
    </div>
  `,
  styleUrls: ['./query-optimizer.component.scss']
})
export class QueryOptimizerComponent implements OnInit {
  sqlQuery: string = '';
  isAnalyzing: boolean = false;
  analysisResult: QueryAnalysisResult | null = null;
  hasSearched: boolean = false;

  constructor(
    private queryAnalysisService: QueryAnalysisService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Load sample query for demonstration
    this.sqlQuery = `SELECT * FROM users 
WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
ORDER BY name;`;
  }

  analyzeQuery(): void {
    if (!this.sqlQuery.trim()) {
      this.showMessage('Please enter a SQL query to analyze', 'error');
      return;
    }

    this.isAnalyzing = true;
    this.hasSearched = true;
    this.analysisResult = null;

    this.queryAnalysisService.analyzeQuery(this.sqlQuery.trim()).subscribe({
      next: (result: QueryAnalysisResult) => {
        this.analysisResult = result;
        this.isAnalyzing = false;
        this.showMessage('Query analysis completed successfully!', 'success');
      },
      error: (error: any) => {
        console.error('Error analyzing query:', error);
        this.isAnalyzing = false;
        this.showMessage('Error analyzing query. Please try again.', 'error');
      }
    });
  }

  clearQuery(): void {
    this.sqlQuery = '';
    this.analysisResult = null;
    this.hasSearched = false;
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      this.showMessage('Query copied to clipboard!', 'success');
    }).catch(() => {
      this.showMessage('Failed to copy to clipboard', 'error');
    });
  }

  isQueryOptimized(): boolean {
    if (!this.analysisResult) return false;
    return this.analysisResult.optimized_query !== this.sqlQuery.trim();
  }

  private showMessage(message: string, type: 'success' | 'error'): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom',
      panelClass: type === 'success' ? 'success-snackbar' : 'error-snackbar'
    });
  }
} 