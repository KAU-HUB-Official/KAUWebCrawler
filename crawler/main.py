from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse, urlunparse

from clients.kau_career_client import KAUCareerClient
from clients.kau_college_client import KAUCollegeClient
from clients.kau_official_client import KAUOfficialClient
from clients.kau_research_client import KAUResearchClient
from config import (
    DEFAULT_MAX_PAGES,
    DEFAULT_POSTS_PER_BOARD,
    FAILED_OUTPUT_FILE,
    NOTICE_BOARDS,
    OUTPUT_FILE,
)
from parsers.kau_career_parser import KAUCareerParser
from parsers.kau_college_parser import KAUCollegeParser
from parsers.kau_official_parser import KAUOfficialParser
from parsers.kau_research_parser import KAUResearchParser
from utils.logger import get_logger
from utils.save_json import save_json

logger = get_logger("crawler.main")


def canonicalize_original_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except Exception:  # noqa: BLE001
        return url

    scheme = parsed.scheme or "https"
    netloc = parsed.netloc
    path = parsed.path
    host = netloc.lower()

    # KAU 공식 공지 상세 URL:
    #   /kaulife/{board}.php?...&code=sXXXX&page=..&mode=read&seq=NNNN
    # 여기서 중복에 영향 없는 page/searchkey/searchvalue는 제거한다.
    if host.endswith("kau.ac.kr") and path.startswith("/kaulife/") and path.endswith(".php"):
        query = parse_qs(parsed.query, keep_blank_values=True)
        if "mode" in query and "seq" in query:
            compact_query: dict[str, str] = {}
            if query.get("code"):
                compact_query["code"] = query["code"][-1]
            compact_query["mode"] = query["mode"][-1]
            compact_query["seq"] = query["seq"][-1]
            normalized_query = urlencode(compact_query)
            return urlunparse((scheme, netloc, path, "", normalized_query, ""))

    # 취업공지 상세 URL:
    #   /ko/dataroom/data/view/{id}?p=1
    # p 파라미터 제거.
    if host.endswith("career.kau.ac.kr") and "/ko/dataroom/data/view/" in path:
        return urlunparse((scheme, netloc, path.rstrip("/"), "", "", ""))

    # college.kau.ac.kr 공지 상세 URL:
    #   /web/pages/gc63585b.do?...&bbsId=0123&nttId=NNNN
    # 중복에 영향 없는 쿼리 파라미터는 제거한다.
    if host.endswith("college.kau.ac.kr") and path.startswith("/web/pages/") and path.endswith(".do"):
        query = parse_qs(parsed.query, keep_blank_values=True)
        if query.get("bbsId") and query.get("nttId"):
            compact_query: dict[str, str] = {
                "bbsId": query["bbsId"][-1],
                "nttId": query["nttId"][-1],
            }
            if query.get("mnuId"):
                compact_query["mnuId"] = query["mnuId"][-1]
            normalized_query = urlencode(compact_query)
            return urlunparse((scheme, netloc, path, "", normalized_query, ""))

    # research.kau.ac.kr 공지 상세 URL:
    #   /info/info_011.php?...&code=s2101&page=..&mode=read&seq=NNNN
    # 중복에 영향 없는 page/search 파라미터를 제거한다.
    if host.endswith("research.kau.ac.kr") and path.startswith("/info/") and path.endswith(".php"):
        query = parse_qs(parsed.query, keep_blank_values=True)
        if "mode" in query and "seq" in query:
            compact_query: dict[str, str] = {}
            if query.get("code"):
                compact_query["code"] = query["code"][-1]
            compact_query["mode"] = query["mode"][-1]
            compact_query["seq"] = query["seq"][-1]
            normalized_query = urlencode(compact_query)
            return urlunparse((scheme, netloc, path, "", normalized_query, ""))

    # generic fallback: fragment 제거 + 쿼리 키 정렬
    query_items = parse_qsl(parsed.query, keep_blank_values=True)
    normalized_query = urlencode(sorted(query_items)) if query_items else ""
    return urlunparse((scheme, netloc, path, "", normalized_query, ""))


