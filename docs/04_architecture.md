# 아키텍처

## 디렉터리 역할
- `crawler/main.py`: 실행 인자 처리 + 전체 오케스트레이션(클라이언트/어댑터 초기화, 결과 저장)
- `crawler/config.py`: URL/보드/출력/타임아웃 설정
- `crawler/clients/`: HTTP 요청, User-Agent, robots 정책, 지연 제어
- `crawler/parsers/`: 목록/상세 HTML 파싱, 정규화
- `crawler/services/`: 크롤링 엔진/레지스트리/URL 정규화/기존 데이터 로드/중복 제거
- `crawler/policies/`: 공지 포함 정책(최근 1년, 상시공지 예외, 페이지 스킵)
- `crawler/models/post.py`: 공통 데이터 모델
- `crawler/utils/`: 로깅/JSON 저장 유틸

## 실행 흐름
1. `main.py`에서 clients/adapters 생성 (`services/board_registry.py`)
   - 현재 주요 board_type: `kau_official`, `kau_career`, `kau_college`, `kau_research`, `kau_admission`, `kau_ctl`, `kau_library`, `kau_ftc`, `kau_amtc`, `kau_community_php`, `kau_lms_ubboard`, `kau_asbt`
2. 기존 결과 파일 로드 후 `known_urls` 구성 (`services/post_store.py`)
3. `NOTICE_BOARDS` 순회하며 공통 엔진 `crawl_board()` 실행 (`services/board_crawler.py`)
4. 목록 수집/신규 URL 선별/상세 파싱/실패 reason 기록 수행
5. 정책 판단 적용 (`policies/notice_policy.py`):
   상시공지 예외, 일반공지 1년 필터, 일반공지 페이지 조기 스킵
6. 기존+신규 데이터를 URL/제목 기준 병합·중복 제거 (`services/dedup_service.py`)
7. 결과/실패/로그 저장

## 데이터 중복 제거
- URL 정규화: `services/url_normalizer.py`에서 canonical URL 생성
- 1차: 게시판 내부 상세 URL 중복 제거(`crawl_board` 목록 단계)
- 2차: 기존 보유 + 신규 결과 병합 시 `original_url` 중복 제거
- 3차: `title` 정규화(공백 정리 + 소문자화) 기준 중복 제거

## 요청 정책
- 공통 세션(`requests.Session`) 사용
- `User-Agent` 명시
- `REQUEST_TIMEOUT_SECONDS` 적용
- 요청 간 랜덤 지연(`REQUEST_DELAY_SECONDS`) 적용
- `robots.txt` 확인 후 차단 시 요청 생략
