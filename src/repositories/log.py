from src.models import Log
from src.repositories import BaseRepository


class LogRepository(BaseRepository[Log]):
    """Repository for Log model operations."""

    def __init__(self):
        super().__init__(Log)
