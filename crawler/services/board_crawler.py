from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from parsers.base_parser import BaseParser
from policies.notice_policy import evaluate_recent_policy
from services.url_normalizer import canonicalize_original_url
from utils.logger import get_logger

logger = get_logger("crawler.services.board_crawler")


@dataclass(frozen=True)
class DetailFetchResult:
    html: str | None
    failure_reason: str = "request_failed"


@dataclass(frozen=True)
class BoardAdapter:
    parser_factory: Callable[[dict[str, Any]], BaseParser]
    build_list_page_url: Callable[[dict[str, Any], int], str]
    fetch_list_html: Callable[[dict[str, Any], int], str | None]
    fetch_detail: Callable[[dict[str, Any], str], DetailFetchResult]
    can_fetch: Callable[[str], bool] | None = None
    check_robots_on_list: bool = False
    check_robots_on_detail: bool = False
    min_pages_field: str | None = None


def _normalize_page_items(raw_items: list[dict], *, page: int) -> list[dict]:
    normalized_items: list[dict] = []

    for raw in raw_items:
        detail_url = canonicalize_original_url(str(raw.get("url") or ""))
        if not detail_url:
            continue
        normalized_items.append(
            {
                "url": detail_url,
                "page": page,
                "is_permanent_notice": bool(raw.get("is_permanent_notice")),
            }
        )

    return normalized_items


def _select_new_items(page_items: list[dict], *, seen_urls: set[str]) -> list[dict]:
    new_items: list[dict] = []

    for item in page_items:
        detail_url = str(item.get("url") or "")
        if not detail_url or detail_url in seen_urls:
            continue
        seen_urls.add(detail_url)
        new_items.append(item)

    return new_items


def _dedup_items(items: list[dict]) -> list[dict]:
    deduped: list[dict] = []
    seen_urls: set[str] = set()

    for item in items:
        detail_url = str(item.get("url") or "")
        if not detail_url or detail_url in seen_urls:
            continue
        seen_urls.add(detail_url)
        deduped.append(item)

    return deduped


def _resolve_effective_max_pages(
    board: dict[str, Any],
    *,
    max_pages: int,
    adapter: BoardAdapter,
) -> int:
    effective_max_pages = max_pages
    if adapter.min_pages_field:
        min_pages = max(1, int(board.get(adapter.min_pages_field, 1)))
        effective_max_pages = max(effective_max_pages, min_pages)
    return effective_max_pages


def crawl_board(
    board: dict[str, Any],
    *,
    max_pages: int,
    adapter: BoardAdapter,
    known_urls: set[str],
) -> tuple[list[dict], list[dict]]:
    parser = adapter.parser_factory(board)

    failed_items: list[dict] = []
    detail_items: list[dict] = []
    seen_for_board: set[str] = set(known_urls)
    effective_max_pages = _resolve_effective_max_pages(board, max_pages=max_pages, adapter=adapter)

    for page in range(1, effective_max_pages + 1):
        page_url = adapter.build_list_page_url(board, page)

        if (
            adapter.check_robots_on_list
            and adapter.can_fetch is not None
            and not adapter.can_fetch(page_url)
        ):
            failed_items.append(
                {
                    "board": board["name"],
                    "url": page_url,
                    "reason": "robots_disallowed",
                }
            )
            logger.warning("[%s] robots.txt 차단으로 목록 스킵: %s", board["name"], page_url)
            # robots가 전역 차단인 경우가 많으므로 페이지 루프를 조기 종료한다.
            break

        html = adapter.fetch_list_html(board, page)

        if not html:
            logger.error(
                "[%s] 목록 요청 실패: page=%s, url=%s",
                board["name"],
                page,
                page_url,
            )
            continue

        page_items = _normalize_page_items(parser.parse_post_items(html, page_url), page=page)
        new_page_items = _select_new_items(page_items, seen_urls=seen_for_board)

        logger.info(
            "[%s] 목록 파싱 완료: page=%s, collected=%s, new=%s",
            board["name"],
            page,
            len(page_items),
            len(new_page_items),
        )
        detail_items.extend(new_page_items)

        # 목록이 최신순이라는 전제에서, 이미 알고 있는 URL만 나오면 이후 페이지도 중복일 가능성이 높다.
        if not new_page_items:
            logger.info("[%s] 신규 URL 없음, page=%s에서 목록 순회 조기 종료", board["name"], page)
            break

    detail_items = _dedup_items(detail_items)
    permanent_items = [item for item in detail_items if bool(item.get("is_permanent_notice"))]
    general_items = [item for item in detail_items if not bool(item.get("is_permanent_notice"))]
    ordered_detail_items = permanent_items + general_items
    logger.info(
        "[%s] 중복 제거 후 상세 URL 수: total=%s (permanent=%s, general=%s)",
        board["name"],
        len(ordered_detail_items),
        len(permanent_items),
        len(general_items),
    )

    posts: list[dict] = []

    for idx, detail_item in enumerate(ordered_detail_items, start=1):
        detail_url = str(detail_item["url"])
        source_page = int(detail_item["page"])
        is_permanent_notice = bool(detail_item["is_permanent_notice"])

        logger.info(
            "[%s] 상세 수집 중 (%s/%s): %s",
            board["name"],
            idx,
            len(ordered_detail_items),
            detail_url,
        )

        if (
            adapter.check_robots_on_detail
            and adapter.can_fetch is not None
            and not adapter.can_fetch(detail_url)
        ):
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "robots_disallowed",
                }
            )
            logger.warning("[%s] robots.txt 차단으로 상세 스킵: %s", board["name"], detail_url)
            continue

        fetch_result = adapter.fetch_detail(board, detail_url)
        if not fetch_result.html:
            if fetch_result.failure_reason == "missing_ntt_id":
                logger.warning("[%s] 상세 URL에 nttId 누락: %s", board["name"], detail_url)
            elif fetch_result.failure_reason == "missing_notice_id":
                logger.warning("[%s] 상세 URL에 notice id 누락: %s", board["name"], detail_url)
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": fetch_result.failure_reason,
                }
            )
            continue

        try:
            post = parser.parse_post(fetch_result.html, detail_url)
            post.original_url = canonicalize_original_url(post.original_url)
            if not post.title or not post.content:
                failed_items.append(
                    {
                        "board": board["name"],
                        "url": detail_url,
                        "reason": "required_field_empty",
                    }
                )
                logger.warning("[%s] 필수 필드 누락으로 스킵: %s", board["name"], detail_url)
                continue

            decision = evaluate_recent_policy(
                board_name=board["name"],
                detail_url=detail_url,
                source_page=source_page,
                is_permanent_notice=is_permanent_notice,
                published_at=post.published_at,
            )
            if not decision.include_post:
                if decision.stop_crawling:
                    logger.info(
                        "[%s] 정책에 따라 상세 수집 중단: page=%s, url=%s",
                        board["name"],
                        source_page,
                        detail_url,
                    )
                    break
                continue

            posts.append(post.to_dict())
            known_urls.add(post.original_url)
        except Exception as exc:  # noqa: BLE001
            logger.exception("[%s] 상세 파싱 실패: %s", board["name"], detail_url)
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": f"parse_error:{exc.__class__.__name__}",
                }
            )

    return posts, failed_items
