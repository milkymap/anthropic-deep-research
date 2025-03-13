from enum import Enum 
from pydantic import BaseModel 

from typing import List, Dict 

class Role(str, Enum):
    USER : str = "user"
    SYSTEM : str = "system"
    DEVELOPPER : str = "developper"
    ASSISTANT : str = "assistant"

class ChatMessage(BaseModel):
    role:Role 
    content: str | List[Dict]


class StopReason(str, Enum):
    END_TURN: str = "end_turn"
    MAX_TOKENS: str = "max_tokens"
    TOOL_USE: str = "tool_use"
    STOP_SEQUENCE: str = "stop_sequence"