from __future__ import annotations

import re
from abc import ABC, abstractmethod

from models.post import Post


class BaseParser(ABC):
    @abstractmethod
    def parse_post_urls(self, html: str, page_url: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def parse_post(self, html: str, detail_url: str) -> Post:
        raise NotImplementedError

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        return re.sub(r"[ \t]+", " ", text).strip()

    @staticmethod
    def normalize_newlines(text: str) -> str:
        text = text.replace("\r", "")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
