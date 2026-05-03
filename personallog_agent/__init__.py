"""
PLATO PersonalLog Agent — Personal Journal for personallog.ai

Personal journal entries, life events, reflection tracking.
Every entry logged to PLATO as a functional tile for later reflection.
"""

import time
import requests
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

DEFAULT_PLATO_URL = "http://localhost:8847"
ROOM = "personallog-ai"


@dataclass
class JournalEntry:
    """A journal entry tile."""
    title: str
    entry_text: str
    entry_type: str = "daily"  # "daily" | "reflection" | "milestone" | "grateful"
    tags: List[str] = None
    mood: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class PersonalLogAgent:
    """
    Personal journal agent.
    
    Logs journal entries, life events, reflections to PLATO.
    Tracks personal growth over time through vessel accumulation.
    """
    
    def __init__(self, user_id: str = "default", plato_url: str = DEFAULT_PLATO_URL):
        self.user_id = user_id
        self.plato_url = plato_url.rstrip("/")
        self.room = ROOM
    
    def _write(self, entry_type: str, data: Dict[str, Any]) -> bool:
        tile = {
            "question": f"journal:{entry_type}",
            "answer": str(data),
            "confidence": 0.9,
            "metadata": {
                "user_id": self.user_id,
                "entry_type": entry_type,
                "timestamp": time.time(),
                **data
            }
        }
        try:
            resp = requests.post(f"{self.plato_url}/room/{self.room}", json=tile, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def log_entry(
        self,
        title: str,
        entry_text: str,
        entry_type: str = "daily",
        tags: Optional[List[str]] = None,
        mood: Optional[str] = None
    ) -> bool:
        """Log a journal entry."""
        return self._write(entry_type, {
            "title": title,
            "entry_text": entry_text,
            "tags": tags or [],
            "mood": mood,
        })
    
    def log_milestone(self, title: str, description: str) -> bool:
        """Log a life milestone."""
        return self._write("milestone", {"title": title, "description": description})
    
    def ask(self, question: str) -> str:
        """Query journal entries from PLATO."""
        try:
            resp = requests.get(f"{self.plato_url}/room/{self.room}?limit=20", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                relevant = [t for t in tiles if any(w in str(t).lower() for w in question.lower().split()[:3])]
                if relevant:
                    return f"Found {len(relevant)} entries: {relevant[-1].get('answer', '')[:200]}"
        except:
            pass
        return "Journal system unavailable."
