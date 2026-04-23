# 크롤링 규칙 상세

이 문서는 현재 크롤러가 게시판을 수집할 때 적용하는 정책을 운영 관점에서 정리한 기준 문서입니다.

## 적용 코드
- 실행 오케스트레이션: `crawler/main.py`
- 보드 공통 수집 엔진: `crawler/services/board_crawler.py`
- 보드 타입별 매핑: `crawler/services/board_registry.py`
- 기간 설정: `crawler/config.py` (`RECENT_NOTICE_DAYS = 365`)
- 최근성/상시공지 정책: `crawler/policies/notice_policy.py`
- URL 정규화/중복 병합: `crawler/services/url_normalizer.py`, `crawler/services/dedup_service.py`
- 목록 항목 메타(`is_permanent_notice`) 판정: 각 parser의 `parse_post_items`

## 1) 수집 한도와 페이지 순회
- 게시판 기본 목표 수집 건수는 `max_posts=20`입니다.
- 목록은 `--max-pages` 범위 내에서 페이지 단위로 순회합니다.
- 목록 항목은 URL과 상시공지 여부(`is_permanent_notice`)를 함께 관리합니다.
- 실제 저장 건수 제한(`max_posts`)은 상세 수집 단계에서 적용됩니다.

## 2) 상시공지 / 일반공지 정책
- 상시공지(`is_permanent_notice=true`):
  - 게시일이 1년을 초과해도 수집합니다.
  - 게시일 파싱이 되지 않아도 수집합니다.
- 일반공지(`is_permanent_notice=false`):
  - 최근 `RECENT_NOTICE_DAYS`(기본 365일) 이내 게시글만 수집합니다.
  - 1년 초과 글 또는 날짜 미확인 글을 만나면,
    같은 페이지의 남은 일반공지 상세 수집은 생략하고 다음 페이지로 이동합니다.

## 3) 최근 1년 필터 세부 동작
- 기준일: 크롤링 실행 시점 `now - RECENT_NOTICE_DAYS`
- `published_at` 파싱 성공:
  - 기준일 이내면 수집
  - 기준일 초과면 일반공지는 스킵
- `published_at` 파싱 실패/누락:
  - 상시공지는 수집
  - 일반공지는 스킵 + 페이지 내 일반공지 조기 종료 트리거

## 4) 증분 수집 및 조기 종료
- 기존 결과(`output/kau_official_posts.json`)의 `original_url`을 캐시로 사용합니다.
- 캐시에 있는 URL은 상세 요청하지 않습니다.
- 목록 페이지에서 신규 URL이 0건이면 해당 게시판의 다음 페이지 순회를 종료합니다.

## 5) 중복 제거 정책
- 1차: canonical `original_url` 기준 중복 제거
- 2차: 제목 정규화 기준 중복 제거
  - 공백 정리
  - 소문자화
- 목적: 교차 홈페이지 재게시 공지 통합 및 저장 데이터 중복 최소화

## 6) 실패 기록 기준
- `request_failed`: HTTP 실패/타임아웃/네트워크 오류
- `parse_error:<Exception>`: 파싱 중 예외
- `required_field_empty`: `title` 또는 `content` 누락
- `robots_disallowed`: robots 정책으로 요청 차단
- `missing_ntt_id`: `college.kau.ac.kr` 상세 URL에서 `nttId` 식별자 누락
- `missing_notice_id`: `eslscat` 상세 URL에서 `id` 식별자 누락

## 7) 운영 시 권장값
- 상시공지 비율이 높은 게시판(예: 학사공지)에서 누락을 줄이려면:
  - `--max-pages`를 먼저 늘리고
  - 필요 시 해당 보드의 `max_posts`도 함께 조정합니다.
- 정책 변경 시에는 `crawler/policies/notice_policy.py`, `crawler/services/board_crawler.py`와 본 문서를 함께 업데이트합니다.
