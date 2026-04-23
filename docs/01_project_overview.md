# 프로젝트 개요

## 목적

한국항공대학교 통합 공지 데이터를 일관된 포맷으로 수집하는 MVP 크롤러입니다.

## 현재 범위

- `kau.ac.kr` 공지 게시판 7종
- `career.kau.ac.kr` 대학일자리센터 공지사항 게시판(`https://career.kau.ac.kr/ko/community/notice`)
- `college.kau.ac.kr` 공지 게시판 9종
  - 국제교류처(`gc63585b`)
  - 인권센터(`gc22052b`)
  - 생활관(`gc65332b`)
  - 항공우주박물관(`gc73673b`)
  - 항공교통관제교육원(`gc80226b`)
  - 항공안전교육원(`gc63977b`)
  - 평생교육원(`gc11101b`)
  - 드림칼리지디자인(`gc24251b`)
  - 항공우주정책대학원(`gc91652b`)
- `research.kau.ac.kr` 산학협력단 공지사항
- `ibhak.kau.ac.kr` 입학처 공지사항
- `ctl.kau.ac.kr` 교수학습센터 공지사항
- `lib.kau.ac.kr` 학술정보관 일반공지
- `ftc.kau.ac.kr` 비행교육원 공지사항
- `amtc.kau.ac.kr` 항공기술교육원 공지사항
- `fsc.kau.ac.kr` 새내기성공센터 공지사항
- `grad.kau.ac.kr` 대학원 공지사항
- `gradbus.kau.ac.kr` 경영대학원 공지사항
- `lms.kau.ac.kr` LMS 공지사항
- `asbt.kau.ac.kr` 첨단분야 부트캠프사업단 공지사항

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
- `career.kau.ac.kr` 공지 보드는 사용자 요청에 따라 robots 예외 정책으로 수집

## 현재 제한

- 일부 게시글은 이미지 본문 위주이며, 텍스트 대신 이미지 ALT/플레이스홀더로 저장
