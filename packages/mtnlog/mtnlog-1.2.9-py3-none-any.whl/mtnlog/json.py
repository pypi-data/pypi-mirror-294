import json
import os
from typing import Any, Union, Dict, List, TypeVar

# Define generic type variables
K = TypeVar('K')
V = TypeVar('V')

class JSONLogger:
    """Arguments logger class."""

    def __init__(self, log_dir: str) -> None:
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir: str = log_dir

    def serialize(
        self, obj: Any
    ) -> Union[Dict[str, Any], List[Any], int, float, str, bool, None]:
        """Custom serialization for non-serializable objects."""
        if isinstance(obj, dict):
            return {k: self.serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.serialize(v) for v in obj]
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        # Convert non-serializable objects to their string representation
        return str(obj)

    def log(self, obj: Any, filename: str = "log") -> None:
        """Logs the object."""
        with open(f"{self.log_dir}/{filename}.json", "w", encoding='utf-8') as f:
            json.dump(self.serialize(obj), f, ensure_ascii=False, indent=4)