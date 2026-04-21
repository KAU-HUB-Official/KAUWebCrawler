# KAU Notice Hub Crawler

한국항공대학교 통합 공지 크롤러 프로젝트입니다.

## 최적화

### 문제-해결 매핑

| 문제 | 해결 |
| --- | --- |
| 게시판을 최신순으로 조회할 때 이미 수집한 공지를 다음 실행에서도 다시 상세 요청하는 오버헤드 발생 | 증분 수집 적용: 기존 `output/kau_official_posts.json`의 `original_url`을 캐시로 사용해 이미 수집한 URL 상세 요청 생략 |
| 같은 게시글이 `page`, `searchkey` 등 쿼리 파라미터만 달라진 URL로 중복 인식 | URL 정규화(canonical) 적용: 중복에 영향 없는 쿼리 파라미터 제거 후 동일 게시글 URL 통합 |
| 서로 다른 홈페이지/게시판에 동일 공지가 재게시될 때 URL이 달라 중복 저장 | 제목 기반 중복 제거 적용: URL 1차 중복 제거 후 제목 정규화(공백 정리, 소문자화) 기준으로 1건만 유지 |
| 새 공지가 거의 없는 상황에서도 여러 페이지를 끝까지 순회해 네트워크 비용 증가 | 목록 조기 종료 적용: 목록 페이지에서 신규 URL이 0개면 해당 게시판의 다음 페이지 순회 중단 |
| `robots.txt` 차단 게시판에서 반복 시도 시 불필요 요청/로그 누적 | robots 차단 조기 종료 적용: 차단 확인 시 페이지 루프 즉시 종료 (`kau_career` 보드는 사용자 요청으로 정책 예외 처리) |

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
