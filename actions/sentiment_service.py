"""
Sentiment analysis service for the chatbot.
Supports both TextBlob and VADER sentiment analysis.
"""
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment analyzer using multiple backends for better accuracy.
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self._textblob_available = False
        self._vader_available = False
        self._init_analyzers()
    
    def _init_analyzers(self):
        """Initialize available sentiment analyzers."""
        # Try to import TextBlob
        try:
            from textblob import TextBlob
            self.TextBlob = TextBlob
            self._textblob_available = True
            logger.info("TextBlob sentiment analyzer initialized")
        except ImportError:
            logger.warning("TextBlob not available")
        
        # Try to import VADER
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader = SentimentIntensityAnalyzer()
            self._vader_available = True
            logger.info("VADER sentiment analyzer initialized")
        except ImportError:
            logger.warning("VADER not available")
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (mood: str, confidence: float)
            mood can be: "sad", "happy", or "motivation"
            confidence is between -1.0 and 1.0
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to sentiment analyzer")
            return "motivation", 0.0
        
        # Try VADER first (generally better for social media text)
        if self._vader_available:
            return self._analyze_vader(text)
        
        # Fall back to TextBlob
        if self._textblob_available:
            return self._analyze_textblob(text)
        
        # Ultimate fallback - keyword-based
        logger.warning("No sentiment analyzers available, using keyword matching")
        return self._analyze_keywords(text)
    
    def _analyze_vader(self, text: str) -> Tuple[str, float]:
        """Analyze using VADER sentiment analyzer."""
        try:
            scores = self.vader.polarity_scores(text)
            compound = scores['compound']
            
            mood = self._polarity_to_mood(compound)
            logger.info(f"VADER analysis: text='{text[:30]}...' score={compound:.3f} mood={mood}")
            
            return mood, compound
        except Exception as e:
            logger.error(f"VADER analysis failed: {e}")
            return self._analyze_textblob(text)
    
    def _analyze_textblob(self, text: str) -> Tuple[str, float]:
        """Analyze using TextBlob sentiment analyzer."""
        try:
            analysis = self.TextBlob(text)
            polarity = analysis.sentiment.polarity
            
            mood = self._polarity_to_mood(polarity)
            logger.info(f"TextBlob analysis: text='{text[:30]}...' score={polarity:.3f} mood={mood}")
            
            return mood, polarity
        except Exception as e:
            logger.error(f"TextBlob analysis failed: {e}")
            return self._analyze_keywords(text)
    
    def _analyze_keywords(self, text: str) -> Tuple[str, float]:
        """Fallback keyword-based sentiment analysis."""
        text_lower = text.lower()
        
        # Negative keywords
        sad_keywords = ['sad', 'depressed', 'unhappy', 'angry', 'stressed', 'anxious', 
                       'worried', 'hurt', 'pain', 'crying', 'cry', 'miss', 'lost',
                       'failed', 'failure', 'tired', 'exhausted', 'sick']
        
        # Positive keywords
        happy_keywords = ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing',
                         'love', 'loving', 'fantastic', 'excellent', 'good', 'best',
                         'blessed', 'grateful', 'thankful', 'fun', 'enjoy']
        
        sad_count = sum(1 for word in sad_keywords if word in text_lower)
        happy_count = sum(1 for word in happy_keywords if word in text_lower)
        
        if sad_count > happy_count:
            return "sad", -0.5
        elif happy_count > sad_count:
            return "happy", 0.5
        else:
            return "motivation", 0.0
    
    def _polarity_to_mood(self, polarity: float) -> str:
        """Convert polarity score to mood category."""
        from .config import Config
        
        if polarity < Config.SAD_THRESHOLD:
            return "sad"
        elif polarity > Config.HAPPY_THRESHOLD:
            return "happy"
        else:
            return "motivation"


# Singleton instance
_analyzer: Optional[SentimentAnalyzer] = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create the sentiment analyzer singleton."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer


def analyze_sentiment(text: str) -> str:
    """
    Convenience function to analyze sentiment.
    
    Args:
        text: Input text
        
    Returns:
        Mood category: "sad", "happy", or "motivation"
    """
    analyzer = get_sentiment_analyzer()
    mood, confidence = analyzer.analyze(text)
    return mood
