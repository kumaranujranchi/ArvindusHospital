# Arvindu Hospitals - Netlify Deployment Guide

## 🏥 Project Overview

This is a Flask-based hospital website for Arvindu Hospitals with the following features:
- **Appointment Booking System**
- **Contact Forms**
- **Newsletter Subscription**
- **Multi-page Hospital Website**
- **Responsive Bootstrap Design**

## 📋 Pre-Deployment Checklist

✅ **Completed Setup Tasks:**
- [x] Fixed routing issues (added missing home route)
- [x] Created Netlify deployment configuration
- [x] Set up serverless function adapter
- [x] Created database configuration for external services
- [x] Added comprehensive testing
- [x] Verified local functionality

## 🚀 Deployment Steps

### Step 1: Database Setup (Required)

Since Netlify doesn't support local databases, you need an external database service:

**Recommended: Supabase (Free PostgreSQL)**
1. Go to [supabase.com](https://supabase.com)
2. Create a free account
3. Create a new project
4. Go to Settings → Database
5. Copy the connection string (starts with `postgresql://`)

**Alternative Options:**
- **PlanetScale** (MySQL)
- **Railway** (PostgreSQL)
- **Heroku Postgres**

### Step 2: Netlify Deployment

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Connect to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   - Netlify will auto-detect the `netlify.toml` configuration

3. **Set Environment Variables in Netlify:**
   - Go to Site Settings → Environment Variables
   - Add these variables:
     ```
     DATABASE_URL=your_database_connection_string
     SESSION_SECRET=your_secure_random_string
     ```

4. **Deploy:**
   - Netlify will automatically build and deploy
   - The build process will install dependencies and set up the serverless functions

### Step 3: Database Initialization

After deployment, initialize your database tables:

**Option A: Local Initialization (Recommended)**
```bash
# Set your production database URL
export DATABASE_URL="your_production_database_url"
python3 deploy.py
```

**Option B: Create a one-time Netlify function**
- The `deploy.py` script can be adapted as a Netlify function for one-time setup

## 🔧 Configuration Files

### Key Files Created:
- `netlify.toml` - Netlify build configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `netlify/functions/app.py` - Serverless function handler
- `deploy.py` - Database setup script
- `test_app.py` - Test suite

## 🧪 Testing

Run tests locally:
```bash
pip3 install -r requirements-dev.txt
python3 test_app.py
```

Run local development server:
```bash
python3 main.py
# Visit http://localhost:8000
```

## 🌐 Production URLs

After deployment, your site will be available at:
- `https://your-site-name.netlify.app`
- Custom domain (if configured)

## 📊 Monitoring

- **Netlify Dashboard**: Monitor deployments and function logs
- **Database Dashboard**: Monitor database usage and performance
- **Application Logs**: Check Netlify function logs for errors

## 🔒 Security Considerations

- ✅ Environment variables for sensitive data
- ✅ CSRF protection enabled
- ✅ Secure session management
- ✅ Input validation on all forms

## 🆘 Troubleshooting

### Common Issues:

1. **Build Fails:**
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Database Connection Errors:**
   - Verify `DATABASE_URL` environment variable
   - Check database service status
   - Ensure database allows external connections

3. **Function Timeout:**
   - Netlify functions have a 10-second timeout
   - Optimize database queries
   - Consider caching strategies

4. **Static Files Not Loading:**
   - Verify static file paths in templates
   - Check Netlify build output

## 📞 Support

For deployment issues:
1. Check Netlify build logs
2. Review function logs in Netlify dashboard
3. Test locally with production database URL
4. Verify all environment variables are set

## 🎯 Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure SSL certificate (automatic with Netlify)
3. Set up monitoring and analytics
4. Plan for regular backups
5. Consider CDN optimization for static assets
