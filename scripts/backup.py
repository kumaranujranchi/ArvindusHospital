#!/usr/bin/env python3
"""
Database backup script for Arvindu Hospitals
Creates backups of the database and provides restore functionality
"""

import os
import sys
import json
import gzip
import subprocess
from datetime import datetime, timedelta
from urllib.parse import urlparse

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db
from models import Appointment, ContactMessage, Newsletter

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, compress=True):
        """Create a database backup"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        with app.app_context():
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
            
            if database_url.startswith('sqlite'):
                return self._backup_sqlite(timestamp, compress)
            elif database_url.startswith('postgresql'):
                return self._backup_postgresql(timestamp, compress)
            else:
                print(f"❌ Unsupported database type: {database_url}")
                return False
    
    def _backup_sqlite(self, timestamp, compress):
        """Backup SQLite database"""
        try:
            # For SQLite, we can copy the file or export data
            backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.json')
            
            data = {
                'timestamp': timestamp,
                'appointments': [],
                'contact_messages': [],
                'newsletter_subscribers': []
            }
            
            # Export appointments
            appointments = Appointment.query.all()
            for apt in appointments:
                data['appointments'].append({
                    'id': apt.id,
                    'name': apt.name,
                    'email': apt.email,
                    'phone': apt.phone,
                    'department': apt.department,
                    'doctor': apt.doctor,
                    'date': apt.date.isoformat() if apt.date else None,
                    'time': apt.time,
                    'message': apt.message,
                    'created_at': apt.created_at.isoformat() if apt.created_at else None
                })
            
            # Export contact messages
            messages = ContactMessage.query.all()
            for msg in messages:
                data['contact_messages'].append({
                    'id': msg.id,
                    'name': msg.name,
                    'email': msg.email,
                    'subject': msg.subject,
                    'message': msg.message,
                    'created_at': msg.created_at.isoformat() if msg.created_at else None
                })
            
            # Export newsletter subscribers
            subscribers = Newsletter.query.all()
            for sub in subscribers:
                data['newsletter_subscribers'].append({
                    'id': sub.id,
                    'email': sub.email,
                    'created_at': sub.created_at.isoformat() if sub.created_at else None
                })
            
            # Write backup file
            if compress:
                backup_file += '.gz'
                with gzip.open(backup_file, 'wt', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            
            print(f"✅ SQLite backup created: {backup_file}")
            print(f"   - Appointments: {len(data['appointments'])}")
            print(f"   - Contact Messages: {len(data['contact_messages'])}")
            print(f"   - Newsletter Subscribers: {len(data['newsletter_subscribers'])}")
            
            return backup_file
            
        except Exception as e:
            print(f"❌ SQLite backup failed: {e}")
            return False
    
    def _backup_postgresql(self, timestamp, compress):
        """Backup PostgreSQL database"""
        try:
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
            parsed = urlparse(database_url)
            
            backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.sql')
            
            # Use pg_dump to create backup
            cmd = [
                'pg_dump',
                '--host', parsed.hostname,
                '--port', str(parsed.port or 5432),
                '--username', parsed.username,
                '--dbname', parsed.path[1:],  # Remove leading slash
                '--file', backup_file,
                '--verbose',
                '--no-password'
            ]
            
            # Set password via environment variable
            env = os.environ.copy()
            if parsed.password:
                env['PGPASSWORD'] = parsed.password
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                if compress:
                    # Compress the backup file
                    with open(backup_file, 'rb') as f_in:
                        with gzip.open(backup_file + '.gz', 'wb') as f_out:
                            f_out.writelines(f_in)
                    os.remove(backup_file)
                    backup_file += '.gz'
                
                print(f"✅ PostgreSQL backup created: {backup_file}")
                return backup_file
            else:
                print(f"❌ PostgreSQL backup failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ PostgreSQL backup failed: {e}")
            return False
    
    def list_backups(self):
        """List available backups"""
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.startswith('backup_'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_mtime)
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep_days=30):
        """Remove backups older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=keep_days)
        removed_count = 0
        
        for backup in self.list_backups():
            if backup['created'] < cutoff_date:
                try:
                    os.remove(backup['filepath'])
                    print(f"🗑️  Removed old backup: {backup['filename']}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Failed to remove {backup['filename']}: {e}")
        
        print(f"✅ Cleanup complete. Removed {removed_count} old backup(s)")
        return removed_count
    
    def restore_backup(self, backup_file):
        """Restore from backup file"""
        if not os.path.exists(backup_file):
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        print("⚠️  WARNING: This will replace all existing data!")
        confirm = input("Type 'RESTORE' to confirm: ")
        
        if confirm != 'RESTORE':
            print("❌ Restore cancelled")
            return False
        
        with app.app_context():
            try:
                if backup_file.endswith('.json') or backup_file.endswith('.json.gz'):
                    return self._restore_json_backup(backup_file)
                elif backup_file.endswith('.sql') or backup_file.endswith('.sql.gz'):
                    return self._restore_sql_backup(backup_file)
                else:
                    print(f"❌ Unsupported backup format: {backup_file}")
                    return False
                    
            except Exception as e:
                print(f"❌ Restore failed: {e}")
                return False
    
    def _restore_json_backup(self, backup_file):
        """Restore from JSON backup"""
        # Load backup data
        if backup_file.endswith('.gz'):
            with gzip.open(backup_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)
        else:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Clear existing data
        db.session.query(Appointment).delete()
        db.session.query(ContactMessage).delete()
        db.session.query(Newsletter).delete()
        
        # Restore appointments
        for apt_data in data.get('appointments', []):
            apt = Appointment(
                name=apt_data['name'],
                email=apt_data['email'],
                phone=apt_data['phone'],
                department=apt_data['department'],
                doctor=apt_data['doctor'],
                date=datetime.fromisoformat(apt_data['date']).date() if apt_data['date'] else None,
                time=apt_data['time'],
                message=apt_data['message']
            )
            if apt_data['created_at']:
                apt.created_at = datetime.fromisoformat(apt_data['created_at'])
            db.session.add(apt)
        
        # Restore contact messages
        for msg_data in data.get('contact_messages', []):
            msg = ContactMessage(
                name=msg_data['name'],
                email=msg_data['email'],
                subject=msg_data['subject'],
                message=msg_data['message']
            )
            if msg_data['created_at']:
                msg.created_at = datetime.fromisoformat(msg_data['created_at'])
            db.session.add(msg)
        
        # Restore newsletter subscribers
        for sub_data in data.get('newsletter_subscribers', []):
            sub = Newsletter(email=sub_data['email'])
            if sub_data['created_at']:
                sub.created_at = datetime.fromisoformat(sub_data['created_at'])
            db.session.add(sub)
        
        db.session.commit()
        
        print(f"✅ Restore completed from {backup_file}")
        print(f"   - Appointments: {len(data.get('appointments', []))}")
        print(f"   - Contact Messages: {len(data.get('contact_messages', []))}")
        print(f"   - Newsletter Subscribers: {len(data.get('newsletter_subscribers', []))}")

        return True

    def _restore_sql_backup(self, backup_file):
        """Restore from SQL backup (PostgreSQL)"""
        try:
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
            parsed = urlparse(database_url)

            # Use psql to restore backup
            if backup_file.endswith('.gz'):
                cmd = f"gunzip -c {backup_file} | psql"
            else:
                cmd = f"psql -f {backup_file}"

            cmd += f" --host {parsed.hostname}"
            cmd += f" --port {parsed.port or 5432}"
            cmd += f" --username {parsed.username}"
            cmd += f" --dbname {parsed.path[1:]}"  # Remove leading slash

            # Set password via environment variable
            env = os.environ.copy()
            if parsed.password:
                env['PGPASSWORD'] = parsed.password

            result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ SQL restore completed from {backup_file}")
                return True
            else:
                print(f"❌ SQL restore failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ SQL restore failed: {e}")
            return False

def main():
    """Main backup function"""
    backup_manager = DatabaseBackup()
    
    if len(sys.argv) < 2:
        print("Usage: python backup.py [create|list|cleanup|restore] [options]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        compress = '--no-compress' not in sys.argv
        backup_file = backup_manager.create_backup(compress=compress)
        if backup_file:
            print(f"🎉 Backup created successfully: {backup_file}")
        else:
            sys.exit(1)
    
    elif command == 'list':
        backups = backup_manager.list_backups()
        if backups:
            print("📋 Available backups:")
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                print(f"   {backup['filename']} ({size_mb:.1f}MB) - {backup['created']}")
        else:
            print("📋 No backups found")
    
    elif command == 'cleanup':
        keep_days = 30
        if len(sys.argv) > 2:
            try:
                keep_days = int(sys.argv[2])
            except ValueError:
                print("❌ Invalid number of days")
                sys.exit(1)
        
        backup_manager.cleanup_old_backups(keep_days)
    
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Please specify backup file to restore")
            sys.exit(1)
        
        backup_file = sys.argv[2]
        if backup_manager.restore_backup(backup_file):
            print("🎉 Restore completed successfully")
        else:
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
