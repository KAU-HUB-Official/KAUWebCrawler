# 크롤링 규칙 상세

이 문서는 현재 크롤러의 수집 정책을 운영 관점에서 설명합니다.
기준 코드:

- `crawler/main.py`
- `crawler/services/board_crawler.py`
- `crawler/services/board_registry.py`
- `crawler/policies/notice_policy.py`
- `crawler/services/url_normalizer.py`
- `crawler/services/dedup_service.py`

## 1) 페이지 순회

- 목록은 `--max-pages` 기준으로 순회합니다.
- adapter에 `min_pages_field`가 있으면 `effective_max_pages = max(max_pages, min_pages)`를 사용합니다.
  - 예: `job_notice`는 `min_pages=2`
- 목록 항목은 `url`, `page`, `is_permanent_notice`로 관리합니다.
- 목록 페이지에서 신규 URL이 0건이면 해당 보드 순회를 조기 종료합니다.

## 2) 상세 수집 순서

- 목록 중복 제거 후 상세 대상은 다음 순서로 재정렬됩니다.
  1. 상시공지(`is_permanent_notice=true`)
  2. 일반공지(`is_permanent_notice=false`)
- 상시공지를 먼저 처리해 오래된 공지라도 누락되지 않도록 합니다.

## 3) 최근성 정책 (`RECENT_NOTICE_DAYS = 365`)

컷오프 계산:

- `cutoff_date = today - 365일`
- 최근 공지 판단식: `published_date > cutoff_date`

즉, 컷오프 날짜와 같은 날짜는 최근으로 보지 않습니다.

세부 동작:

- 상시공지
  - 게시일과 무관하게 포함
- 일반공지
  - `published_at` 파싱 성공 + `published_date > cutoff_date`인 경우만 포함
  - 그 외(컷오프 이전/같은 날짜, 게시일 미확인)는 제외 + 해당 보드 상세 수집 즉시 중단

## 4) 증분 수집

- 실행 시작 시 결과 파일(`--output`)의 `original_url`을 읽어 `known_urls` 캐시를 구성합니다.
- 캐시에 있는 URL은 상세 요청하지 않습니다.
- 새로 수집된 post의 canonical URL은 즉시 `known_urls`에 반영됩니다.

## 5) 중복 제거

- 1차: URL canonicalization 기준 중복 제거
- 2차: 제목 정규화 기준 통합
  - 공백 정리
  - 소문자화

제목 통합 시:

- 동일 제목 공지를 1건으로 저장
- `source_name`, `source_type`, `category_raw`를 배열로 병합
- `source_meta` 배열에 출처 메타 누적
- 첨부파일은 URL 기준으로 병합

## 6) 실패 기록

- `request_failed`
- `parse_error:<Exception>`
- `required_field_empty`
- `robots_disallowed`
- `missing_ntt_id` (`kau_college`)
- `missing_notice_id` (`kau_eslscat`)

## 7) 운영 시 참고

- `max_posts` 설정값은 현재 상세 수집 상한으로 직접 사용되지 않습니다.
- 정책 변경 시 다음 파일을 함께 업데이트해야 합니다.
  - `crawler/policies/notice_policy.py`
  - `crawler/services/board_crawler.py`
  - 본 문서(`docs/08_crawling_rules.md`)
