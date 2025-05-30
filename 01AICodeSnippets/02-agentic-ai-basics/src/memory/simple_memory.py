from typing import List, Dict, Any
from datetime import datetime

class SimpleMemory:
    def __init__(self):
        self.short_term = []
        self.long_term = {}
        
    def add_to_short_term(self, item: Any):
        timestamp = datetime.now().isoformat()
        self.short_term.append({"timestamp": timestamp, "content": item})
        
        # Keep only last 10 items
        if len(self.short_term) > 10:
            self.short_term.pop(0)
    
    def add_to_long_term(self, key: str, value: Any):
        timestamp = datetime.now().isoformat()
        self.long_term[key] = {
            "timestamp": timestamp,
            "content": value
        }
    
    def get_short_term_memory(self) -> List[Dict]:
        return self.short_term
    
    def get_long_term_memory(self, key: str) -> Any:
        return self.long_term.get(key, {}).get("content") 