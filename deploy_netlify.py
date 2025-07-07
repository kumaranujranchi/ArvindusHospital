#!/usr/bin/env python3
"""
Netlify deployment script for Arvindu Hospitals
Deploys the application directly to Netlify using the CLI
"""

import os
import sys
import subprocess
import json

def check_netlify_cli():
    """Check if Netlify CLI is installed"""
    try:
        result = subprocess.run(['netlify', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Netlify CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Netlify CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Netlify CLI not installed")
        return False

def check_netlify_auth():
    """Check if user is authenticated with Netlify"""
    try:
        result = subprocess.run(['netlify', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Authenticated with Netlify")
            return True
        else:
            print("❌ Not authenticated with Netlify")
            return False
    except Exception:
        print("❌ Error checking Netlify authentication")
        return False

def run_tests():
    """Run pre-deployment tests"""
    print("🧪 Running pre-deployment tests...")
    try:
        result = subprocess.run(['python3', 'test_netlify.py'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def deploy_to_netlify():
    """Deploy the application to Netlify"""
    print("🚀 Deploying to Netlify...")
    
    try:
        # Deploy to Netlify
        result = subprocess.run(['netlify', 'deploy', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(result.stdout)
            
            # Extract the URL from the output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Website URL:' in line or 'Live Draft URL:' in line:
                    url = line.split(':', 1)[1].strip()
                    print(f"🌐 Your site is live at: {url}")
                    return url
            
            return True
        else:
            print("❌ Deployment failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False

def setup_environment_variables():
    """Guide user through setting up environment variables"""
    print("\n🔧 Environment Variables Setup")
    print("=" * 50)
    print("For production deployment, you should set these environment variables:")
    print("1. DATABASE_URL - Your external database connection string")
    print("2. SESSION_SECRET - A secure random string for sessions")
    print("\nTo set environment variables:")
    print("  netlify env:set DATABASE_URL 'your-database-url'")
    print("  netlify env:set SESSION_SECRET 'your-secret-key'")
    print("\nRecommended database services:")
    print("  - Supabase (PostgreSQL) - Free tier available")
    print("  - PlanetScale (MySQL) - Free tier available")
    print("  - Railway (PostgreSQL) - Free tier available")

def main():
    """Main deployment function"""
    print("🏥 Arvindu Hospitals - Netlify Deployment")
    print("=" * 60)
    
    # Check prerequisites
    if not check_netlify_cli():
        print("\n📥 Please install Netlify CLI:")
        print("  npm install -g netlify-cli")
        print("  or")
        print("  brew install netlify-cli")
        sys.exit(1)
    
    if not check_netlify_auth():
        print("\n🔐 Please authenticate with Netlify:")
        print("  netlify login")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed. Please fix issues before deploying.")
        sys.exit(1)
    
    # Deploy
    result = deploy_to_netlify()
    
    if result:
        print("\n🎉 Deployment completed successfully!")
        setup_environment_variables()
        
        print("\n📋 Next steps:")
        print("1. Test your deployed site")
        print("2. Set up environment variables (optional)")
        print("3. Configure custom domain (optional)")
        print("4. Set up monitoring and analytics")
        
        print("\n🔧 Useful Netlify commands:")
        print("  netlify open          - Open your site in browser")
        print("  netlify logs          - View function logs")
        print("  netlify env:list      - List environment variables")
        print("  netlify deploy        - Deploy draft version")
        print("  netlify deploy --prod - Deploy to production")
        
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
