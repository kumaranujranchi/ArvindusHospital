#!/usr/bin/env python3
"""
Maintenance script for Arvindu Hospitals website
Performs routine maintenance tasks like cleanup, optimization, and health checks
"""

import os
import sys
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db
from models import Appointment, ContactMessage, Newsletter

class MaintenanceManager:
    """Handles routine maintenance tasks"""
    
    def __init__(self):
        self.app = app
    
    def cleanup_old_data(self, days=365):
        """Clean up old data from database"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        with self.app.app_context():
            try:
                # Clean up old appointments (older than specified days)
                old_appointments = Appointment.query.filter(
                    Appointment.created_at < cutoff_date
                ).all()
                
                # Clean up old contact messages (older than specified days)
                old_messages = ContactMessage.query.filter(
                    ContactMessage.created_at < cutoff_date
                ).all()
                
                print(f"🧹 Found {len(old_appointments)} old appointments to clean up")
                print(f"🧹 Found {len(old_messages)} old contact messages to clean up")
                
                if old_appointments or old_messages:
                    confirm = input("Proceed with cleanup? (y/N): ")
                    if confirm.lower() == 'y':
                        # Delete old appointments
                        for apt in old_appointments:
                            db.session.delete(apt)
                        
                        # Delete old messages
                        for msg in old_messages:
                            db.session.delete(msg)
                        
                        db.session.commit()
                        
                        print(f"✅ Cleaned up {len(old_appointments)} appointments")
                        print(f"✅ Cleaned up {len(old_messages)} contact messages")
                        return True
                    else:
                        print("❌ Cleanup cancelled")
                        return False
                else:
                    print("✅ No old data to clean up")
                    return True
                    
            except Exception as e:
                print(f"❌ Cleanup failed: {e}")
                db.session.rollback()
                return False
    
    def optimize_database(self):
        """Optimize database performance"""
        with self.app.app_context():
            try:
                database_url = self.app.config.get('SQLALCHEMY_DATABASE_URI')
                
                if database_url.startswith('sqlite'):
                    # SQLite optimization
                    db.session.execute(db.text('VACUUM'))
                    db.session.execute(db.text('ANALYZE'))
                    print("✅ SQLite database optimized (VACUUM and ANALYZE)")
                
                elif database_url.startswith('postgresql'):
                    # PostgreSQL optimization
                    db.session.execute(db.text('VACUUM ANALYZE'))
                    print("✅ PostgreSQL database optimized (VACUUM ANALYZE)")
                
                db.session.commit()
                return True
                
            except Exception as e:
                print(f"❌ Database optimization failed: {e}")
                return False
    
    def check_data_integrity(self):
        """Check data integrity and consistency"""
        with self.app.app_context():
            issues = []
            
            try:
                # Check for duplicate newsletter subscriptions
                duplicate_emails = db.session.query(Newsletter.email).group_by(
                    Newsletter.email
                ).having(db.func.count(Newsletter.email) > 1).all()
                
                if duplicate_emails:
                    issues.append(f"Found {len(duplicate_emails)} duplicate newsletter emails")
                
                # Check for appointments with invalid dates
                invalid_appointments = Appointment.query.filter(
                    Appointment.date < datetime.utcnow().date() - timedelta(days=365*2)
                ).count()
                
                if invalid_appointments > 0:
                    issues.append(f"Found {invalid_appointments} appointments with very old dates")
                
                # Check for empty required fields
                empty_name_appointments = Appointment.query.filter(
                    (Appointment.name == '') | (Appointment.name.is_(None))
                ).count()
                
                if empty_name_appointments > 0:
                    issues.append(f"Found {empty_name_appointments} appointments with empty names")
                
                # Check for invalid email formats (basic check)
                invalid_emails = Appointment.query.filter(
                    ~Appointment.email.contains('@')
                ).count()
                
                if invalid_emails > 0:
                    issues.append(f"Found {invalid_emails} appointments with invalid email formats")
                
                if issues:
                    print("⚠️  Data integrity issues found:")
                    for issue in issues:
                        print(f"   - {issue}")
                    return False
                else:
                    print("✅ Data integrity check passed")
                    return True
                    
            except Exception as e:
                print(f"❌ Data integrity check failed: {e}")
                return False
    
    def generate_statistics(self):
        """Generate usage statistics"""
        with self.app.app_context():
            try:
                # Get current counts
                total_appointments = Appointment.query.count()
                total_messages = ContactMessage.query.count()
                total_subscribers = Newsletter.query.count()
                
                # Get recent activity (last 30 days)
                thirty_days_ago = datetime.utcnow() - timedelta(days=30)
                recent_appointments = Appointment.query.filter(
                    Appointment.created_at >= thirty_days_ago
                ).count()
                recent_messages = ContactMessage.query.filter(
                    ContactMessage.created_at >= thirty_days_ago
                ).count()
                recent_subscribers = Newsletter.query.filter(
                    Newsletter.created_at >= thirty_days_ago
                ).count()
                
                # Get department statistics
                department_stats = db.session.query(
                    Appointment.department,
                    db.func.count(Appointment.id).label('count')
                ).group_by(Appointment.department).all()
                
                print("📊 Arvindu Hospitals - Usage Statistics")
                print("=" * 50)
                print(f"Total Records:")
                print(f"  Appointments: {total_appointments}")
                print(f"  Contact Messages: {total_messages}")
                print(f"  Newsletter Subscribers: {total_subscribers}")
                
                print(f"\nLast 30 Days:")
                print(f"  New Appointments: {recent_appointments}")
                print(f"  New Messages: {recent_messages}")
                print(f"  New Subscribers: {recent_subscribers}")
                
                print(f"\nDepartment Popularity:")
                for dept, count in sorted(department_stats, key=lambda x: x[1], reverse=True):
                    if dept:  # Skip None values
                        print(f"  {dept}: {count} appointments")
                
                return True
                
            except Exception as e:
                print(f"❌ Statistics generation failed: {e}")
                return False
    
    def health_check(self):
        """Perform comprehensive health check"""
        print("🏥 Arvindu Hospitals - Health Check")
        print("=" * 50)
        
        checks = [
            ("Database Connection", self._check_database_connection),
            ("Table Integrity", self._check_table_integrity),
            ("Data Consistency", self.check_data_integrity),
            ("Disk Space", self._check_disk_space),
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"🔍 {check_name}...", end=" ")
            try:
                if check_func():
                    print("✅ PASS")
                else:
                    print("❌ FAIL")
                    all_passed = False
            except Exception as e:
                print(f"❌ ERROR: {e}")
                all_passed = False
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 All health checks passed!")
        else:
            print("⚠️  Some health checks failed. Please review the issues above.")
        
        return all_passed
    
    def _check_database_connection(self):
        """Check database connectivity"""
        with self.app.app_context():
            db.session.execute(db.text('SELECT 1'))
            return True
    
    def _check_table_integrity(self):
        """Check that all required tables exist"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['appointment', 'contact_message', 'newsletter']
            for table in required_tables:
                if table not in tables:
                    print(f"Missing table: {table}")
                    return False
            
            return True
    
    def _check_disk_space(self):
        """Check available disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('/')
            free_gb = free / (1024**3)
            
            if free_gb < 1.0:  # Less than 1GB free
                print(f"Low disk space: {free_gb:.1f}GB free")
                return False
            
            return True
        except Exception:
            # If we can't check disk space, assume it's okay
            return True

def main():
    """Main maintenance function"""
    maintenance = MaintenanceManager()
    
    if len(sys.argv) < 2:
        print("Usage: python maintenance.py [cleanup|optimize|check|stats|health] [options]")
        print("\nCommands:")
        print("  cleanup [days]  - Clean up old data (default: 365 days)")
        print("  optimize        - Optimize database performance")
        print("  check          - Check data integrity")
        print("  stats          - Generate usage statistics")
        print("  health         - Perform comprehensive health check")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'cleanup':
        days = 365
        if len(sys.argv) > 2:
            try:
                days = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid number of days")
                sys.exit(1)
        
        if maintenance.cleanup_old_data(days):
            print("🎉 Cleanup completed successfully")
        else:
            sys.exit(1)
    
    elif command == 'optimize':
        if maintenance.optimize_database():
            print("🎉 Database optimization completed")
        else:
            sys.exit(1)
    
    elif command == 'check':
        if maintenance.check_data_integrity():
            print("🎉 Data integrity check passed")
        else:
            sys.exit(1)
    
    elif command == 'stats':
        if maintenance.generate_statistics():
            print("\n🎉 Statistics generated successfully")
        else:
            sys.exit(1)
    
    elif command == 'health':
        if not maintenance.health_check():
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
