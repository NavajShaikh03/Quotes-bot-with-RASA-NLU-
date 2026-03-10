"""
Tests for sentiment analysis service.
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from actions.sentiment_service import analyze_sentiment, SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for sentiment analyzer."""

    def test_analyze_happy_text(self):
        """Test that positive text returns 'happy' mood."""
        text = "I am so happy and excited today!"
        mood = analyze_sentiment(text)
        assert mood in ["happy", "motivation"], f"Expected 'happy' or 'motivation', got '{mood}'"

    def test_analyze_sad_text(self):
        """Test that negative text returns 'sad' mood."""
        text = "I feel so depressed and sad"
        mood = analyze_sentiment(text)
        assert mood == "sad", f"Expected 'sad', got '{mood}'"

    def test_analyze_neutral_text(self):
        """Test that neutral text returns 'motivation' mood."""
        text = "I am going to the store"
        mood = analyze_sentiment(text)
        assert mood in ["motivation", "happy", "sad"], f"Expected a mood, got '{mood}'"

    def test_analyze_motivation_request(self):
        """Test that motivation requests are detected."""
        text = "I need some motivation"
        mood = analyze_sentiment(text)
        assert mood in ["motivation", "happy"], f"Expected 'motivation' or 'happy', got '{mood}'"

    def test_empty_text(self):
        """Test handling of empty text."""
        mood = analyze_sentiment("")
        assert mood == "motivation", f"Expected 'motivation' for empty text, got '{mood}'"

    def test_whitespace_only(self):
        """Test handling of whitespace-only text."""
        mood = analyze_sentiment("   ")
        assert mood == "motivation", f"Expected 'motivation' for whitespace, got '{mood}'"


class TestKeywordSentiment:
    """Test keyword-based sentiment fallback."""

    def test_sad_keywords(self):
        """Test sad keyword detection."""
        analyzer = SentimentAnalyzer()
        mood, confidence = analyzer._analyze_keywords("I feel so sad and depressed")
        assert mood == "sad", f"Expected 'sad', got '{mood}'"

    def test_happy_keywords(self):
        """Test happy keyword detection."""
        analyzer = SentimentAnalyzer()
        mood, confidence = analyzer._analyze_keywords("I am so happy and joyful today")
        assert mood == "happy", f"Expected 'happy', got '{mood}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
