# KAU Notice Hub Crawler

한국항공대학교 통합 공지 크롤러 프로젝트입니다.

## 현재 범위

- `kau.ac.kr` 공지 게시판 7종
- `career.kau.ac.kr` 대학일자리센터 공지사항 게시판(`https://career.kau.ac.kr/ko/community/notice`)
- `college.kau.ac.kr` 공지 게시판 2종
  - 국제교류처(`gc63585b`)
  - 인권센터(`gc22052b`)
- `research.kau.ac.kr` 산학협력단 공지사항
- `ibhak.kau.ac.kr` 입학처 공지사항
- `ctl.kau.ac.kr` 교수학습센터 공지사항
- `lib.kau.ac.kr` 학술정보관 일반공지
- `ftc.kau.ac.kr` 비행교육원 공지사항
- `amtc.kau.ac.kr` 항공기술교육원 공지사항
- `college.kau.ac.kr` 생활관/항공교통관제교육원/항공안전교육원/평생교육원 공지사항
- `aerospacemuseum.or.kr` 박물관 공지사항(실제 수집은 `college.kau.ac.kr` 공지 페이지)

## 최적화

### 문제-해결 매핑

| 문제                                                                                              | 해결                                                                                                                  |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 게시판을 최신순으로 조회할 때 이미 수집한 공지를 다음 실행에서도 다시 상세 요청하는 오버헤드 발생 | 증분 수집 적용: 기존 `output/kau_official_posts.json`의 `original_url`을 캐시로 사용해 이미 수집한 URL 상세 요청 생략 |
| 같은 게시글이 `page`, `searchkey` 등 쿼리 파라미터만 달라진 URL로 중복 인식                       | URL 정규화(canonical) 적용: 중복에 영향 없는 쿼리 파라미터 제거 후 동일 게시글 URL 통합                               |
| 서로 다른 홈페이지/게시판에 동일 공지가 재게시될 때 URL이 달라 중복 저장                          | 제목 기반 중복 제거 적용: URL 1차 중복 제거 후 제목 정규화(공백 정리, 소문자화) 기준으로 1건만 유지                   |
| 새 공지가 거의 없는 상황에서도 여러 페이지를 끝까지 순회해 네트워크 비용 증가                     | 목록 조기 종료 적용: 목록 페이지에서 신규 URL이 0개면 해당 게시판의 다음 페이지 순회 중단                             |
| `robots.txt` 차단 게시판에서 반복 시도 시 불필요 요청/로그 누적                                   | robots 차단 조기 종료 적용: 차단 확인 시 페이지 루프 즉시 종료 (`kau_career` 보드는 사용자 요청으로 정책 예외 처리)   |

## 크롤링 규칙 (요약)

- 게시판별 기본 목표 수집 건수는 `max_posts=20`입니다.
- 목록 수집은 `--max-pages` 범위 내에서 페이지를 순회합니다.
- 목록 항목은 `url + is_permanent_notice(상시공지 여부)`로 수집합니다.
- 기존 결과 파일의 `original_url`(canonical)을 캐시로 사용해 이미 수집한 URL은 상세 요청에서 제외합니다.
- 목록 페이지에서 신규 URL이 0건이면 해당 게시판 목록 순회를 조기 종료합니다.
- 상세 수집 규칙:
  - 상시공지(`is_permanent_notice=true`)는 게시일이 1년을 초과하거나 게시일을 확인할 수 없어도 수집합니다.
  - 일반공지는 `RECENT_NOTICE_DAYS=365` 이내 게시글만 수집합니다.
  - 일반공지에서 1년 초과/게시일 미확인 글을 만나면, 같은 페이지의 남은 일반공지 상세 수집은 생략하고 다음 페이지 항목으로 넘어갑니다.
  - `title` 또는 `content`가 비어 있으면 `required_field_empty`로 실패 처리합니다.
- 최종 결과 저장 전 중복 제거:
  - 1차: canonical `original_url` 기준 중복 제거
  - 2차: 제목 정규화(공백 정리 + 소문자화) 기준 중복 제거

상시공지 총량이 많은 게시판(예: 학사공지)에서 상시 공지를 더 많이 포함하려면 `--max-pages`를 늘리고, 필요 시 해당 보드의 `max_posts`도 함께 조정하세요.

## 빠른 실행

```bash
pip install requests beautifulsoup4
python3 crawler/main.py --max-pages 1
```

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
- [크롤링 규칙 상세](./docs/08_crawling_rules.md)

## 산출물

- `output/kau_official_posts.json`
- `output/kau_official_failed.json`
- `output/crawler.log`
