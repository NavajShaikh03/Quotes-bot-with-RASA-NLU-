"""
Quote recommender action for RASA chatbot.
Provides mood-based quotes using sentiment analysis.
"""
import json
import logging
import random
from typing import Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .config import Config
from .sentiment_service import analyze_sentiment

logger = logging.getLogger(__name__)


class ActionRecommendQuote(Action):
    """
    Custom action that recommends quotes based on user sentiment.
    
    This action:
    1. Analyzes the user's message for sentiment
    2. Loads quotes from the JSON file
    3. Selects an appropriate quote based on mood
    4. Returns the quote to the user
    """
    
    def name(self) -> str:
        """Return the unique action name."""
        return "action_recommend_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> List[Dict]:
        """
        Execute the action.
        
        Args:
            dispatcher: For sending messages back to user
            tracker: For accessing conversation state
            domain: The domain configuration
            
        Returns:
            List of events to update the conversation state
        """
        logger.info("Executing ActionRecommendQuote")
        
        # Get user message
        user_message = tracker.latest_message.get("text", "")
        logger.info(f"User message: {user_message}")
        
        if not user_message:
            logger.warning("No user message found")
            dispatcher.utter_message(text=Config.ERROR_MESSAGES["action_failed"])
            return []
        
        try:
            # Analyze sentiment
            mood = analyze_sentiment(user_message)
            logger.info(f"Detected mood: {mood}")
            
            # Get quote
            quote = self._get_quote(mood)
            
            # Send response
            dispatcher.utter_message(text=quote)
            logger.info(f"Sent quote for mood: {mood}")
            
            # Set mood slot for potential follow-up
            return [SlotSet("mood", mood)]
            
        except Exception as e:
            logger.error(f"Error in ActionRecommendQuote: {e}", exc_info=True)
            dispatcher.utter_message(text=Config.ERROR_MESSAGES["action_failed"])
            return []
    
    def _get_quote(self, mood: str) -> str:
        """
        Get a random quote for the given mood.
        
        Args:
            mood: The detected mood category
            
        Returns:
            A quote string
        """
        quotes = self._load_quotes()
        
        # Get quotes for the mood, or use fallback
        mood_quotes = quotes.get(mood, Config.FALLBACK_QUOTES.get(mood, []))
        
        if mood_quotes:
            quote = random.choice(mood_quotes)
            logger.debug(f"Selected quote for {mood}: {quote}")
            return quote
        
        # Ultimate fallback
        logger.warning(f"No quotes found for mood: {mood}, using default")
        return Config.ERROR_MESSAGES["quote_not_found"]
    
    def _load_quotes(self) -> Dict[str, List[str]]:
        """
        Load quotes from the JSON file.
        
        Returns:
            Dictionary of mood -> list of quotes
        """
        quotes_path = Config.get_quotes_path()
        
        if quotes_path is None:
            logger.info("Using fallback quotes")
            return Config.FALLBACK_QUOTES
        
        try:
            with open(quotes_path, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
                logger.info(f"Loaded {sum(len(v) for v in quotes.values())} quotes")
                return quotes
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in quotes file: {e}")
        except IOError as e:
            logger.error(f"Error reading quotes file: {e}")
        
        return Config.FALLBACK_QUOTES


class ActionShowMoodSummary(Action):
    """
    Action to show a summary of the user's mood based on conversation history.
    """
    
    def name(self) -> str:
        return "action_show_mood_summary"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> List[Dict]:
        """Show mood summary from conversation."""
        # Get mood history from slots
        mood = tracker.get_slot("mood")
        
        if mood:
            response = f"I noticed you're feeling {mood} today. "
            if mood == "sad":
                response += "I'm here for you. Would you like some encouragement?"
            elif mood == "happy":
                response += "That's wonderful to hear! Keep spreading that positivity!"
            else:
                response += "Stay focused on your goals!"
        else:
            response = "I haven't detected your mood yet. Tell me how you're feeling!"
        
        dispatcher.utter_message(text=response)
        return []


class ActionHandleMoodChange(Action):
    """
    Action to handle explicit mood change requests.
    """
    
    def name(self) -> str:
        return "action_handle_mood_change"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> List[Dict]:
        """Handle explicit mood change requests."""
        # Get user's requested mood from intent
        # This would typically come from an entity or slot
        current_mood = tracker.get_slot("mood")
        
        response_messages = {
            "sad": "I understand you're feeling down. Here's something to lift your spirits:",
            "happy": "I'm glad you're feeling positive! Here's a celebration quote:",
            "motivation": "Here's some inspiration to keep you going:"
        }
        
        # Get quote for current mood or motivation
        mood_to_show = current_mood if current_mood else "motivation"
        
        # Get a quote
        quotes = Config.FALLBACK_QUOTES.get(mood_to_show, [])
        if quotes:
            quote = random.choice(quotes)
            dispatcher.utter_message(text=response_messages.get(mood_to_show, "Here's a quote:"))
            dispatcher.utter_message(text=quote)
        
        return []
