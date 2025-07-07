#!/usr/bin/env python3
"""
Initial database schema migration
Creates all the necessary tables for Arvindu Hospitals website
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db
from models import Appointment, ContactMessage, Newsletter

def upgrade():
    """Create all tables"""
    print("🔄 Running initial schema migration...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Successfully created all database tables:")
            print("   - appointments")
            print("   - contact_message") 
            print("   - newsletter")
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['appointment', 'contact_message', 'newsletter']
            for table in expected_tables:
                if table in tables:
                    print(f"   ✓ Table '{table}' created successfully")
                else:
                    print(f"   ❌ Table '{table}' not found")
                    
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

def downgrade():
    """Drop all tables (use with caution!)"""
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'DELETE ALL DATA' to confirm: ")
    
    if confirm != "DELETE ALL DATA":
        print("❌ Migration cancelled")
        return False
        
    with app.app_context():
        try:
            db.drop_all()
            print("✅ All tables dropped successfully")
            return True
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
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
