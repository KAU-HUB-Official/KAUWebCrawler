# 아키텍처

## 디렉터리 역할
- `crawler/main.py`: 게시판 루프, 실행 흐름, 저장/로깅 오케스트레이션
- `crawler/config.py`: URL/보드/출력/타임아웃 설정
- `crawler/clients/`: HTTP 요청, User-Agent, robots 정책, 지연 제어
- `crawler/parsers/`: 목록/상세 HTML 파싱, 정규화
- `crawler/models/post.py`: 공통 데이터 모델
- `crawler/utils/`: 로깅/JSON 저장 유틸

## 실행 흐름
1. `NOTICE_BOARDS` 순회
2. 기존 결과 파일 로드 후 `known_urls` 구성
3. 게시판별 목록 URL 수집
4. 신규 상세 URL만 선별(known URL 스킵)
5. 상세 파싱 후 `Post` 변환
6. 기존+신규 데이터를 `original_url` 기준 병합/중복 제거
7. 결과/실패/로그 저장

## 데이터 중복 제거
- URL 정규화: `page`, `searchkey` 등 비본질 쿼리 제거 후 canonical URL로 비교
- 1차: 게시판 내부 상세 URL 중복 제거
- 2차: 기존 보유 + 신규 결과 병합 시 `original_url` 중복 제거

## 요청 정책
- 공통 세션(`requests.Session`) 사용
- `User-Agent` 명시
- `REQUEST_TIMEOUT_SECONDS` 적용
- 요청 간 랜덤 지연(`REQUEST_DELAY_SECONDS`) 적용
- `robots.txt` 확인 후 차단 시 요청 생략
