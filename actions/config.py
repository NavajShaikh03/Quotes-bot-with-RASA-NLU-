"""
Central configuration for the RASA chatbot actions.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Config:
    """Central configuration class for the chatbot."""

    # Base directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Quote file paths (in order of priority)
    # Using single source: quotes/quotes.json
    QUOTE_PATHS = [
        BASE_DIR / "quotes" / "quotes.json",
        BASE_DIR / "app" / "data" / "quotes.json",
    ]

    # Sentiment thresholds
    SAD_THRESHOLD = -0.3
    HAPPY_THRESHOLD = 0.3

    # Fallback quotes
    FALLBACK_QUOTES: Dict[str, List[str]] = {
        "sad": [
            "Every storm runs out of rain.",
            "You are stronger than you think.",
            "Difficult roads lead to beautiful destinations.",
            "This too shall pass. Keep going."
        ],
        "happy": [
            "Happiness depends upon ourselves.",
            "Smile, it makes life beautiful.",
            "Your joy is contagious."
        ],
        "motivation": [
            "Push yourself because no one else will do it for you.",
            "Dream big and dare to fail.",
            "Success starts with self-discipline."
        ]
    }

    # Error messages
    ERROR_MESSAGES = {
        "sentiment_failed": "I'm here to help. Tell me how you're feeling.",
        "quote_not_found": "Stay positive and keep moving forward.",
        "action_failed": "I apologize, but I couldn't process that. Try again."
    }

    @classmethod
    def get_quotes_path(cls) -> Optional[Path]:
        """Find the first available quotes file."""
        for path in cls.QUOTE_PATHS:
            if path.exists():
                logger.info(f"Found quotes file at: {path}")
                return path
        logger.warning("No quotes.json found, using fallback quotes")
        return None
