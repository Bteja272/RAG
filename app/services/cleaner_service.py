import re


class TextCleanerService:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        text = text.replace("\x00", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()