def load_existing_posts(output_path: Path) -> list[dict]:
    if not output_path.exists():
        return []

    try:
        with output_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:  # noqa: BLE001
        logger.warning("기존 결과 파일 로드 실패: %s (%s)", output_path, exc)
        return []

    if not isinstance(data, list):
        logger.warning("기존 결과 파일 형식이 list가 아님: %s", output_path)
        return []

    valid_items = [item for item in data if isinstance(item, dict) and item.get("original_url")]
    if len(valid_items) != len(data):
        logger.warning(
            "기존 결과 파일의 일부 항목이 유효하지 않아 제외됨: valid=%s total=%s",
            len(valid_items),
            len(data),
        )

    normalized_items: list[dict] = []
    for item in valid_items:
        copied = dict(item)
        copied["original_url"] = canonicalize_original_url(str(copied["original_url"]))
        normalized_items.append(copied)
    return normalized_items


def crawl_kau_official_board(
    board: dict,
    *,
    max_pages: int,
    client: KAUOfficialClient,
    known_urls: set[str],
) -> tuple[list[dict], list[dict]]:
    parser = KAUOfficialParser(
        source_name=board["source_name"],
        source_type=board["source_type"],
    )

    detail_urls: list[str] = []
    seen_for_board: set[str] = set(known_urls)
    target_posts = max(1, int(board.get("max_posts", DEFAULT_POSTS_PER_BOARD)))

    for page in range(1, max_pages + 1):
        page_url = client.build_board_list_url(
            list_url=board["list_url"],
            code=board["code"],
            page=page,
        )
        html = client.fetch_board_list(
            list_url=board["list_url"],
            code=board["code"],
            page=page,
        )

        if not html:
            logger.error(
                "[%s] 목록 요청 실패: page=%s, url=%s",
                board["name"],
                page,
                page_url,
            )
            continue

        page_urls = [canonicalize_original_url(url) for url in parser.parse_post_urls(html, page_url)]
        new_page_urls = [url for url in page_urls if url not in seen_for_board]
        seen_for_board.update(new_page_urls)

        logger.info(
            "[%s] 목록 파싱 완료: page=%s, collected=%s, new=%s",
            board["name"],
            page,
            len(page_urls),
            len(new_page_urls),
        )
        detail_urls.extend(new_page_urls)

        if len(detail_urls) >= target_posts:
            logger.info("[%s] 목표 수집 건수 도달(%s), 목록 순회 종료", board["name"], target_posts)
            break

        # 목록이 최신순이라는 전제에서, 이미 알고 있는 URL만 나오면 이후 페이지도 중복일 가능성이 높다.
        if not new_page_urls:
            logger.info("[%s] 신규 URL 없음, page=%s에서 목록 순회 조기 종료", board["name"], page)
            break

    detail_urls = list(dict.fromkeys(detail_urls))[:target_posts]
    logger.info(
        "[%s] 중복 제거 후 상세 URL 수: %s (max_posts=%s)",
        board["name"],
        len(detail_urls),
        target_posts,
    )

    posts: list[dict] = []
    failed_items: list[dict] = []

    for idx, detail_url in enumerate(detail_urls, start=1):
        logger.info(
            "[%s] 상세 수집 중 (%s/%s): %s",
            board["name"],
            idx,
            len(detail_urls),
            detail_url,
        )

        html = client.fetch_detail(detail_url, referer=board["list_url"])
        if not html:
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "request_failed",
                }
            )
            continue

        try:
            post = parser.parse_post(html, detail_url)
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

            posts.append(post.to_dict())
            known_urls.add(detail_url)
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


