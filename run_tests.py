#!/usr/bin/env python3
"""
Test runner for SQL Optimizer backend
"""

import sys
import unittest
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def run_tests():
    """Run all backend tests"""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'backend')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running SQL Optimizer Backend Tests...")
    print("=" * 50)
    
    success = run_tests()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1) 