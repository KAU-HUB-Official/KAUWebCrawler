from __future__ import annotations

import random
import time
from typing import Any
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests

from utils.logger import get_logger


class BaseClient:
    def __init__(
        self,
        *,
        base_url: str,
        user_agent: str,
        timeout: int,
        request_delay: tuple[float, float],
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url
        self.user_agent = user_agent
        self.timeout = timeout
        self.request_delay = request_delay
        self.verify_ssl = verify_ssl

        self.logger = get_logger(self.__class__.__name__)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )

        self._robots_loaded = False
        self._robots_parser: RobotFileParser | None = None
        self._request_count = 0

    def _load_robots(self) -> None:
        if self._robots_loaded:
            return

        self._robots_loaded = True
        robots_url = urljoin(self.base_url, "/robots.txt")
        parser = RobotFileParser()

        try:
            response = self.session.get(
                robots_url,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            if response.status_code >= 400:
                self.logger.warning(
                    "robots.txt request failed (%s): %s",
                    response.status_code,
                    robots_url,
                )
                return
            parser.parse(response.text.splitlines())
            self._robots_parser = parser
        except requests.RequestException as exc:
            self.logger.warning("robots.txt 확인 실패: %s (%s)", robots_url, exc)

    def can_fetch(self, url: str) -> bool:
        self._load_robots()
        if self._robots_parser is None:
            return True

        allowed = self._robots_parser.can_fetch(self.user_agent, url)
        if not allowed:
            self.logger.warning("robots.txt 정책으로 요청이 차단됨: %s", url)
        return allowed

    def _sleep_between_requests(self) -> None:
        if self._request_count <= 0:
            return
        delay = random.uniform(self.request_delay[0], self.request_delay[1])
        time.sleep(delay)

    def get(self, url: str, *, referer: str | None = None) -> str | None:
        if not self.can_fetch(url):
            return None

        self._sleep_between_requests()

        headers = {}
        if referer:
            headers["Referer"] = referer

        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            self._request_count += 1
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            self.logger.error("요청 실패: %s (%s)", url, exc)
            return None

    def post_json(
        self,
        url: str,
        payload: dict[str, Any],
        *,
        referer: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> str | None:
        if not self.can_fetch(url):
            return None

        self._sleep_between_requests()

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json, text/plain, */*",
        }
        if referer:
            headers["Referer"] = referer
        if extra_headers:
            headers.update(extra_headers)

        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            self._request_count += 1
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            self.logger.error("JSON POST 요청 실패: %s (%s)", url, exc)
            return None
