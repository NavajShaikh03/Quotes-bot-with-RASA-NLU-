"""
Pytest configuration for RASA chatbot tests.
"""
import pytest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def sample_happy_text():
    """Sample happy text for testing."""
    return "I am so happy and excited today!"


@pytest.fixture
def sample_sad_text():
    """Sample sad text for testing."""
    return "I feel so depressed and sad"


@pytest.fixture
def sample_neutral_text():
    """Sample neutral text for testing."""
    return "I am going to the store"
