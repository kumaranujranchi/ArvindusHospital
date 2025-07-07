#!/usr/bin/env python3
"""
Database migration manager for Arvindu Hospitals
Handles running migrations in order and tracking migration state
"""

import os
import sys
import importlib.util
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db

class MigrationManager:
    def __init__(self):
        self.migrations_dir = os.path.dirname(__file__)
        self.migration_table = 'schema_migrations'
        
    def ensure_migration_table(self):
        """Create migration tracking table if it doesn't exist"""
        with app.app_context():
            try:
                db.session.execute(db.text(f"""
                    CREATE TABLE IF NOT EXISTS {self.migration_table} (
                        id SERIAL PRIMARY KEY,
                        migration_name VARCHAR(255) NOT NULL UNIQUE,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                db.session.commit()
                return True
            except Exception as e:
                print(f"❌ Error creating migration table: {e}")
                return False
    
    def get_applied_migrations(self):
        """Get list of already applied migrations"""
        with app.app_context():
            try:
                result = db.session.execute(
                    db.text(f"SELECT migration_name FROM {self.migration_table} ORDER BY applied_at")
                )
                return [row[0] for row in result]
            except Exception:
                return []
    
    def mark_migration_applied(self, migration_name):
        """Mark a migration as applied"""
        with app.app_context():
            try:
                db.session.execute(
                    db.text(f"INSERT INTO {self.migration_table} (migration_name) VALUES (:name)"),
                    {"name": migration_name}
                )
                db.session.commit()
                return True
            except Exception as e:
                print(f"❌ Error marking migration as applied: {e}")
                return False
    
    def get_pending_migrations(self):
        """Get list of migrations that haven't been applied yet"""
        applied = set(self.get_applied_migrations())
        all_migrations = []
        
        # Find all migration files
        for filename in sorted(os.listdir(self.migrations_dir)):
            if filename.endswith('.py') and filename != 'migrate.py' and not filename.startswith('__'):
                migration_name = filename[:-3]  # Remove .py extension
                if migration_name not in applied:
                    all_migrations.append(migration_name)
        
        return all_migrations
    
    def run_migration(self, migration_name):
        """Run a specific migration"""
        migration_path = os.path.join(self.migrations_dir, f"{migration_name}.py")
        
        if not os.path.exists(migration_path):
            print(f"❌ Migration file not found: {migration_path}")
            return False
        
        try:
            # Load the migration module
            spec = importlib.util.spec_from_file_location(migration_name, migration_path)
            migration_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration_module)
            
            # Run the upgrade function
            if hasattr(migration_module, 'upgrade'):
                print(f"🔄 Running migration: {migration_name}")
                success = migration_module.upgrade()
                
                if success:
                    self.mark_migration_applied(migration_name)
                    print(f"✅ Migration {migration_name} completed successfully")
                    return True
                else:
                    print(f"❌ Migration {migration_name} failed")
                    return False
            else:
                print(f"❌ Migration {migration_name} has no upgrade function")
                return False
                
        except Exception as e:
            print(f"❌ Error running migration {migration_name}: {e}")
            return False
    
    def migrate(self):
        """Run all pending migrations"""
        print("🏥 Arvindu Hospitals - Database Migration")
        print("=" * 50)
        
        # Ensure migration tracking table exists
        if not self.ensure_migration_table():
            return False
        
        # Get pending migrations
        pending = self.get_pending_migrations()
        
        if not pending:
            print("✅ No pending migrations. Database is up to date!")
            return True
        
        print(f"📋 Found {len(pending)} pending migration(s):")
        for migration in pending:
            print(f"   - {migration}")
        
        print("\n🔄 Running migrations...")
        
        # Run each migration
        for migration in pending:
            if not self.run_migration(migration):
                print(f"\n❌ Migration failed at: {migration}")
                return False
        
        print(f"\n✅ All migrations completed successfully!")
        return True
    
    def status(self):
        """Show migration status"""
        print("🏥 Arvindu Hospitals - Migration Status")
        print("=" * 50)
        
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()
        
        print(f"📊 Applied migrations: {len(applied)}")
        for migration in applied:
            print(f"   ✅ {migration}")
        
        print(f"\n📋 Pending migrations: {len(pending)}")
        for migration in pending:
            print(f"   ⏳ {migration}")
        
        if not pending:
            print("\n🎉 Database is up to date!")

def main():
    """Main function"""
    manager = MigrationManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "status":
            manager.status()
        elif command == "migrate":
            success = manager.migrate()
            sys.exit(0 if success else 1)
        else:
            print("Usage: python migrate.py [status|migrate]")
            sys.exit(1)
    else:
        # Default to migrate
        success = manager.migrate()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
