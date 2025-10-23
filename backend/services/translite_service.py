import re
from typing import Union
from transliterate import translit
from services.logger_service import logger


class TransliteService:
    @staticmethod
    def translite(text: Union[str, None]) -> str:
        if text is None:
            return ""
        try:
            text = translit(
                text.strip().replace(" ", "_"), language_code="ru", reversed=True
            )
            clean_text = re.sub("[^a-zA-Z0-9_]", "", f"{text}")
            return clean_text
        except Exception as e:
            logger.error(f"Не удалось выполнить транслит: {e}")
            raise ValueError(f"Не удалось выполнить транслит: {e}")
