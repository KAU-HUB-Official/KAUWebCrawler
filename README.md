# KAU Notice Hub Crawler

한국항공대학교 통합 공지 크롤러 프로젝트입니다.

## 최적화

### 문제 상황

- 게시판을 최신순으로 조회할 때, 이미 수집한 공지를 다음 실행에서도 다시 상세 요청하는 오버헤드가 발생했습니다.
- 같은 게시글이 `page`, `searchkey` 같은 쿼리 파라미터만 달라진 URL로 중복 인식될 수 있었습니다.
- 새 공지가 거의 없는 상황에서도 여러 페이지를 끝까지 순회해 불필요한 네트워크 비용이 발생했습니다.

### 해결 방법

- 증분 수집: 기존 `output/kau_official_posts.json`의 `original_url`을 캐시로 사용해 이미 수집한 URL은 상세 요청을 생략합니다.
- URL 정규화(canonical): 중복에 영향 없는 쿼리 파라미터를 제거해 동일 게시글 URL을 하나로 통합합니다.
- 조기 종료: 목록 페이지에서 신규 URL이 0개면 해당 게시판의 다음 페이지 순회를 중단합니다.
- robots 차단 조기 종료: `robots.txt`로 차단된 게시판은 첫 차단 시 페이지 루프를 즉시 종료합니다.

## 문서 안내

세부 문서는 `docs/`로 분리했습니다.

- [문서 인덱스](./docs/README.md)
- [프로젝트 개요](./docs/01_project_overview.md)
- [실행 가이드](./docs/02_quickstart.md)
- [크롤링 대상](./docs/03_crawl_targets.md)
- [아키텍처](./docs/04_architecture.md)
- [파싱 규칙과 셀렉터](./docs/05_parsing_and_selectors.md)
- [운영/장애 대응](./docs/06_operations_and_failure.md)
- [확장 가이드](./docs/07_extension_guide.md)

## 빠른 실행

```bash
pip install requests beautifulsoup4
python3 crawler/main.py --max-pages 1
```

## 산출물

- `output/kau_official_posts.json`
- `output/kau_official_failed.json`
- `output/crawler.log`
