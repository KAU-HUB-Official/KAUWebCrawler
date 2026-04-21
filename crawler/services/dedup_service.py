from __future__ import annotations

import re
from dataclasses import dataclass

from services.url_normalizer import canonicalize_original_url
from utils.logger import get_logger

logger = get_logger("crawler.services.dedup_service")


@dataclass(frozen=True)
class MergeResult:
    posts: list[dict]
    url_dedup_removed: int
    title_dedup_removed: int


def normalize_title_for_dedup(title: str | None) -> str:
    if not title:
        return ""

    # 사이트별 공백/대소문자 차이를 줄여 제목 기반 중복 판단 키를 만든다.
    normalized = re.sub(r"\s+", " ", str(title)).strip().lower()
    return normalized


def merge_posts_with_dedup(existing_posts: list[dict], new_posts: list[dict]) -> MergeResult:
    url_dedup_posts: list[dict] = []
    seen_urls: set[str] = set()

    # 기존 보유 데이터를 먼저 유지하고, 신규 데이터를 뒤에 병합한다.
    for post in existing_posts + new_posts:
        original_url = canonicalize_original_url(str(post.get("original_url") or ""))
        if not original_url or original_url in seen_urls:
            continue
        copied = dict(post)
        copied["original_url"] = original_url
        seen_urls.add(original_url)
        url_dedup_posts.append(copied)

    dedup_posts: list[dict] = []
    seen_titles: set[str] = set()
    title_dedup_removed = 0

    # 제목이 동일한 공지는 서로 다른 홈페이지여도 같은 공지로 간주해 1건만 유지한다.
    for post in url_dedup_posts:
        title_key = normalize_title_for_dedup(str(post.get("title") or ""))
        if title_key and title_key in seen_titles:
            title_dedup_removed += 1
            logger.info(
                "제목 중복으로 스킵: title=%s, url=%s",
                post.get("title"),
                post.get("original_url"),
            )
            continue
        if title_key:
            seen_titles.add(title_key)
        dedup_posts.append(post)

    url_dedup_removed = len(existing_posts) + len(new_posts) - len(url_dedup_posts)
    return MergeResult(
        posts=dedup_posts,
        url_dedup_removed=url_dedup_removed,
        title_dedup_removed=title_dedup_removed,
    )
