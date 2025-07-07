#!/usr/bin/env python3
"""
Test script for Netlify deployment
Tests the application without database to ensure it works in demo mode
"""

import os
import sys
import tempfile

# Set environment for testing
os.environ['FLASK_ENV'] = 'netlify'
os.environ.pop('DATABASE_URL', None)  # Remove database URL to test fallback

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_netlify_deployment():
    """Test the application in Netlify mode without database"""
    print("🧪 Testing Netlify deployment configuration...")
    
    try:
        # Create app in Netlify mode
        app = create_app('netlify')
        
        print("✅ App created successfully in Netlify mode")
        
        # Test basic routes
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            print(f"Home page: {response.status_code}")
            assert response.status_code == 200
            
            # Test about page
            response = client.get('/about')
            print(f"About page: {response.status_code}")
            assert response.status_code == 200
            
            # Test appointment page
            response = client.get('/appointment')
            print(f"Appointment page: {response.status_code}")
            assert response.status_code == 200
            
            # Test contact page
            response = client.get('/contact')
            print(f"Contact page: {response.status_code}")
            assert response.status_code == 200
            
            # Test departments page
            response = client.get('/departments')
            print(f"Departments page: {response.status_code}")
            assert response.status_code == 200
            
            # Test doctors page
            response = client.get('/doctors')
            print(f"Doctors page: {response.status_code}")
            assert response.status_code == 200
            
            # Test 404 handling
            response = client.get('/nonexistent-page')
            print(f"404 page: {response.status_code}")
            assert response.status_code == 404
            
            # Test form submission in demo mode
            response = client.post('/appointment', data={
                'name': 'Test Patient',
                'email': 'test@example.com',
                'phone': '1234567890',
                'department': 'cardiology',
                'date': '2024-12-31',
                'time': 'morning',
                'csrf_token': 'test'  # This will be handled by the form
            }, follow_redirects=True)
            print(f"Appointment form submission: {response.status_code}")
            # Should redirect and show demo message
            
        print("✅ All basic routes working correctly")
        print("✅ Application ready for Netlify deployment")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_serverless_function():
    """Test the serverless function handler"""
    print("\n🧪 Testing serverless function handler...")
    
    try:
        # Import the handler
        from netlify.functions.app import handler
        
        # Create a mock event
        event = {
            'httpMethod': 'GET',
            'path': '/.netlify/functions/app/',
            'headers': {},
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }
        
        # Test the handler
        response = handler(event, {})
        
        print(f"Handler response status: {response['statusCode']}")
        print(f"Handler response headers: {list(response['headers'].keys())}")
        
        assert response['statusCode'] == 200
        assert 'body' in response
        assert 'Arvindu Hospitals' in response['body']
        
        print("✅ Serverless function handler working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Serverless function test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🏥 Arvindu Hospitals - Netlify Deployment Test")
    print("=" * 60)
    
    success = True
    
    # Test basic app functionality
    if not test_netlify_deployment():
        success = False
    
    # Test serverless function
    if not test_serverless_function():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Ready for Netlify deployment")
        print("\n📋 Next steps:")
        print("1. Push code to GitHub")
        print("2. Connect repository to Netlify")
        print("3. Deploy!")
        print("\n💡 Optional: Add DATABASE_URL environment variable later")
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
