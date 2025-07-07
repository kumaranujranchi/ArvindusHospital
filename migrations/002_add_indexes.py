#!/usr/bin/env python3
"""
Add database indexes for better performance
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db

def upgrade():
    """Add performance indexes"""
    print("🔄 Adding database indexes for better performance...")
    
    with app.app_context():
        try:
            # Add indexes for common queries
            indexes = [
                # Appointment table indexes
                "CREATE INDEX IF NOT EXISTS idx_appointment_date ON appointment(date)",
                "CREATE INDEX IF NOT EXISTS idx_appointment_email ON appointment(email)",
                "CREATE INDEX IF NOT EXISTS idx_appointment_department ON appointment(department)",
                "CREATE INDEX IF NOT EXISTS idx_appointment_created_at ON appointment(created_at)",
                
                # Contact message indexes
                "CREATE INDEX IF NOT EXISTS idx_contact_email ON contact_message(email)",
                "CREATE INDEX IF NOT EXISTS idx_contact_created_at ON contact_message(created_at)",
                
                # Newsletter indexes
                "CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter(email)",
                "CREATE INDEX IF NOT EXISTS idx_newsletter_created_at ON newsletter(created_at)",
            ]
            
            for index_sql in indexes:
                try:
                    db.session.execute(db.text(index_sql))
                    print(f"   ✓ {index_sql.split('idx_')[1].split(' ON')[0]}")
                except Exception as e:
                    print(f"   ⚠️  Warning: {e}")
            
            db.session.commit()
            print("✅ Database indexes added successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error adding indexes: {e}")
            db.session.rollback()
            return False

def downgrade():
    """Remove the indexes"""
    print("🔄 Removing database indexes...")
    
    with app.app_context():
        try:
            # Drop indexes
            indexes = [
                "DROP INDEX IF EXISTS idx_appointment_date",
                "DROP INDEX IF EXISTS idx_appointment_email", 
                "DROP INDEX IF EXISTS idx_appointment_department",
                "DROP INDEX IF EXISTS idx_appointment_created_at",
                "DROP INDEX IF EXISTS idx_contact_email",
                "DROP INDEX IF EXISTS idx_contact_created_at",
                "DROP INDEX IF EXISTS idx_newsletter_email",
                "DROP INDEX IF EXISTS idx_newsletter_created_at",
            ]
            
            for index_sql in indexes:
                try:
                    db.session.execute(db.text(index_sql))
                    print(f"   ✓ Removed {index_sql.split('idx_')[1]}")
                except Exception as e:
                    print(f"   ⚠️  Warning: {e}")
            
            db.session.commit()
            print("✅ Database indexes removed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error removing indexes: {e}")
            db.session.rollback()
            return False

def main():
    """Main migration function"""
    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        return downgrade()
    else:
        return upgrade()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
