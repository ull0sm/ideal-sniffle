#!/usr/bin/env python3
"""Verification script for Boeing India Career Chatbot."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports."""
    print("Testing imports...")
    
    try:
        from config.settings import settings
        print("  ✓ Settings imported")
    except Exception as e:
        print(f"  ✗ Settings import failed: {e}")
        return False
    
    try:
        from models.database import Base, User, Conversation, Message, Bookmark, Analytics, KnowledgeBase
        print("  ✓ Database models imported")
        print(f"    Tables: {', '.join([t.name for t in Base.metadata.tables.values()])}")
    except Exception as e:
        print(f"  ✗ Database models import failed: {e}")
        return False
    
    try:
        from utils.database import init_db, get_db
        print("  ✓ Database utilities imported")
    except Exception as e:
        print(f"  ✗ Database utilities import failed: {e}")
        return False
    
    try:
        from utils.auth import auth_manager
        print("  ✓ Auth manager imported")
    except Exception as e:
        print(f"  ✗ Auth manager import failed: {e}")
        return False
    
    try:
        from utils.conversation import conversation_manager
        print("  ✓ Conversation manager imported")
    except Exception as e:
        print(f"  ✗ Conversation manager import failed: {e}")
        return False
    
    try:
        from utils.rate_limit import rate_limiter
        print("  ✓ Rate limiter imported")
    except Exception as e:
        print(f"  ✗ Rate limiter import failed: {e}")
        return False
    
    try:
        from utils.analytics import analytics_manager
        print("  ✓ Analytics manager imported")
    except Exception as e:
        print(f"  ✗ Analytics manager import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database initialization."""
    print("\nTesting database...")
    
    try:
        from utils.database import init_db, get_db, engine
        from models.database import Base
        
        # Initialize database
        init_db()
        print("  ✓ Database initialized")
        
        # Check tables
        tables = Base.metadata.tables.keys()
        print(f"  ✓ Created tables: {', '.join(tables)}")
        
        # Test connection
        with get_db() as db:
            print("  ✓ Database connection successful")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def test_settings():
    """Test settings configuration."""
    print("\nTesting settings...")
    
    try:
        from config.settings import settings
        
        print(f"  ✓ App Name: {settings.APP_NAME}")
        print(f"  ✓ App Version: {settings.APP_VERSION}")
        print(f"  ✓ Max Tokens: {settings.MAX_TOKENS}")
        print(f"  ✓ Temperature: {settings.TEMPERATURE}")
        print(f"  ✓ Rate Limit (per min): {settings.RATE_LIMIT_PER_MINUTE}")
        print(f"  ✓ Rate Limit (per hour): {settings.RATE_LIMIT_PER_HOUR}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Settings test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Boeing India Career Chatbot - Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Settings", test_settings()))
    results.append(("Database", test_database()))
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nYou can now run the application:")
        print("  streamlit run app.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
