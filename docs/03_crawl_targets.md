# 크롤링 대상

## 대상 게시판 목록

| key | 게시판명 | 홈페이지 분류 | board_type | 목록 URL | code | 상태 |
|---|---|---|---|---|---|---|
| general_notice | 일반공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/notice.php | s1101 | 수집 가능 |
| academic_notice | 학사공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/acdnoti.php | s1201 | 수집 가능 |
| scholarship_notice | 장학/대출공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/scholnoti.php | s1301 | 수집 가능 |
| event_notice | 행사공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/event.php | s1401 | 수집 가능 |
| bid_notice | 입찰공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/bid.php | s1601 | 수집 가능 |
| covid_notice | 감염병 관리 공지사항 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/covidnoti.php | s1701 | 수집 가능 |
| it_notice | IT공지사항 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/itnoti.php | s1801 | 수집 가능 |
| job_notice | 대학일자리센터 공지사항 | 대학일자리센터 | kau_career | https://career.kau.ac.kr/ko/community/notice | - | 수집 가능 |
| college_gc63585_notice | college.kau.ac.kr 공지(gc63585b) | 국제교류처 | kau_college | http://college.kau.ac.kr/web/pages/gc63585b.do | bbsId=0123 | 수집 가능 |
| human_rights_notice | 인권센터 공지사항 | 인권센터 | kau_college | http://college.kau.ac.kr/web/pages/gc22052b.do | bbsId=0142 | 수집 가능 |
| research_notice | 산학협력단 공지사항 | 연구협력처 | kau_research | https://research.kau.ac.kr/info/info_011.php | code=s2101 | 수집 가능 |
| admission_notice | 입학처 공지사항 | 입학처 | kau_admission | https://ibhak.kau.ac.kr/admission/html/guide/notice.asp | p_board_id=BBS0004 | 수집 가능 |
| ctl_notice | 교수학습센터 공지사항 | 교수학습센터 | kau_ctl | https://ctl.kau.ac.kr/notice/list.php?code=s1101 | code=s1101 | 수집 가능 |
| library_notice | 학술정보관 일반공지 | 학술정보관 | kau_library | https://lib.kau.ac.kr/sb/default_notice_list.mir | sb_no 기반 | 수집 가능 |

## 홈페이지 분류
- 공식홈: `kau.ac.kr`
- 대학일자리센터: `career.kau.ac.kr`
- 국제교류처: `college.kau.ac.kr`
- 인권센터: `college.kau.ac.kr`
- 연구협력처: `research.kau.ac.kr`
- 입학처: `ibhak.kau.ac.kr`
- 교수학습센터: `ctl.kau.ac.kr`
- 학술정보관: `lib.kau.ac.kr`

## 대학일자리센터 정책 처리
`career.kau.ac.kr`는 robots 정책이 전면 차단으로 설정되어 있어,
현재 구현은 사용자 요청에 따라 `kau_career` 보드에 한해 robots 검사를 예외 처리합니다.
또한 1페이지 고유 URL이 20건 미만인 경우를 보완하기 위해 `job_notice`는 최소 2페이지를 조회합니다.
