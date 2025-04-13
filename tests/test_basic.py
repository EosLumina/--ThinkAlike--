"""
Basic test file to verify test setup is working.
"""

def test_basic():
    """Simple test that always passes to verify test runner is working."""
    assert True, "Basic test should always pass"

def test_imports():
    """Test that required packages can be imported."""
    try:
        import httpx
        assert httpx is not None, "httpx should be importable"
    except ImportError:
        assert False, "httpx should be installed"

    try:
        import pandas as pd
        assert pd is not None, "pandas should be importable"
    except ImportError:
        assert False, "pandas should be installed"
