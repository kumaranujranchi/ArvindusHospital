#!/usr/bin/env python3
"""
Comprehensive deployment script for Arvindu Hospitals website
This script helps set up the database, run migrations, and prepare for deployment
"""

import os
import sys
from app import app, db

def create_tables():
    """Create all database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False

def check_database_connection():
    """Check if database connection is working"""
    with app.app_context():
        try:
            # Try to execute a simple query
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

def run_migrations():
    """Run database migrations"""
    try:
        from migrations.migrate import MigrationManager
        manager = MigrationManager()
        return manager.migrate()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def run_health_check():
    """Run comprehensive health check"""
    try:
        from scripts.maintenance import MaintenanceManager
        maintenance = MaintenanceManager()
        return maintenance.health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🏥 Arvindu Hospitals - Comprehensive Deployment Setup")
    print("=" * 60)

    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL not set. Using SQLite for local development.")
    else:
        print(f"✅ DATABASE_URL configured: {database_url[:50]}...")

    session_secret = os.environ.get('SESSION_SECRET')
    if not session_secret:
        print("⚠️  SESSION_SECRET not set. Using default (not secure for production).")
    else:
        print("✅ SESSION_SECRET configured")

    print("\n🔍 Checking database connection...")
    if not check_database_connection():
        print("❌ Deployment failed: Database connection issue")
        sys.exit(1)

    print("\n🗄️  Running database migrations...")
    if not run_migrations():
        print("❌ Deployment failed: Migration issues")
        sys.exit(1)

    print("\n🏥 Running health check...")
    if not run_health_check():
        print("⚠️  Health check found issues, but continuing deployment...")

    print("\n✅ Deployment setup completed successfully!")
    print("\n📋 Next steps for Netlify deployment:")
    print("1. Set up your database service (Supabase, PlanetScale, etc.)")
    print("2. Configure DATABASE_URL in your Netlify environment variables")
    print("3. Configure SESSION_SECRET in your Netlify environment variables")
    print("4. Push code to GitHub and connect to Netlify")
    print("5. Deploy to Netlify")
    print("\n🔧 Available maintenance commands:")
    print("   python scripts/backup.py create     - Create database backup")
    print("   python scripts/maintenance.py health - Run health check")
    print("   python migrations/migrate.py status  - Check migration status")

if __name__ == "__main__":
    main()