def crawl_kau_career_board(
    board: dict,
    *,
    max_pages: int,
    client: KAUCareerClient,
    known_urls: set[str],
) -> tuple[list[dict], list[dict]]:
    parser = KAUCareerParser(
        source_name=board["source_name"],
        source_type=board["source_type"],
    )

    posts: list[dict] = []
    failed_items: list[dict] = []
    detail_urls: list[str] = []
    seen_for_board: set[str] = set(known_urls)
    target_posts = max(1, int(board.get("max_posts", DEFAULT_POSTS_PER_BOARD)))

    for page in range(1, max_pages + 1):
        page_url = client.build_notice_list_url(page)

        if not client.can_fetch(page_url):
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
            continue

        html = client.fetch_notice_list(page)

        if not html:
            logger.error(
                "[%s] 목록 요청 실패: page=%s, url=%s",
                board["name"],
                page,
                page_url,
            )
            continue

        page_urls = [canonicalize_original_url(url) for url in parser.parse_post_urls(html, page_url)]
        new_page_urls = [url for url in page_urls if url not in seen_for_board]
        seen_for_board.update(new_page_urls)

        logger.info(
            "[%s] 목록 파싱 완료: page=%s, collected=%s, new=%s",
            board["name"],
            page,
            len(page_urls),
            len(new_page_urls),
        )
        detail_urls.extend(new_page_urls)

        if len(detail_urls) >= target_posts:
            logger.info("[%s] 목표 수집 건수 도달(%s), 목록 순회 종료", board["name"], target_posts)
            break

        if not new_page_urls:
            logger.info("[%s] 신규 URL 없음, page=%s에서 목록 순회 조기 종료", board["name"], page)
            break

    detail_urls = list(dict.fromkeys(detail_urls))[:target_posts]
    logger.info(
        "[%s] 중복 제거 후 상세 URL 수: %s (max_posts=%s)",
        board["name"],
        len(detail_urls),
        target_posts,
    )

    for idx, detail_url in enumerate(detail_urls, start=1):
        logger.info(
            "[%s] 상세 수집 중 (%s/%s): %s",
            board["name"],
            idx,
            len(detail_urls),
            detail_url,
        )

        if not client.can_fetch(detail_url):
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "robots_disallowed",
                }
            )
            logger.warning("[%s] robots.txt 차단으로 상세 스킵: %s", board["name"], detail_url)
            continue

        html = client.fetch_notice_detail(detail_url)
        if not html:
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "request_failed",
                }
            )
            continue

        try:
            post = parser.parse_post(html, detail_url)
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

            posts.append(post.to_dict())
            known_urls.add(detail_url)
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


