/**
 * Interface representing the result of SQL query analysis
 */
export interface QueryAnalysisResult {
  /** List of syntax errors found in the query */
  errors: string[];
  
  /** List of warnings and bad practices detected */
  warnings: string[];
  
  /** The optimized version of the SQL query */
  optimized_query: string;
}

/**
 * Interface for the API request payload
 */
export interface QueryAnalysisRequest {
  /** The SQL query to analyze */
  query: string;
}

/**
 * Interface for API error responses
 */
export interface ApiError {
  /** Error message */
  error: string;
  
  /** Additional error details if available */
  details?: string;
} 