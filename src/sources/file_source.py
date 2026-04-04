from typing import Iterable, Iterator
from pathlib import Path
import json 
from datetime import datetime
import logging
from ..models import Task

logger=logging.getLogger(__name__)

def _parse_datetime(value:str)->datetime:
    try:
        return datetime.fromisoformat(value)
    except Exception:
        raise ValueError(f"Invalid datetime format: {value!r}")
    
class FileTaskSource:
    """
    Task source from json file
    """
    def __init__(self,path:str|Path):
        self.path=Path(path)

    def get_tasks(self) -> Iterable[Task]:
        if not self.path.exists():
            logger.error("Tasks file not found: %s", str(self.path))
            return []
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:
            logger.exception("Failed to read tasks file: %s", exc)
            return []

        return self._iter_from_raw(data)
    

    @staticmethod
    def _iter_from_raw(raw)->Iterator[Task]:
        if not isinstance(raw,list):
            logger.error("File must contain json array")
            return iter([])
        
        def gen():
            for idx, item in enumerate(raw):
                try:
                    t = Task(
                        id=str(item["id"]),
                        description=str(item.get("description", "")),
                        priority=int(item.get("priority", 0)),
                        status=str(item.get("status", "") or ""),
                        created_at=_parse_datetime(item["created_at"]),
                    )
                    yield t
                except Exception as e:
                    logger.error("Skipping invalid task at index %d: %s", idx, e)
                    continue
        return gen()