def crawl_kau_college_board(
    board: dict,
    *,
    max_pages: int,
    client: KAUCollegeClient,
    known_urls: set[str],
) -> tuple[list[dict], list[dict]]:
    parser = KAUCollegeParser(
        source_name=board["source_name"],
        source_type=board["source_type"],
        notice_page_url=board["list_url"],
        site_flag=board["site_flag"],
        mnu_id=board["mnu_id"],
        bbs_id=board["bbs_id"],
        category_raw=board.get("name"),
    )

    posts: list[dict] = []
    failed_items: list[dict] = []
    detail_urls: list[str] = []
    seen_for_board: set[str] = set(known_urls)
    target_posts = max(1, int(board.get("max_posts", DEFAULT_POSTS_PER_BOARD)))

    for page in range(1, max_pages + 1):
        page_url = board["list_url"]

        if not client.can_fetch(page_url):
            failed_items.append(
                {
                    "board": board["name"],
                    "url": page_url,
                    "reason": "robots_disallowed",
                }
            )
            logger.warning("[%s] robots.txt 차단으로 목록 스킵: %s", board["name"], page_url)
            break

        response_text = client.fetch_notice_list(
            site_flag=board["site_flag"],
            bbs_id=board["bbs_id"],
            bbs_auth=board["bbs_auth"],
            page_index=page,
            page_unit=max(1, int(board.get("page_unit", target_posts))),
        )

        if not response_text:
            logger.error(
                "[%s] 목록 요청 실패: page=%s, url=%s",
                board["name"],
                page,
                page_url,
            )
            continue

        page_urls = [
            canonicalize_original_url(url)
            for url in parser.parse_post_urls(response_text, page_url)
        ]
        new_page_urls = [url for url in page_urls if url not in seen_for_board]
        seen_for_board.update(new_page_urls)

        logger.info(
            "[%s] 목록 파싱 완료: page=%s, collected=%s, new=%s",
            board["name"],
            page,
            len(page_urls),
            len(new_page_urls),
        )
        detail_urls.extend(new_page_urls)

        if len(detail_urls) >= target_posts:
            logger.info("[%s] 목표 수집 건수 도달(%s), 목록 순회 종료", board["name"], target_posts)
            break

        if not new_page_urls:
            logger.info("[%s] 신규 URL 없음, page=%s에서 목록 순회 조기 종료", board["name"], page)
            break

    detail_urls = list(dict.fromkeys(detail_urls))[:target_posts]
    logger.info(
        "[%s] 중복 제거 후 상세 URL 수: %s (max_posts=%s)",
        board["name"],
        len(detail_urls),
        target_posts,
    )

    for idx, detail_url in enumerate(detail_urls, start=1):
        logger.info(
            "[%s] 상세 수집 중 (%s/%s): %s",
            board["name"],
            idx,
            len(detail_urls),
            detail_url,
        )

        query = parse_qs(urlparse(detail_url).query)
        ntt_id = (query.get("nttId") or [""])[-1]
        bbs_id = (query.get("bbsId") or [board["bbs_id"]])[-1]
        if not ntt_id:
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "missing_ntt_id",
                }
            )
            logger.warning("[%s] 상세 URL에 nttId 누락: %s", board["name"], detail_url)
            continue

        response_text = client.fetch_notice_detail(
            site_flag=board["site_flag"],
            bbs_id=bbs_id,
            ntt_id=ntt_id,
            mnu_id=board["mnu_id"],
            bbs_auth=board["bbs_auth"],
        )
        if not response_text:
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "request_failed",
                }
            )
            continue

        try:
            post = parser.parse_post(response_text, detail_url)
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


def crawl_kau_research_board(
    board: dict,
    *,
    max_pages: int,
    client: KAUResearchClient,
    known_urls: set[str],
) -> tuple[list[dict], list[dict]]:
    parser = KAUResearchParser(
        source_name=board["source_name"],
        source_type=board["source_type"],
        category_fallback=board.get("name"),
    )

    detail_urls: list[str] = []
    seen_for_board: set[str] = set(known_urls)
    target_posts = max(1, int(board.get("max_posts", DEFAULT_POSTS_PER_BOARD)))

    for page in range(1, max_pages + 1):
        page_url = client.build_board_list_url(
            list_url=board["list_url"],
            code=board["code"],
            page=page,
        )
        html = client.fetch_board_list(
            list_url=board["list_url"],
            code=board["code"],
            page=page,
        )

        if not html:
            logger.error(
                "[%s] 목록 요청 실패: page=%s, url=%s",
                board["name"],
                page,
                page_url,
            )
            continue

        page_urls = [canonicalize_original_url(url) for url in parser.parse_post_urls(html, page_url)]
        new_page_urls = [url for url in page_urls if url not in seen_for_board]
        seen_for_board.update(new_page_urls)

        logger.info(
            "[%s] 목록 파싱 완료: page=%s, collected=%s, new=%s",
            board["name"],
            page,
            len(page_urls),
            len(new_page_urls),
        )
        detail_urls.extend(new_page_urls)

        if len(detail_urls) >= target_posts:
            logger.info("[%s] 목표 수집 건수 도달(%s), 목록 순회 종료", board["name"], target_posts)
            break

        if not new_page_urls:
            logger.info("[%s] 신규 URL 없음, page=%s에서 목록 순회 조기 종료", board["name"], page)
            break

    detail_urls = list(dict.fromkeys(detail_urls))[:target_posts]
    logger.info(
        "[%s] 중복 제거 후 상세 URL 수: %s (max_posts=%s)",
        board["name"],
        len(detail_urls),
        target_posts,
    )

    posts: list[dict] = []
    failed_items: list[dict] = []

    for idx, detail_url in enumerate(detail_urls, start=1):
        logger.info(
            "[%s] 상세 수집 중 (%s/%s): %s",
            board["name"],
            idx,
            len(detail_urls),
            detail_url,
        )

        html = client.fetch_detail(detail_url, referer=board["list_url"])
        if not html:
            failed_items.append(
                {
                    "board": board["name"],
                    "url": detail_url,
                    "reason": "request_failed",
                }
            )
            continue

        try:
            post = parser.parse_post(html, detail_url)
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


