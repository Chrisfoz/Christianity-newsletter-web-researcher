"""
Test that API keys are properly configured
"""
import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_exa_api_key_exists():
    """Test that EXA_API_KEY is set"""
    api_key = os.getenv('EXA_API_KEY')
    assert api_key is not None, "EXA_API_KEY not found in environment variables"
    assert len(api_key) > 0, "EXA_API_KEY is empty"
    assert api_key != "your-exa-api-key-here", "EXA_API_KEY is still using placeholder value"


def test_openai_api_key_exists():
    """Test that OPENAI_API_KEY is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    assert api_key is not None, "OPENAI_API_KEY not found in environment variables"
    assert len(api_key) > 0, "OPENAI_API_KEY is empty"
    assert api_key.startswith('sk-'), "OPENAI_API_KEY should start with 'sk-'"
    assert api_key != "your-openai-api-key-here", "OPENAI_API_KEY is still using placeholder value"


def test_api_keys_format():
    """Test that API keys have valid formats"""
    exa_key = os.getenv('EXA_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')

    # EXA key should be UUID-like format
    assert '-' in exa_key, "EXA_API_KEY should contain hyphens (UUID format)"

    # OpenAI key should have expected format
    assert len(openai_key) > 20, "OPENAI_API_KEY seems too short"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
