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
- 페이지 URL: `https://career.kau.ac.kr/ko/community/notice`
- 기본: `ul[data-role='table'] li.tbody span.title > a[href]`
- 필터: `/ko/community/notice/view/` 포함 링크

### 상세 필드
- 제목: `article[data-role='post'] .header h5`
- 작성일: `article[data-role='post'] .header li.date time`
- 본문: `#ModuleBoardunivBodyPrintBox [data-role='wysiwyg-content']`
- 첨부: `[data-module='attachment'] a[href]` (`data-download` 우선)
- 카테고리: `div.nbreadcrumb span` 마지막 값

## college.kau.ac.kr 공지 (`kau_college_parser.py`)

### 목록 URL
- 페이지 URL: `http://college.kau.ac.kr/web/pages/gc63585b.do`
- 실제 목록 데이터: `POST /web/bbs/bbsListApi.gen` (JSON)
- 식별값: `siteFlag=inter_www`, `bbsId=0123`, `pageIndex`, `bbsAuth=30`

### 상세 필드
- 상세 데이터: `POST /web/bbs/bbsViewApi.gen` (JSON)
- 제목: `result.nttSj`
- 작성일: `result.frstRegisterPnttm`
- 본문 HTML: `result.nttCn` (BeautifulSoup 텍스트 정리)
- 첨부: `resultFile[*]` → `/web/bbs/FileDownApi.gen?atchFileId=...&fileSn=...&mnuId=...`
- 카테고리: board name fallback (`college.kau.ac.kr 공지(gc63585b)`)

## 산학협력단 공지 (`kau_research_parser.py`)

### 목록 URL
- 페이지 URL: `https://research.kau.ac.kr/info/info_011.php`
- 목록 선택자: `table.table_01 td.tit > a[href]`
- 필터: `mode=read` + `seq=` 포함 링크만 수집

### 상세 필드
- 제목: `div.view_header h4`
- 작성일: `div.view_header .view_info .date`
- 본문: `div.view_conts`
- 첨부: `div.view_attatch a[href]`
- 카테고리: `div.article_tit h3` (`공지사항`) fallback

## 입학처 공지 (`kau_admission_parser.py`)

### 목록 URL
- 페이지 URL: `https://ibhak.kau.ac.kr/admission/html/guide/notice.asp`
- 목록 선택자: `section.board_list .bl table tbody td.tit a[onclick]`
- 링크 규칙: `onclick="viewBoardProcess('6119')"`에서 `p_board_idx`를 추출해
  `noticeView.asp?p_board_id=...&p_board_idx=...` 상세 URL 생성

### 상세 필드
- 제목: `section.board_read h2.br_tit`
- 작성일: `section.board_read ul.br_info li` (`bri_tit=작성일`, `bri_desc=YYYY.MM.DD`)
- 본문: `section.board_read div.br_con .editor`
- 첨부: `section.board_read div.br_file a[href]`
- 카테고리: `section.board_read h3.br_cart` (`공통`, `정시`, `재외국민` 등)

## 상대경로 처리
모든 링크는 `urljoin()`으로 절대경로 변환합니다.

## URL 정규화(중복 방지)
- `kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 남기고 `page/searchkey/searchvalue`는 제거합니다.
- `career.kau.ac.kr` 상세 URL은 `/ko/community/notice/view/{id}` 경로만 유지하고 `?p=`는 제거합니다.
- `college.kau.ac.kr` 상세 URL은 `bbsId`, `nttId`, `mnuId`만 유지합니다.
- `research.kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 유지합니다.
- `ibhak.kau.ac.kr` 상세 URL은 `p_board_id`, `p_board_idx`만 유지합니다.
