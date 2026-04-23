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
- 페이지 URL:
  - `http://college.kau.ac.kr/web/pages/gc63585b.do` (국제교류처)
  - `http://college.kau.ac.kr/web/pages/gc22052b.do` (인권센터)
- 실제 목록 데이터: `POST /web/bbs/bbsListApi.gen` (JSON)
- 식별값:
  - 국제교류처: `siteFlag=inter_www`, `bbsId=0123`, `mnuId=gc63585b`
  - 인권센터: `siteFlag=rights_www`, `bbsId=0142`, `mnuId=gc22052b`

### 상세 필드
- 상세 데이터: `POST /web/bbs/bbsViewApi.gen` (JSON)
- 제목: `result.nttSj`
- 작성일: `result.frstRegisterPnttm`
- 본문 HTML: `result.nttCn` (BeautifulSoup 텍스트 정리)
- 첨부: `resultFile[*]` → `/web/bbs/FileDownApi.gen?atchFileId=...&fileSn=...&mnuId=...`
- 카테고리: board name fallback (`college.kau.ac.kr 공지(gc63585b)`)

## 교수학습센터 공지 (`kau_ctl_parser.py`)

### 목록 URL
- 페이지 URL: `https://ctl.kau.ac.kr/notice/list.php?code=s1101`
- 목록 선택자: `table.table_01 td.tit > a[href]`
- 필터: `mode=read` + `seq=` 포함 링크만 수집

### 상세 필드
- 제목: `div.view_header h4`
- 작성일: `div.view_header ul.info li` (`작성날짜 : YYYY-MM-DD HH:MM:SS`)
- 본문: `div.view_conts`
- 첨부: `div.attach a[href], div.view_attatch a[href], li.attatch a[href]`
- 카테고리: `div.location span.here` (없으면 board name fallback)

## 학술정보관 일반공지 (`kau_library_parser.py`)

### 목록 URL
- 페이지 URL: `https://lib.kau.ac.kr/sb/default_notice_list.mir`
- 목록 선택자: `tr[onclick*='go_view(']`
- 링크 규칙: `onclick=\"go_view('4955','default_notice_view');\"`에서 `sb_no` 추출
  - 상세 URL: `/sb/default_notice_view.mir?sb_no=...`

### 상세 필드
- 제목: `div.sc_view_header p.title`
- 작성일: `div.sc_view_header ul li` 내 날짜 텍스트
- 본문: `div.view_content`
- 첨부: `dl.sc_board dd a[onclick*='download_file(']`
  - `download_file('file_no','file_mno')`를
    `/sb/filedownload.mir?file_no=...&file_mno=...&sb_skin=default&sb_code=notice`로 변환
- 카테고리: 상단 제목 selector fallback 후 board name 사용

## 비행교육원 공지 (`kau_ftc_parser.py`)

### 목록 URL
- 페이지 URL: `https://ftc.kau.ac.kr/info/notice_02.php`
- 목록 선택자: `a[href*='mode=read'][href*='seq=']`
- 링크 규칙: `notice_02.php?...&mode=read&seq=...`

### 상세 필드
- 제목: `div.view_header h4`
- 작성일: `div.view_header ul.view_info li` 내 날짜 값 (`YYYY-MM-DD`)
- 본문: `div.view_conts`
- 첨부: `div.attach a[href]` (fallback: `div.view_attatch`, `li.attatch`)
- 카테고리: `view_info` 첫 항목 fallback

## 공통 PHP 공지 (`kau_community_php` + `kau_ftc_parser.py`)

### 대상 사이트
- 새내기성공센터: `http://fsc.kau.ac.kr/info/info_01.php` (`code=s1101`)
- 대학원: `https://grad.kau.ac.kr/community/notice_02.php` (`code=s1201`)
- 경영대학원: `http://gradbus.kau.ac.kr/community/notice_01.php` (`code=s1101`)

### 목록 URL
- 선택자: `a[href*='mode=read'][href*='seq=']`
- 링크 규칙: `...php?...&code=sXXXX&page=...&mode=read&seq=...`

### 상세 필드
- 제목: `div.view_header h4`
- 작성일: `div.view_header ul.view_info li` 내 날짜 패턴
- 본문: `div.view_conts`
- 첨부: `div.attach a[href]`, `div.view_attatch a[href]`, `li.attatch a[href]`
- 카테고리: `view_info` 첫 항목 사용
  - 첫 항목이 `관리자` 계열이면 board name fallback 사용

