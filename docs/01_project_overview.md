# 프로젝트 개요

## 목적
한국항공대학교 통합 공지 데이터를 일관된 포맷으로 수집하는 MVP 크롤러입니다.

## 현재 범위
- `kau.ac.kr` 공지 게시판 7종
- `career.kau.ac.kr` 취업공지 게시판(정책상 차단 상태)

## 수집 데이터 포맷
`Post` 모델 기준:
- `source_name`
- `source_type`
- `category_raw`
- `title`
- `content`
- `published_at`
- `original_url`
- `attachments`
- `crawled_at`

## 핵심 정책
- `requests + BeautifulSoup` 기반
- 상대경로 URL 절대경로 변환
- `original_url` 기준 중복 제거
- 요청 실패/파싱 실패를 JSON + 로그로 저장
- `robots.txt` 존중

## 현재 제한
- 취업공지(`career.kau.ac.kr`)는 `robots.txt`에서 `Disallow: /`라 자동 수집 불가
- 일부 게시글은 이미지 본문 위주이며, 텍스트 대신 이미지 ALT/플레이스홀더로 저장
