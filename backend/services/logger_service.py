import logging
from pathlib import Path


class LoggerService:
    def __init__(self, log_file: str = "app.log"):
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_path = log_dir / log_file

        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            encoding="utf-8",
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)


logger = LoggerService("app.log")
