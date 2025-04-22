import json
import os
import threading
import time
from typing import Dict, Any, Optional

class DiffStore:
    """A thread-safe storage mechanism to replace Flask session."""
    
    def __init__(self, expiry_seconds: int = 3600, storage_file: str = 'diff_store.json'):
        self.lock = threading.RLock()
        self.data: Dict[str, Dict[str, Any]] = {}
        self.expiry_seconds = expiry_seconds
        self.storage_file = storage_file
        self._load_from_file()
    
    def _load_from_file(self) -> None:
        """Load data from file if it exists."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    stored_data = json.load(f)
                    # Only load non-expired data
                    current_time = time.time()
                    with self.lock:
                        for key, value in stored_data.items():
                            if value.get('expiry', 0) > current_time:
                                self.data[key] = value
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or can't be read, start with empty data
            self.data = {}
    
    def _save_to_file(self) -> None:
        """Save data to file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f)
        except IOError:
            # If we can't write to file, just continue with in-memory storage
            pass
    
    def set(self, session_id: str, key: str, value: Any) -> None:
        """Set a value in the store."""
        with self.lock:
            if session_id not in self.data:
                self.data[session_id] = {'expiry': time.time() + self.expiry_seconds}
            self.data[session_id][key] = value
            self._save_to_file()
    
    def get(self, session_id: str, key: str, default: Any = None) -> Any:
        """Get a value from the store."""
        with self.lock:
            self._cleanup_expired()
            session_data = self.data.get(session_id, {})
            return session_data.get(key, default)
    
    def delete(self, session_id: str) -> None:
        """Delete a session from the store."""
        with self.lock:
            if session_id in self.data:
                del self.data[session_id]
                self._save_to_file()
    
    def _cleanup_expired(self) -> None:
        """Clean up expired sessions."""
        current_time = time.time()
        expired_keys = []
        
        for key, value in self.data.items():
            if value.get('expiry', 0) < current_time:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.data[key]
        
        if expired_keys:
            self._save_to_file()

# Create a singleton instance
diff_store = DiffStore()
