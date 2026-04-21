# 운영/장애 대응

## 로그와 산출물
- 실행 로그: `output/crawler.log`
- 성공 데이터: `output/kau_official_posts.json`
- 실패 데이터: `output/kau_official_failed.json`

## 실패 reason 정의
- `request_failed`: HTTP 요청 실패/타임아웃/네트워크 오류
- `parse_error:<Exception>`: 파싱 중 예외 발생
- `required_field_empty`: title/content 필수값 비어 있음
- `robots_disallowed`: robots 정책으로 요청 차단

## 점검 루틴
1. `crawler.log`에서 게시판별 수집 건수 확인
2. `newly_added` 값으로 증분 수집 효과 확인
3. `kau_official_failed.json`의 `reason` 집계 확인
4. 특정 URL 샘플 수동 점검

## 자주 보는 케이스
- `career.kau.ac.kr` 공지: 사용자 요청으로 `kau_career` 보드는 robots 검사 예외 처리됨
- 이미지 중심 본문: 텍스트 대신 이미지 fallback 본문 생성

## 중복 오버헤드 관련 동작
- 기존 결과 파일을 URL 캐시로 사용해 이미 수집된 공지 상세 요청을 생략
- URL은 canonical 형태로 정규화해 `page=1/2` 같은 파라미터 차이 중복을 방지
- URL 중복 제거 후 제목 정규화(공백 정리 + 소문자화) 기준으로 교차 홈페이지 중복 공지를 1건으로 통합
- 목록에서 신규 URL이 0개면 해당 게시판 페이지 순회를 조기 종료

## 운영 팁
- 과도한 트래픽 방지를 위해 `--max-pages`를 점진적으로 확대
- 사이트 구조 변경 시 selector 문서(05번)와 parser 파일을 함께 수정
