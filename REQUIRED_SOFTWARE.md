# Required Software for SQL Query Doctor

This document lists all the software and dependencies required to run the SQL Query Doctor system on your local machine.

## 🌐 System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **Network**: Internet connection for downloading dependencies

## 🐍 Python Requirements

### Python Version
- **Python**: 3.8 or higher (3.9+ recommended)
- **Package Manager**: pip (usually comes with Python)

### Python Dependencies
The following packages will be automatically installed via `requirements.txt`:

#### Core Dependencies
- **Flask 2.3.3** - Web framework for the backend API
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing support
- **sqlparse 0.4.4** - SQL parsing and formatting
- **sqlglot 19.0.0** - SQL parsing, transpiling, and analysis
- **Werkzeug 2.3.7** - WSGI web application library

#### Development & Testing
- **pytest 7.4.2** - Testing framework
- **pytest-flask 1.2.0** - Flask testing utilities
- **gunicorn 21.2.0** - WSGI HTTP Server for production

## 🟢 Node.js Requirements

### Node.js Version
- **Node.js**: 18.0.0 or higher (LTS version recommended)
- **npm**: 8.0.0 or higher (comes with Node.js)

### Node.js Dependencies
The following packages will be automatically installed via `package.json`:

#### Core Dependencies
- **Angular 17.0.0** - Frontend framework
- **Angular Material 17.0.0** - UI component library
- **RxJS 7.8.0** - Reactive programming library
- **TypeScript 5.2.0** - Programming language

#### Development Dependencies
- **Angular CLI 17.0.0** - Command line interface for Angular
- **Karma 6.4.0** - Test runner
- **Jasmine 5.1.0** - Testing framework

## 🛠️ Development Tools (Optional but Recommended)

### Code Editor
- **VS Code** (recommended) with extensions:
  - Python extension
  - Angular Language Service
  - TypeScript and JavaScript support
  - ESLint
  - Prettier

### Version Control
- **Git**: 2.20.0 or higher

### Database Tools (Optional)
- **SQLite Browser** or **DBeaver** for database management
- **PostgreSQL** or **MySQL** if you plan to use external databases

## 📋 Installation Instructions

### 1. Install Python
```bash
# Windows: Download from python.org
# macOS: brew install python3
# Ubuntu/Debian: sudo apt install python3 python3-pip
```

### 2. Install Node.js
```bash
# Windows: Download from nodejs.org
# macOS: brew install node
# Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
#                sudo apt-get install -y nodejs
```

### 3. Verify Installations
```bash
# Check Python
python3 --version
pip3 --version

# Check Node.js
node --version
npm --version
```

## 🔧 Environment Setup

### Python Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Node.js Dependencies
```bash
cd frontend
npm install
```

## 🚀 Running the System

### Backend (Flask API)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```
**Access at**: http://localhost:5001

### Frontend (Angular)
```bash
cd frontend
npm start
```
**Access at**: http://localhost:4200

## 🔍 Troubleshooting

### Common Issues

#### Python Issues
- **Module not found**: Ensure virtual environment is activated
- **Permission denied**: Use `pip3` instead of `pip` or add `--user` flag
- **Version conflicts**: Update Python to 3.8+ or use pyenv

#### Node.js Issues
- **Permission denied**: Use `sudo npm` or fix npm permissions
- **Version conflicts**: Use nvm to manage Node.js versions
- **Port already in use**: Change port in `angular.json` or kill existing process

#### Port Conflicts
- **Backend port 5001**: Change in `backend/app.py`
- **Frontend port 4200**: Change in `frontend/angular.json`

## 📚 Additional Resources

- [Python Official Documentation](https://docs.python.org/)
- [Node.js Official Documentation](https://nodejs.org/docs/)
- [Angular Official Documentation](https://angular.io/docs)
- [Flask Official Documentation](https://flask.palletsprojects.com/)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all software versions match requirements
3. Check the project's issue tracker
4. Ensure all dependencies are properly installed
5. Check system firewall and antivirus settings

---

**Last Updated**: December 2024
**Project Version**: SQL Query Doctor v1.0
