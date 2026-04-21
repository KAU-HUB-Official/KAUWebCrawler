from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from config import RECENT_NOTICE_DAYS
from utils.logger import get_logger

logger = get_logger("crawler.policies.notice_policy")


@dataclass(frozen=True)
class RecentPolicyDecision:
    include_post: bool
    skip_rest_general_in_page: bool


def parse_published_date(published_at: str | None) -> date | None:
    if not published_at:
        return None

    # 파서별 포맷(YYYY-MM-DD, YYYY.MM.DD, YYYY-MM-DD HH:MM 등)에서 날짜만 추출한다.
    match = re.search(r"(\d{4})[./-](\d{1,2})[./-](\d{1,2})", str(published_at))
    if not match:
        return None

    year, month, day = (int(value) for value in match.groups())
    try:
        return date(year, month, day)
    except ValueError:
        return None


def is_recent_notice(published_at: str | None, *, lookback_days: int = RECENT_NOTICE_DAYS) -> bool:
    published_date = parse_published_date(published_at)
    if not published_date:
        return False

    cutoff_date = datetime.now().date() - timedelta(days=lookback_days)
    return published_date >= cutoff_date


def evaluate_recent_policy(
    *,
    board_name: str,
    detail_url: str,
    source_page: int,
    is_permanent_notice: bool,
    published_at: str | None,
) -> RecentPolicyDecision:
    """
    Returns:
      - include_post: 결과 저장 여부
      - skip_rest_general_in_page: 현재 페이지의 나머지 일반공지 상세 수집 생략 여부
    """
    if is_permanent_notice:
        if is_recent_notice(published_at):
            return RecentPolicyDecision(include_post=True, skip_rest_general_in_page=False)
        logger.info(
            "[%s] 상시공지로 간주하여 날짜 필터 예외 적용: published_at=%s, page=%s, url=%s",
            board_name,
            published_at,
            source_page,
            detail_url,
        )
        return RecentPolicyDecision(include_post=True, skip_rest_general_in_page=False)

    if is_recent_notice(published_at):
        return RecentPolicyDecision(include_post=True, skip_rest_general_in_page=False)

    logger.info(
        "[%s] 일반공지 1년 초과 또는 게시일 미확인으로 스킵 후 다음 페이지 이동: published_at=%s, page=%s, url=%s",
        board_name,
        published_at,
        source_page,
        detail_url,
    )
    return RecentPolicyDecision(include_post=False, skip_rest_general_in_page=True)
