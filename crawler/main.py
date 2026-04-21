from __future__ import annotations

import argparse
from pathlib import Path

from config import DEFAULT_MAX_PAGES, FAILED_OUTPUT_FILE, NOTICE_BOARDS, OUTPUT_FILE
from services.board_crawler import crawl_board
from services.board_registry import build_board_adapters, build_clients
from services.dedup_service import merge_posts_with_dedup
from services.post_store import load_existing_posts
from services.url_normalizer import canonicalize_original_url
from utils.logger import get_logger
from utils.save_json import save_json

logger = get_logger("crawler.main")


def crawl_all_notices(max_pages: int, output_path: Path) -> tuple[list[dict], list[dict]]:
    clients = build_clients()
    adapters = build_board_adapters(clients)

    try:
        existing_posts = load_existing_posts(output_path)
        known_urls: set[str] = {
            canonicalize_original_url(str(post.get("original_url") or ""))
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

            adapter = adapters.get(board["board_type"])
            if adapter is None:
                logger.warning("지원하지 않는 board_type: %s", board["board_type"])
                continue

            posts, failed_items = crawl_board(
                board,
                max_pages=max_pages,
                adapter=adapter,
                known_urls=known_urls,
            )
            all_new_posts.extend(posts)
            all_failed_items.extend(failed_items)

        merge_result = merge_posts_with_dedup(existing_posts, all_new_posts)

        save_json(merge_result.posts, output_path)
        logger.info(
            "결과 저장 완료: %s (total=%s, newly_added=%s, url_dedup_removed=%s, title_dedup_removed=%s)",
            output_path,
            len(merge_result.posts),
            len(all_new_posts),
            merge_result.url_dedup_removed,
            merge_result.title_dedup_removed,
        )

        if all_failed_items:
            save_json(all_failed_items, FAILED_OUTPUT_FILE)
            logger.warning(
                "실패 로그 저장 완료: %s (count=%s)",
                FAILED_OUTPUT_FILE,
                len(all_failed_items),
            )
        elif FAILED_OUTPUT_FILE.exists():
            FAILED_OUTPUT_FILE.unlink()
            logger.info("실패 항목이 없어 기존 실패 로그 파일 삭제: %s", FAILED_OUTPUT_FILE)

        return merge_result.posts, all_failed_items
    finally:
        clients.close()


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
