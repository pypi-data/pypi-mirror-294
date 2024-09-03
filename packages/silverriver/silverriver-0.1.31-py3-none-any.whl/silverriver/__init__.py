# This module defines the public API for the silverriver package.
# It provides core components for creating and interacting with
# web automation agents, including abstract interfaces and client classes.

from silverriver.interfaces.base_agent import AbstractAgent
from silverriver.interfaces.chat import AgentChatInterface
from .client import Crux, BrowserSession

__all__ = [
    "AbstractAgent",
    "AgentChatInterface",
    "Crux",
    "BrowserSession",
]
