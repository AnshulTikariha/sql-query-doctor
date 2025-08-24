import unittest
from sql_analyzer import SQLAnalyzer

class TestSQLAnalyzer(unittest.TestCase):
    """Test cases for SQLAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = SQLAnalyzer()
    
    def test_valid_sql_query(self):
        """Test analysis of a valid SQL query"""
        query = "SELECT id, name FROM users WHERE id = 1"
        result = self.analyzer.analyze_query(query)
        
        self.assertIsInstance(result, dict)
        self.assertIn('errors', result)
        self.assertIn('warnings', result)
        self.assertIn('optimized_query', result)
        self.assertEqual(len(result['errors']), 0)
    
    def test_select_star_detection(self):
        """Test detection of SELECT * usage"""
        query = "SELECT * FROM users WHERE id = 1"
        result = self.analyzer.analyze_query(query)
        
        self.assertGreater(len(result['warnings']), 0)
        self.assertTrue(any('SELECT *' in warning for warning in result['warnings']))
    
    def test_missing_where_clause(self):
        """Test detection of DELETE/UPDATE without WHERE"""
        query = "DELETE FROM users"
        result = self.analyzer.analyze_query(query)
        
        self.assertGreater(len(result['warnings']), 0)
        self.assertTrue(any('WHERE' in warning for warning in result['warnings']))
    
    def test_large_in_clause(self):
        """Test detection of large IN clauses"""
        query = "SELECT * FROM users WHERE id IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)"
        result = self.analyzer.analyze_query(query)
        
        self.assertGreater(len(result['warnings']), 0)
        self.assertTrue(any('IN clause' in warning for warning in result['warnings']))
    
    def test_order_by_without_limit(self):
        """Test detection of ORDER BY without LIMIT"""
        query = "SELECT * FROM users ORDER BY name"
        result = self.analyzer.analyze_query(query)
        
        self.assertGreater(len(result['warnings']), 0)
        self.assertTrue(any('ORDER BY' in warning for warning in result['warnings']))
    
    def test_invalid_sql_syntax(self):
        """Test handling of invalid SQL syntax"""
        query = "SELECT FROM users WHERE id = 1"
        result = self.analyzer.analyze_query(query)
        
        self.assertGreater(len(result['errors']), 0)
    
    def test_empty_query(self):
        """Test handling of empty query"""
        query = ""
        result = self.analyzer.analyze_query(query)
        
        # Should handle gracefully without crashing
        self.assertIsInstance(result, dict)
    
    def test_query_formatting(self):
        """Test SQL query formatting"""
        query = "select id,name from users where id=1"
        formatted = self.analyzer.format_query(query)
        
        self.assertIsInstance(formatted, str)
        self.assertNotEqual(query, formatted)  # Should be different after formatting
    
    def test_query_complexity(self):
        """Test query complexity analysis"""
        query = "SELECT u.id, u.name FROM users u JOIN orders o ON u.id = o.user_id WHERE u.active = 1"
        complexity = self.analyzer.get_query_complexity(query)
        
        self.assertIsInstance(complexity, dict)
        self.assertIn('tables', complexity)
        self.assertIn('joins', complexity)
        self.assertIn('conditions', complexity)
        self.assertIn('subqueries', complexity)

if __name__ == '__main__':
    unittest.main() 