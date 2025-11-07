"""
Basic tests for the newsletter researcher functionality
"""
import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_environment_setup():
    """Test that the environment is properly set up"""
    assert os.getenv('EXA_API_KEY') is not None
    assert os.getenv('OPENAI_API_KEY') is not None


def test_researcher_imports():
    """Test that we can import the researcher module"""
    try:
        import researcher
        assert True
    except ImportError as e:
        pytest.fail(f"Could not import researcher module: {e}")


def test_required_dependencies():
    """Test that required packages are installed"""
    required_packages = [
        'openai',
        'exa_py',
        'dotenv',
        'pytest'
    ]

    for package in required_packages:
        try:
            __import__(package.replace('_', '-').replace('dotenv', 'python-dotenv'))
        except ImportError:
            pytest.fail(f"Required package '{package}' is not installed")


@pytest.mark.skipif(
    not os.getenv('EXA_API_KEY') or not os.getenv('OPENAI_API_KEY'),
    reason="API keys not configured"
)
def test_api_keys_loaded():
    """Test that API keys are loaded from environment"""
    exa_key = os.getenv('EXA_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    assert exa_key and len(exa_key) > 10
    assert openai_key and len(openai_key) > 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
