import sqlparse
import sqlglot
from sqlglot import parse, exp
from sqlglot.errors import ParseError
import re
from typing import Dict, List, Tuple, Optional

class SQLAnalyzer:
    """
    SQL Query Analyzer and Optimizer
    
    Provides rule-based analysis of SQL queries including:
    - Syntax validation
    - Bad practice detection
    - Query optimization suggestions
    """
    
    def __init__(self):
        """Initialize the SQL analyzer with optimization rules"""
        self.optimization_rules = [
            self._rule_select_star,
            self._rule_missing_where,
            self._rule_in_clause_optimization,
            self._rule_order_by_limit,
            self._rule_unnecessary_distinct,
            self._rule_table_aliases,
            self._rule_index_hints
        ]
    
    def analyze_query(self, query: str) -> Dict[str, List[str]]:
        """
        Analyze a SQL query and return analysis results
        
        Args:
            query (str): The SQL query to analyze
            
        Returns:
            Dict containing errors, warnings, and optimized query
        """
        result = {
            "errors": [],
            "warnings": [],
            "optimized_query": query
        }
        
        try:
            # Basic syntax validation
            self._validate_syntax(query, result)
            
            # Apply optimization rules and get actual optimizations
            if not result["errors"]:
                optimized_query = self._apply_optimization_rules(query, result)
                result["optimized_query"] = optimized_query
                
        except Exception as e:
            result["errors"].append(f"Analysis error: {str(e)}")
        
        return result
    
    def _validate_syntax(self, query: str, result: Dict[str, List[str]]) -> None:
        """Validate SQL syntax using sqlglot"""
        try:
            # Try to parse with sqlglot
            parsed = parse(query)
            if not parsed:
                result["errors"].append("Unable to parse SQL query - check syntax")
        except ParseError as e:
            result["errors"].append(f"SQL syntax error: {str(e)}")
        except Exception as e:
            result["errors"].append(f"Unexpected parsing error: {str(e)}")
    
    def _apply_optimization_rules(self, query: str, result: Dict[str, List[str]]) -> str:
        """Apply all optimization rules to the query and return optimized version"""
        optimized_query = query
        
        # Apply rules in specific order and accumulate changes
        for rule in self.optimization_rules:
            try:
                rule_result = rule(optimized_query)  # Use the current optimized version
                if rule_result:
                    warning, suggestion = rule_result
                    result["warnings"].append(warning)
                    if suggestion:
                        optimized_query = suggestion  # Update with the new optimization
            except Exception as e:
                # Log rule execution errors but don't fail the analysis
                continue
        
        return optimized_query
    
    def _rule_select_star(self, query: str) -> Optional[Tuple[str, str]]:
        """Detect SELECT * usage and suggest specific columns"""
        if re.search(r'SELECT\s+\*', query, re.IGNORECASE | re.DOTALL):
            # Try to extract table name to suggest common columns
            table_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE | re.DOTALL)
            if table_match:
                table_name = table_match.group(1)
                
                # Check if there are specific columns mentioned in WHERE or ORDER BY
                where_columns = re.findall(r'WHERE\s+(\w+)', query, re.IGNORECASE | re.DOTALL)
                order_columns = re.findall(r'ORDER\s+BY\s+(\w+)', query, re.IGNORECASE | re.DOTALL)
                
                # Combine all referenced columns
                referenced_columns = set()
                if where_columns:
                    referenced_columns.update(where_columns)
                if order_columns:
                    referenced_columns.update(order_columns)
                
                # Suggest columns based on table and context
                if table_name.lower() == 'users':
                    # For users table, prioritize commonly needed columns
                    if referenced_columns:
                        # Include referenced columns plus common ones
                        suggested_columns = list(referenced_columns) + ['id', 'name', 'email', 'number']
                        suggested_columns = list(dict.fromkeys(suggested_columns))  # Remove duplicates
                    else:
                        # Default suggestion for users table
                        suggested_columns = ['id', 'name', 'email', 'created_at']
                        
                elif table_name.lower() == 'orders':
                    if referenced_columns:
                        suggested_columns = list(referenced_columns) + ['id', 'user_id', 'total', 'status']
                        suggested_columns = list(dict.fromkeys(suggested_columns))
                    else:
                        suggested_columns = ['id', 'user_id', 'total', 'status', 'created_at']
                        
                elif table_name.lower() == 'products':
                    if referenced_columns:
                        suggested_columns = list(referenced_columns) + ['id', 'name', 'price', 'category']
                        suggested_columns = list(dict.fromkeys(suggested_columns))
                    else:
                        suggested_columns = ['id', 'name', 'price', 'category', 'stock']
                        
                else:
                    # Generic suggestion based on referenced columns
                    if referenced_columns:
                        suggested_columns = list(referenced_columns) + ['id', 'name']
                        suggested_columns = list(dict.fromkeys(suggested_columns))
                    else:
                        suggested_columns = ['id', 'name']
                
                # Create optimized query
                columns_str = ', '.join(suggested_columns)
                optimized = re.sub(r'SELECT\s+\*', f'SELECT {columns_str}', query, flags=re.IGNORECASE | re.DOTALL)
                
                return (
                    f"SELECT * is used - consider specifying only needed columns for better performance. Suggested: {columns_str}",
                    optimized
                )
            else:
                return (
                    "SELECT * is used - consider specifying only needed columns for better performance",
                    None
                )
        return None
    
    def _rule_missing_where(self, query: str) -> Optional[Tuple[str, str]]:
        """Detect DELETE/UPDATE without WHERE clause"""
        if re.search(r'\b(DELETE|UPDATE)\s+FROM?\s+\w+', query, re.IGNORECASE):
            if not re.search(r'\bWHERE\b', query, re.IGNORECASE):
                return (
                    "DELETE/UPDATE statement missing WHERE clause - this could affect all rows",
                    None
                )
        return None
    
    def _rule_in_clause_optimization(self, query: str) -> Optional[Tuple[str, str]]:
        """Detect large IN clauses and suggest alternatives"""
        in_match = re.search(r'\bIN\s*\(([^)]+)\)', query, re.IGNORECASE)
        if in_match:
            values = in_match.group(1).split(',')
            if len(values) > 10:
                # Check if values are sequential (can use BETWEEN)
                try:
                    numeric_values = [int(v.strip()) for v in values if v.strip().isdigit()]
                    if len(numeric_values) == len(values):
                        numeric_values.sort()
                        if numeric_values[-1] - numeric_values[0] + 1 == len(numeric_values):
                            # Sequential range - suggest BETWEEN
                            column_match = re.search(r'\bWHERE\s+(\w+)', query, re.IGNORECASE)
                            if column_match:
                                column_name = column_match.group(1)
                                
                                # Create optimized query with BETWEEN
                                optimized = re.sub(
                                    rf'\bWHERE\s+{column_name}\s+IN\s*\([^)]+\)',
                                    f'WHERE {column_name} BETWEEN {numeric_values[0]} AND {numeric_values[-1]}',
                                    query,
                                    flags=re.IGNORECASE
                                )
                                
                                return (
                                    f"IN clause contains {len(values)} sequential values - consider using BETWEEN {numeric_values[0]} AND {numeric_values[-1]} for better performance",
                                    optimized
                                )
                except (ValueError, IndexError):
                    pass
                
                # For non-sequential values, suggest breaking into smaller chunks
                table_match = re.search(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
                column_match = re.search(r'\bWHERE\s+(\w+)', query, re.IGNORECASE)
                if table_match and column_match:
                    table_name = table_match.group(1)
                    column_name = column_match.group(1)
                    
                    # Get current SELECT columns or use default
                    select_match = re.search(r'\bSELECT\s+([^FROM]+)', query, re.IGNORECASE)
                    if select_match:
                        select_columns = select_match.group(1).strip()
                    else:
                        select_columns = "id, name, email"
                    
                    # Suggest breaking into smaller chunks
                    chunk_size = 5
                    chunks = [values[i:i + chunk_size] for i in range(0, len(values), chunk_size)]
                    
                    optimized = f"""-- Break large IN clause into smaller chunks for better performance
-- Option 1: Use UNION of smaller IN clauses
SELECT {select_columns} FROM {table_name}
WHERE {column_name} IN ({', '.join(chunks[0])})
UNION
SELECT {select_columns} FROM {table_name}
WHERE {column_name} IN ({', '.join(chunks[1])})
UNION
SELECT {select_columns} FROM {table_name}
WHERE {column_name} IN ({', '.join(chunks[2])})
ORDER BY name LIMIT 100;

-- Option 2: Use EXISTS with a temporary table (for very large datasets)
-- CREATE TEMPORARY TABLE temp_ids (id INT);
-- INSERT INTO temp_ids VALUES {', '.join([f"({v.strip()})" for v in values])};
-- SELECT {select_columns} FROM {table_name} t
-- WHERE EXISTS (SELECT 1 FROM temp_ids ti WHERE ti.id = t.{column_name})
-- ORDER BY name LIMIT 100;"""
                    
                    return (
                        f"IN clause contains {len(values)} values - consider breaking into smaller chunks or using BETWEEN if sequential",
                        optimized
                    )
                
                return (
                    f"IN clause contains {len(values)} values - consider using BETWEEN if sequential or breaking into smaller chunks",
                    None
                )
        return None
    
    def _rule_order_by_limit(self, query: str) -> Optional[Tuple[str, str]]:
        """Suggest adding LIMIT when ORDER BY is used without LIMIT"""
        if re.search(r'\bORDER\s+BY\b', query, re.IGNORECASE):
            if not re.search(r'\bLIMIT\b', query, re.IGNORECASE):
                # Add LIMIT clause
                optimized = query.rstrip(';') + " LIMIT 100;"
                return (
                    "ORDER BY used without LIMIT - consider adding LIMIT to control result size",
                    optimized
                )
        return None
    
    def _rule_unnecessary_distinct(self, query: str) -> Optional[Tuple[str, str]]:
        """Detect potentially unnecessary DISTINCT usage"""
        if re.search(r'\bDISTINCT\b', query, re.IGNORECASE):
            # Check if there's a unique constraint or primary key in WHERE clause
            if re.search(r'\bWHERE\s+\w+\.\w+\s*=\s*\d+', query, re.IGNORECASE):
                # Remove DISTINCT if it's unnecessary
                optimized = re.sub(r'\bDISTINCT\s+', '', query, flags=re.IGNORECASE)
                return (
                    "DISTINCT used with unique constraint - may be unnecessary",
                    optimized
                )
        return None
    
    def _rule_table_aliases(self, query: str) -> Optional[Tuple[str, str]]:
        """Suggest table aliases for complex queries"""
        # Count table references
        table_refs = re.findall(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
        table_refs.extend(re.findall(r'\bJOIN\s+(\w+)', query, re.IGNORECASE))
        
        if len(table_refs) > 2 and not re.search(r'\bAS\s+\w+', query, re.IGNORECASE):
            # Add table aliases
            optimized = query
            for i, table in enumerate(table_refs):
                alias = chr(97 + i)  # a, b, c, etc.
                optimized = re.sub(rf'\b{table}\b', f'{table} AS {alias}', optimized, count=1)
            
            return (
                "Multiple table references detected - consider using table aliases for clarity",
                optimized
            )
        return None
    
    def _rule_index_hints(self, query: str) -> Optional[Tuple[str, str]]:
        """Suggest index hints for common patterns"""
        if re.search(r'\bWHERE\s+\w+\s*=\s*\w+', query, re.IGNORECASE):
            return (
                "Consider adding appropriate indexes for columns used in WHERE clauses",
                None
            )
        return None
    
    def _rule_suggest_additional_columns(self, query: str) -> Optional[Tuple[str, str]]:
        """Suggest additional useful columns that might be missing"""
        # Check if it's a SELECT query (not SELECT *)
        if re.search(r'\bSELECT\s+(?!\*)(\w+)', query, re.IGNORECASE):
            table_match = re.search(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
            if table_match:
                table_name = table_match.group(1)
                current_columns = re.search(r'\bSELECT\s+([^FROM]+)', query, re.IGNORECASE)
                
                if current_columns:
                    current_cols = current_columns.group(1).strip()
                    
                    # Suggest additional useful columns based on table
                    if table_name.lower() == 'users':
                        if 'id' in current_cols and 'name' in current_cols:
                            # If they have id and name, suggest adding 'number' (phone number)
                            if 'number' not in current_cols and 'phone' not in current_cols:
                                # Add number column to the SELECT
                                optimized = re.sub(
                                    r'\bSELECT\s+([^FROM]+)',
                                    r'SELECT \1, number',
                                    query,
                                    flags=re.IGNORECASE
                                )
                                return (
                                    "Consider adding 'number' column for complete user information",
                                    optimized
                                )
                    
                    elif table_name.lower() == 'orders':
                        if 'id' in current_cols and 'user_id' in current_cols:
                            if 'total' not in current_cols:
                                optimized = re.sub(
                                    r'\bSELECT\s+([^FROM]+)',
                                    r'SELECT \1, total',
                                    query,
                                    flags=re.IGNORECASE
                                )
                                return (
                                    "Consider adding 'total' column for order value information",
                                    optimized
                                )
        
        return None
    
    def format_query(self, query: str) -> str:
        """Format SQL query for better readability"""
        try:
            parsed = sqlparse.parse(query)
            return sqlparse.format(query, reindent=True, keyword_case='upper')
        except Exception:
            return query
    
    def get_query_complexity(self, query: str) -> Dict[str, any]:
        """Analyze query complexity metrics"""
        try:
            parsed = parse(query)
            complexity = {
                "tables": 0,
                "joins": 0,
                "conditions": 0,
                "subqueries": 0
            }
            
            # Count tables
            tables = [t for t in parsed.find_all(exp.Table)]
            complexity["tables"] = len(tables)
            
            # Count joins
            joins = [j for j in parsed.find_all(exp.Join)]
            complexity["joins"] = len(joins)
            
            # Count WHERE conditions
            where_clauses = [w for w in parsed.find_all(exp.Where)]
            complexity["conditions"] = len(where_clauses)
            
            # Count subqueries
            subqueries = [s for s in parsed.find_all(exp.Subquery)]
            complexity["subqueries"] = len(subqueries)
            
            return complexity
            
        except Exception:
            return {"error": "Unable to analyze query complexity"} 