def crawl_all_notices(max_pages: int, output_path: Path) -> tuple[list[dict], list[dict]]:
    official_client = KAUOfficialClient()
    career_client = KAUCareerClient()
    college_client = KAUCollegeClient()
    research_client = KAUResearchClient()

    existing_posts = load_existing_posts(output_path)
    known_urls: set[str] = {
        canonicalize_original_url(str(post["original_url"]))
        for post in existing_posts
        if post.get("original_url")
    }

    all_new_posts: list[dict] = []
    all_failed_items: list[dict] = []

    logger.info(
        "공지 게시판 수집 시작: 게시판=%s, 페이지=%s, 기존보유URL=%s",
        len(NOTICE_BOARDS),
        max_pages,
        len(known_urls),
    )

    for board in NOTICE_BOARDS:
        logger.info("게시판 수집 시작: %s", board["name"])

        if board["board_type"] == "kau_official":
            posts, failed_items = crawl_kau_official_board(
                board,
                max_pages=max_pages,
                client=official_client,
                known_urls=known_urls,
            )
        elif board["board_type"] == "kau_career":
            posts, failed_items = crawl_kau_career_board(
                board,
                max_pages=max_pages,
                client=career_client,
                known_urls=known_urls,
            )
        elif board["board_type"] == "kau_college":
            posts, failed_items = crawl_kau_college_board(
                board,
                max_pages=max_pages,
                client=college_client,
                known_urls=known_urls,
            )
        elif board["board_type"] == "kau_research":
            posts, failed_items = crawl_kau_research_board(
                board,
                max_pages=max_pages,
                client=research_client,
                known_urls=known_urls,
            )
        else:
            logger.warning("지원하지 않는 board_type: %s", board["board_type"])
            continue

        all_new_posts.extend(posts)
        all_failed_items.extend(failed_items)

    dedup_posts: list[dict] = []
    seen_urls: set[str] = set()

    # 기존 보유 데이터를 먼저 유지하고, 신규 데이터를 뒤에 병합한다.
    for post in existing_posts + all_new_posts:
        original_url = canonicalize_original_url(str(post["original_url"]))
        if original_url in seen_urls:
            continue
        post["original_url"] = original_url
        seen_urls.add(original_url)
        dedup_posts.append(post)

    save_json(dedup_posts, output_path)
    logger.info(
        "결과 저장 완료: %s (total=%s, newly_added=%s)",
        output_path,
        len(dedup_posts),
        len(all_new_posts),
    )

    if all_failed_items:
        save_json(all_failed_items, FAILED_OUTPUT_FILE)
        logger.warning(
            "실패 로그 저장 완료: %s (count=%s)",
            FAILED_OUTPUT_FILE,
            len(all_failed_items),
        )

    return dedup_posts, all_failed_items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="한국항공대학교 통합 공지 크롤러",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help=f"게시판별 수집할 목록 페이지 수 (기본값: {DEFAULT_MAX_PAGES})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_FILE,
        help=f"결과 JSON 저장 경로 (기본값: {OUTPUT_FILE})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    crawl_all_notices(max_pages=args.max_pages, output_path=args.output)


if __name__ == "__main__":
    main()
