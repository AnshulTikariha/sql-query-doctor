# SQL Query Doctor

A full-stack application that diagnoses and prescribes improvements for SQL queries using rule-based analysis and suggestions.

## 🚀 Features

- **Frontend**: Angular 17 with Material UI for a clean, responsive interface
- **Backend**: Flask API with SQL analysis capabilities
- **Analysis**: Detects syntax errors, bad practices, and suggests optimizations
- **Local Development**: Easy setup with Python and Node.js

## 🏗️ Project Structure

```
sql-optimizer/
├── frontend/          # Angular 17 application
├── backend/           # Flask API server
├── README.md         # This file
└── REQUIRED_SOFTWARE.md # Software requirements
```

## 🛠️ Prerequisites

- Node.js 18+ (for local development)
- Python 3.8+ (for local development)

## 🚀 Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd sql-optimizer
   ```

2. **Follow the setup guide:**
   - See `REQUIRED_SOFTWARE.md` for detailed installation steps
   - Or follow the Local Development section below

3. **Access the application:**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:5001

## 🖥️ Local Development

### Frontend (Angular)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Access at:** http://localhost:4200

### Backend (Flask)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Flask server:**
   ```bash
   python app.py
   ```

5. **Access at:** http://localhost:5001

## 📚 API Endpoints

### POST /analyze-query

Analyzes and optimizes SQL queries.

**Request Body:**
```json
{
  "query": "SELECT * FROM users WHERE id = 1"
}
```

**Response:**
```json
{
  "errors": [],
  "warnings": [
    "SELECT * is used - consider specifying only needed columns"
  ],
  "optimized_query": "SELECT id, name, email FROM users WHERE id = 1"
}
```

## 🔧 Configuration

- Frontend runs on port 4200
- Backend runs on port 5001
- CORS is configured for local development
- All ports can be customized in the respective configuration files

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
python -m pytest
```

## 🚀 Deployment

The project can be deployed using various methods:

1. **Traditional deployment:**
   - Deploy backend to a Python hosting service (Heroku, PythonAnywhere, etc.)
   - Deploy frontend to a static hosting service (Netlify, Vercel, GitHub Pages, etc.)

2. **Environment variables:**
   - Configure production settings in your hosting environment
   - Set up CORS for your production domain

## 🔮 Future Enhancements

- AI-powered query optimization
- Database-specific optimization rules
- Query performance metrics
- Integration with database engines
- Advanced syntax highlighting
- Query history and favorites

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions, please create an issue in the repository. 