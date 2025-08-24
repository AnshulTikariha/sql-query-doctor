from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_analyzer import SQLAnalyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize SQL analyzer
sql_analyzer = SQLAnalyzer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "sql-optimizer-backend"})

@app.route('/analyze-query', methods=['POST'])
def analyze_query():
    """
    Analyze and optimize SQL query endpoint
    
    Expected JSON payload:
    {
        "query": "SELECT * FROM users WHERE id = 1"
    }
    
    Returns:
    {
        "errors": ["list of syntax errors"],
        "warnings": ["list of warnings/bad practices"],
        "optimized_query": "optimized version of the query"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in request body"
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                "error": "Query cannot be empty"
            }), 400
        
        logger.info(f"Analyzing query: {query[:100]}...")
        
        # Analyze the SQL query
        result = sql_analyzer.analyze_query(query)
        
        logger.info(f"Analysis completed successfully")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing query: {str(e)}")
        return jsonify({
            "error": "Internal server error during query analysis",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 