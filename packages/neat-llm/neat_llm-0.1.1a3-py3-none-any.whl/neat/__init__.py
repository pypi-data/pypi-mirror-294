"""
neat: A simpler LLM abstraction enabling quick development.
"""

from .config import neat_config, settings
from .main import Neat, neat
from .types import LLMModel

__all__ = [
    "Neat",
    "neat",
    "LLMModel",
    "settings",
    "neat_config",
]

__version__ = "0.1.1a3"
