"""
Configuration module for GATE Civil Bot.
Centralizes all configuration and provides validation.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class BotConfig:
    """Configuration container for the bot."""
    telegram_token: str
    channel_id: str
    gemini_api_key: str
    
    # Timeouts and retries
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 2
    
    # Cache settings
    cache_ttl: int = 3600  # 1 hour
    
    # Content settings
    default_difficulty: str = "medium"
    questions_per_topic: int = 5
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of warnings."""
        warnings = []
        
        if not self.telegram_token:
            warnings.append("TELEGRAM_BOT_TOKEN is not set - bot will not work")
        
        if not self.channel_id:
            warnings.append("TELEGRAM_CHANNEL_ID is not set - scheduled posting disabled")
        
        if not self.gemini_api_key:
            warnings.append("GEMINI_API_KEY is not set - AI features will be disabled")
        
        return warnings
    
    def is_valid(self) -> bool:
        """Check if minimum configuration is present."""
        return bool(self.telegram_token)
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """Create configuration from environment variables."""
        load_dotenv(override=True)
        
        config = cls(
            telegram_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            channel_id=os.getenv("TELEGRAM_CHANNEL_ID", ""),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=int(os.getenv("RETRY_DELAY", "2")),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            default_difficulty=os.getenv("DEFAULT_DIFFICULTY", "medium"),
        )
        
        # Log warnings
        for warning in config.validate():
            logger.warning(f"⚠️ Config: {warning}")
        
        return config


# Singleton config instance
_config: Optional[BotConfig] = None

def get_config() -> BotConfig:
    """Get or create the configuration instance."""
    global _config
    if _config is None:
        _config = BotConfig.from_env()
    return _config


# Topic definitions
TOPICS = {
    "SM": "Soil Mechanics",
    "FM": "Fluid Mechanics",
    "SA": "Structural Analysis",
    "RCC": "Reinforced Concrete Design",
    "STEEL": "Steel Structures",
    "GEO": "Geomatics / Surveying",
    "ENV": "Environmental Engineering",
    "TRANS": "Transportation Engineering",
    "HYDRO": "Hydrology & Irrigation",
    "CONST": "Construction Management"
}

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

# Topic emojis
TOPIC_EMOJIS = {
    "SM": "🏔️",
    "FM": "💧",
    "SA": "🏗️",
    "RCC": "🧱",
    "STEEL": "🔩",
    "GEO": "🗺️",
    "ENV": "🌿",
    "TRANS": "🛣️",
    "HYDRO": "🌊",
    "CONST": "📋"
}

def get_topic_name(code: str) -> str:
    """Get full topic name from code."""
    return TOPICS.get(code.upper(), "General")

def get_topic_emoji(code: str) -> str:
    """Get emoji for topic code."""
    return TOPIC_EMOJIS.get(code.upper(), "📚")