## 항공기술교육원 공지 (`kau_amtc_parser.py`)

### 목록 URL
- 페이지 URL: `http://amtc.kau.ac.kr/bbs/board.php?bo_table=notice`
- 목록 선택자: `a[href*='bo_table='][href*='wr_id=']`
- 링크 규칙: `board.php?bo_table=notice&wr_id=...`

### 상세 필드
- 제목: `#bo_v_title` (`.bo_v_tit` fallback)
- 작성일: `strong.if_date` (`YY-MM-DD` 또는 `YYYY-MM-DD` → `YYYY-MM-DD` 정규화)
- 본문: `#bo_v_con` (`#bo_v_atc` fallback)
- 첨부: `#bo_v_file a[href]`, `a[href*='download.php']`
- 카테고리: `<title>` 앞부분(예: `일반/학사공지`) fallback

## LMS 공지 (`kau_lms_parser.py`)

### 목록 URL
- 페이지 URL: `https://lms.kau.ac.kr/mod/ubboard/view.php?id=55398`
- 목록 선택자: `div.ubboard_list table.ubboard_table tbody tr`
- 링크 규칙: `a[href*='article.php'][href*='bwid=']`
- 상시공지 판정: `img[alt*='공지']` 또는 공지 마커 셀

### 상세 필드
- 제목: `div.ubboard_view .subject`
- 작성일: `div.ubboard_view .date`, `div.ubboard_view .writer` 텍스트에서 날짜 패턴 추출
- 본문: `div.ubboard_view .content .text_to_html` (`.content` fallback)
- 첨부: `.attach/.file` 링크 + `pluginfile.php`/`download.php` 링크
- 카테고리: breadcrumb 마지막 항목 fallback

## 부트캠프 사업단 공지 (`kau_asbt_parser.py`)

### 목록 URL
- 페이지 URL: `https://asbt.kau.ac.kr/customer/notice.php?ptype=list&code=notice`
- 목록 선택자: `table tbody tr a[href*='ptype=view'][href*='idx=']`
- 링크 규칙: `notice.php?ptype=view&idx=...&code=notice`
- 상시공지 판정: `tr.point` 또는 `.notice/.m_notice` 마커

### 상세 필드
- 제목: `div.bbs_view h3.subject`
- 작성일: `div.bbs_view ul li` 중 `작성일` 항목
- 본문: `div.bbs_view div.view_content`
- 첨부: `div.bbs_view div.view_file a[href]`
- 카테고리: `#subtitle h3` fallback

## 토익 사이버 강좌 공지 (`kau_eslscat_parser.py`)

현재 `eslscat_notice` 보드는 운영 대상에서 제외되어 기본 수집 목록(`NOTICE_BOARDS`)에는 포함되지 않습니다.

### 목록 URL
- 페이지 URL: `https://www.eslscat.com/class/student/help/notice_list.asp`
- 목록 선택자: `a[href*='javascript:goview(']`
- 링크 규칙: `javascript:goview(id)` → `notice_view.asp?id={id}` 형태로 변환

### 상세 필드
- 제목: `table.tt_list thead th`
- 작성일: `table.tt_list tbody tr` 중 `작성일` 행
- 본문: `table.tt_list tbody tr:last-child td[colspan]`
- 첨부: `첨부파일` 행의 `a[href]`
- 카테고리: `li.sub_title` fallback

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
- `ctl.kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 유지합니다.
- `lib.kau.ac.kr` 상세 URL은 `sb_no`만 유지합니다.
- `ftc.kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 유지합니다.
- `fsc.kau.ac.kr`, `grad.kau.ac.kr`, `gradbus.kau.ac.kr` 상세 URL은 `code`, `mode`, `seq`만 유지합니다.
- `lms.kau.ac.kr` 상세 URL은 `id`, `bwid`만 유지합니다.
- `asbt.kau.ac.kr` 상세 URL은 `ptype=view`, `idx`, `code`만 유지합니다.
- `www.eslscat.com` 상세 URL은 `id`만 유지합니다.
- `amtc.kau.ac.kr` 상세 URL은 `bo_table`, `wr_id`만 유지합니다.
