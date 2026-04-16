# 파싱 규칙과 셀렉터

## KAU 공식 공지 (`kau_official_parser.py`)

### 목록 URL
- 기본: `table.table_board tbody td.title > a[href]`
- 필터: `mode=read` + `seq=` 포함 링크만 수집

### 상세 필드
- 제목: `div.view_header h4`
- 작성일: `div.view_header li.date`
- 본문: `div.view_conts`
- 첨부: `div.view_header li.attatch a[href]`
- 카테고리: `div.location_wrap ul.location li` 마지막 항목

### 이미지 본문 fallback
텍스트 본문이 비어 있으면:
1. `img alt`를 `[이미지] ...` 라인으로 합성
2. `alt`도 없으면 `[이미지 본문] 텍스트 본문 없음 (이미지 N개)` 저장

## 취업공지 (`kau_career_parser.py`)

### 목록 URL
- 기본: `ul[data-role='table'] li.tbody span.title > a[href]`
- 필터: `/view/` 포함 링크

### 상세 필드
- 제목: `article[data-role='post'] .header h5`
- 작성일: `article[data-role='post'] .header li.date time`
- 본문: `#ModuleBoardunivBodyPrintBox [data-role='wysiwyg-content']`
- 첨부: `[data-module='attachment'] a.file` (`data-download` 우선)
- 카테고리: `div.nbreadcrumb span` 마지막 값

## 상대경로 처리
모든 링크는 `urljoin()`으로 절대경로 변환합니다.

## URL 정규화(중복 방지)
- `kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 남기고 `page/searchkey/searchvalue`는 제거합니다.
- `career.kau.ac.kr` 상세 URL은 `/view/{id}` 경로만 유지하고 `?p=`는 제거합니다.
