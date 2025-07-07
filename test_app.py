#!/usr/bin/env python3
"""
Test script for Arvindu Hospitals website
Run this to verify that the application is working correctly
"""

import unittest
import os
import tempfile
from app import app, db

class ArvindusHospitalTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_home_page(self):
        """Test that home page loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Arvindu Hospitals', rv.data)
    
    def test_about_page(self):
        """Test that about page loads correctly"""
        rv = self.app.get('/about')
        self.assertEqual(rv.status_code, 200)
    
    def test_appointment_page(self):
        """Test that appointment page loads correctly"""
        rv = self.app.get('/appointment')
        self.assertEqual(rv.status_code, 200)
    
    def test_contact_page(self):
        """Test that contact page loads correctly"""
        rv = self.app.get('/contact')
        self.assertEqual(rv.status_code, 200)
    
    def test_departments_page(self):
        """Test that departments page loads correctly"""
        rv = self.app.get('/departments')
        self.assertEqual(rv.status_code, 200)
    
    def test_doctors_page(self):
        """Test that doctors page loads correctly"""
        rv = self.app.get('/doctors')
        self.assertEqual(rv.status_code, 200)
    
    def test_404_page(self):
        """Test that 404 page works correctly"""
        rv = self.app.get('/nonexistent-page')
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    print("🧪 Running tests for Arvindu Hospitals website...")
    unittest.main(verbosity=2)
