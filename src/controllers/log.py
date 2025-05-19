from src.repositories import LogRepository
from src.schemas import CreateLog, LogResponse


class LogController:
    """Business logic for Log operations."""

    def __init__(self) -> None:
        """
        Initializes the LogController.

        Args:
            log_repository (LogRepository): Repository instance for interacting with Log model.
        """
        self.log_repository = LogRepository()

    def create_log(self, log_request: CreateLog) -> LogResponse:
        """
        Create users action log.
        """
        log = self.log_repository.create(attributes=log_request)

        return LogResponse(
            id=log.id,
            method=log.method,
            endpoint=log.endpoint,
            status=log.status,
            user_id=log.user_id,
        )
