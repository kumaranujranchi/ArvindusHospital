# Arvindu Hospitals Website

A comprehensive static website for Arvindu Hospitals, a premier multispecialty healthcare network based in Bihar. This website has been converted from Flask to a static site optimized for Netlify deployment with serverless functions for form handling.

## 🔄 Conversion Status

**✅ CONVERTED TO STATIC SITE**

This website has been successfully converted from Flask to a static HTML site while maintaining the exact same design, content, and functionality. The conversion includes:

- ✅ Static HTML pages (index.html, appointment.html, contact.html)
- ✅ Netlify Functions for form handling (appointment, contact, newsletter)
- ✅ All original styling and JavaScript preserved
- ✅ Responsive design maintained
- ✅ Form validation and submission working
- ✅ Ready for Netlify deployment

## 🏥 Features

### Core Functionality
- **Appointment Booking System**: Patients can book appointments online with department and doctor selection
- **Contact Forms**: Multiple contact forms for different purposes with validation
- **Newsletter Subscription**: Email newsletter signup with duplicate prevention
- **Multi-page Website**: Home, About, Departments, Doctors, Patient Care, Blog, Careers, etc.
- **Responsive Design**: Mobile-friendly Bootstrap-based design with modern UI

### Advanced Features
- **Database Migrations**: Automated schema management and versioning
- **Performance Optimization**: Caching, compression, and query optimization
- **Monitoring & Logging**: Comprehensive application monitoring and error tracking
- **Health Checks**: Automated health monitoring with detailed diagnostics
- **Backup System**: Automated database backup and restore functionality
- **Maintenance Tools**: Data cleanup, optimization, and integrity checks
- **Environment Management**: Multi-environment configuration (dev, prod, testing)
- **Security Features**: CSRF protection, secure sessions, input validation

## 🚀 Quick Start (Static Site)

### Local Development

1. **Start a local server**:
   ```bash
   python3 -m http.server 8000
   ```

2. **Open in browser**:
   ```
   http://localhost:8000
   ```

3. **For testing Netlify Functions locally**:
   ```bash
   npm install -g netlify-cli
   netlify dev
   ```

### Original Flask Development (Legacy)

If you need to run the original Flask version:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. Open http://localhost:5000 in your browser

## 🌐 Netlify Deployment (Static Site)

This website is now a static site optimized for Netlify deployment with serverless functions.

### Prerequisites for Netlify Deployment

- Netlify account
- Git repository (GitHub, GitLab, or Bitbucket)

### Deployment Steps

1. **Push to Git Repository**:
   ```bash
   git add .
   git commit -m "Deploy static Arvindu Hospitals website"
   git push origin main
   ```

2. **Deploy to Netlify**:
   - Connect your Git repository to Netlify
   - Build settings:
     - Build command: `echo 'Building Arvindu Hospitals static site...'`
     - Publish directory: `.` (root directory)
   - Deploy the site

3. **Configure Environment Variables** (optional):
   - Set up any required environment variables in Netlify dashboard
   - For email services, analytics, etc.

### Form Handling

The static site uses Netlify Functions for form handling:
- **Appointment Form**: `/.netlify/functions/appointment`
- **Contact Form**: `/.netlify/functions/contact`
- **Newsletter**: `/.netlify/functions/newsletter`

No database is required - forms can be configured to send emails or integrate with external services.

## 📁 Project Structure

```
├── app.py                    # Flask application factory
├── main.py                   # Local development entry point
├── config.py                 # Environment configuration management
├── routes.py                 # URL routes and view functions
├── models.py                 # Database models (SQLAlchemy)
├── forms.py                  # WTForms form definitions
├── monitoring.py             # Application monitoring and logging
├── performance.py            # Performance optimization utilities
├── deploy.py                 # Comprehensive deployment script
├── test_app.py              # Test suite
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS, JavaScript, images
├── migrations/              # Database migration scripts
│   ├── migrate.py          # Migration manager
│   ├── 001_initial_schema.py
│   └── 002_add_indexes.py
├── scripts/                 # Maintenance and utility scripts
│   ├── backup.py           # Database backup/restore
│   └── maintenance.py      # Routine maintenance tasks
├── netlify/                 # Netlify Functions for serverless deployment
│   └── functions/
│       └── app.py          # Serverless function handler
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── netlify.toml            # Netlify configuration
├── runtime.txt             # Python version specification
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── DEPLOYMENT_GUIDE.md     # Detailed deployment instructions
```

## 🛠️ Management Commands

### Database Migrations
```bash
# Check migration status
python migrations/migrate.py status

# Run pending migrations
python migrations/migrate.py migrate

# Run specific migration
python migrations/001_initial_schema.py
```

### Database Backup & Restore
```bash
# Create backup
python scripts/backup.py create

# List available backups
python scripts/backup.py list

# Restore from backup
python scripts/backup.py restore backup_20240101_120000.json.gz

# Cleanup old backups (keep last 30 days)
python scripts/backup.py cleanup 30
```

### Maintenance Tasks
```bash
# Run health check
python scripts/maintenance.py health

# Generate usage statistics
python scripts/maintenance.py stats

# Clean up old data (older than 365 days)
python scripts/maintenance.py cleanup 365

# Optimize database performance
python scripts/maintenance.py optimize

# Check data integrity
python scripts/maintenance.py check
```

### Development Tools
```bash
# Run test suite
python test_app.py

# Clear application cache (dev only)
curl http://localhost:8000/performance/cache/clear

# Get performance stats (dev only)
curl http://localhost:8000/performance/stats

# Health check endpoint
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed
```

## 🔧 Technologies Used

- **Backend**: Flask 3.1+, SQLAlchemy 2.0+, WTForms 3.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (local), PostgreSQL/MySQL (production)
- **Deployment**: Netlify Functions (serverless)
- **Monitoring**: Custom monitoring with health checks
- **Performance**: Caching, compression, query optimization
- **Security**: CSRF protection, secure sessions, input validation

## 🚀 Performance Features

- **Caching**: In-memory caching for frequently accessed data
- **Compression**: Automatic response compression for text content
- **Database Optimization**: Connection pooling and query optimization
- **Static File Optimization**: Long-term caching for static assets
- **HTML Minification**: Automatic HTML minification in production
- **Performance Monitoring**: Request timing and slow query detection

## 📊 Monitoring & Observability

- **Health Checks**: Automated health monitoring endpoints
- **Error Tracking**: Comprehensive error logging and tracking
- **Performance Metrics**: Request timing and performance monitoring
- **Database Monitoring**: Connection health and query performance
- **Application Logs**: Structured logging with rotation

## 🔒 Security Features

- **CSRF Protection**: Cross-site request forgery protection
- **Secure Sessions**: HTTP-only, secure session cookies
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: Parameterized queries
- **Environment Variables**: Secure configuration management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python test_app.py`)
5. Run health check (`python scripts/maintenance.py health`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is proprietary to Arvindu Hospitals.

## 📞 Support

For technical support or deployment assistance:
1. Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
2. Run health checks: `python scripts/maintenance.py health`
3. Check application logs
4. Review Netlify function logs (for production issues)
