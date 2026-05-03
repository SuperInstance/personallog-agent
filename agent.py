#!/usr/bin/env python3
"""personallog-agent — Personal logging and life tracking"""
import json, time
from typing import List, Dict

class PersonalLogAgent:
    def __init__(self, plato_url="http://147.224.38.131:8847"):
        self.plato_url = plato_url
        self.entries: List[Dict] = []
    
    def log_entry(self, mood: str, energy: int, highlight: str, gratitude: str=""):
        entry = {"mood": mood, "energy": energy, "highlight": highlight, "gratitude": gratitude, "time": time.time()}
        self.entries.append(entry)
        self._submit(f"Daily entry: {mood}", f"Energy {energy}/10. Highlight: {highlight}. Grateful for: {gratitude}")
        return entry
    
    def get_insights(self) -> Dict:
        if not self.entries: return {"error": "No entries"}
        moods = {}
        for e in self.entries: moods[e["mood"]] = moods.get(e["mood"], 0) + 1
        avg_energy = sum(e["energy"] for e in self.entries) / len(self.entries)
        return {"total_entries": len(self.entries), "mood_distribution": moods, "avg_energy": round(avg_energy, 1), "latest_highlight": self.entries[-1]["highlight"]}
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "personallog-agent", "room": "personallog"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = PersonalLogAgent()
    a.log_entry("content", 7, "Finished refactoring the fleet dashboard", "Grateful for quiet morning")
    a.log_entry("excited", 9, "Oracle1 merged 3 PRs", "Team momentum")
    a.log_entry("tired", 5, "Long debugging session", "Coffee supply")
    print(a.get_insights())

if __name__ == "__main__": demo()
