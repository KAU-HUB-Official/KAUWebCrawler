# 크롤링 대상

## 대상 게시판 목록 (`NOTICE_BOARDS`)

| key | 게시판명 | 홈페이지 분류 | board_type | 목록 URL | 식별값 |
| --- | --- | --- | --- | --- | --- |
| general_notice | 일반공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/notice.php | `code=s1101` |
| academic_notice | 학사공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/acdnoti.php | `code=s1201` |
| scholarship_notice | 장학/대출공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/scholnoti.php | `code=s1301` |
| event_notice | 행사공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/event.php | `code=s1401` |
| bid_notice | 입찰공지 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/bid.php | `code=s1601` |
| covid_notice | 감염병 관리 공지사항 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/covidnoti.php | `code=s1701` |
| it_notice | IT공지사항 | 공식홈 | kau_official | https://kau.ac.kr/kaulife/itnoti.php | `code=s1801` |
| job_notice | 대학일자리센터 공지사항 | 대학일자리센터 | kau_career | https://career.kau.ac.kr/ko/community/notice | `min_pages=2` |
| college_gc63585_notice | 국제교류처 공지(gc63585b) | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc63585b.do | `site_flag=inter_www`, `bbs_id=0123`, `mnu_id=gc63585b` |
| college_gc24251_notice | 드림칼리지디자인 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc24251b.do | `site_flag=mat_WWW`, `bbs_id=0414`, `mnu_id=gc24251b` |
| human_rights_notice | 인권센터 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc22052b.do | `site_flag=rights_www`, `bbs_id=0142`, `mnu_id=gc22052b` |
| dorm_notice | 생활관 일반공지 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc65332b.do | `site_flag=dorm_www`, `bbs_id=0230`, `mnu_id=gc65332b` |
| museum_notice | 항공우주박물관 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc73673b.do | `site_flag=museum`, `bbs_id=0276`, `mnu_id=gc73673b` |
| atci_notice | 항공교통관제교육원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc80226b.do | `site_flag=atci`, `bbs_id=0226`, `mnu_id=gc80226b` |
| college_gc91652_notice | 항공우주정책대학원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc91652b.do | `site_flag=lawpolicy_www`, `bbs_id=0349`, `mnu_id=gc91652b` |
| materials_grad_notice | 신소재공학과 대학원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc74927b.do | `site_flag=materials_www`, `bbs_id=0097`, `mnu_id=gc74927b` |
| eie_grad_notice | 항공전자정보공학부 대학원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc23761b.do | `site_flag=eie_www`, `bbs_id=0015`, `mnu_id=gc23761b` |
| kasi_notice | 항공안전교육원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc63977b.do | `site_flag=kasi_www`, `bbs_id=0136`, `mnu_id=gc63977b` |
| life_notice | 평생교육원 공지사항 | college 계열 | kau_college | http://college.kau.ac.kr/web/pages/gc11101b.do | `site_flag=life_www`, `bbs_id=0120`, `mnu_id=gc11101b` |
| research_notice | 산학협력단 공지사항 | 산학협력단 | kau_research | https://research.kau.ac.kr/info/info_011.php | `code=s2101` |
| admission_notice | 입학처 공지사항 | 입학처 | kau_admission | https://ibhak.kau.ac.kr/admission/html/guide/notice.asp | `board_id=BBS0004`, `site_type=MAM0001` |
| ctl_notice | 교수학습센터 공지사항 | 교수학습센터 | kau_ctl | https://ctl.kau.ac.kr/notice/list.php | `code=s1101` |
| library_notice | 학술정보관 일반공지 | 학술정보관 | kau_library | https://lib.kau.ac.kr/sb/default_notice_list.mir | `sb_no` 기반 |
| ftc_notice | 비행교육원 공지사항 | 비행교육원 | kau_ftc | https://ftc.kau.ac.kr/info/notice_02.php | `code=s1102` |
| fsc_notice | 새내기성공센터 공지사항 | 새내기성공센터 | kau_community_php | http://fsc.kau.ac.kr/info/info_01.php | `base_url=fsc.kau.ac.kr`, `code=s1101` |
| grad_notice | 대학원 공지사항 | 대학원 | kau_community_php | https://grad.kau.ac.kr/community/notice_02.php | `base_url=grad.kau.ac.kr`, `code=s1201` |
| gradbus_notice | 경영대학원 공지사항 | 경영대학원 | kau_community_php | http://gradbus.kau.ac.kr/community/notice_01.php | `base_url=gradbus.kau.ac.kr`, `code=s1101` |
| amtc_notice | 항공기술교육원 공지사항 | 항공기술교육원 | kau_amtc | http://amtc.kau.ac.kr/bbs/board.php | `bo_table=notice` |
| lms_notice | LMS 공지사항 | LMS | kau_lms_ubboard | https://lms.kau.ac.kr/mod/ubboard/view.php?id=55398 | `id=55398` |
| asbt_notice | 첨단분야 부트캠프사업단 공지사항 | 부트캠프 사업단 | kau_asbt | https://asbt.kau.ac.kr/customer/notice.php | `code=notice` |

## 도메인 그룹

- 공식홈: `kau.ac.kr`
- 대학일자리센터: `career.kau.ac.kr`
- college 계열: `college.kau.ac.kr`
- 산학협력단: `research.kau.ac.kr`
- 입학처: `ibhak.kau.ac.kr`
- 교수학습센터: `ctl.kau.ac.kr`
- 학술정보관: `lib.kau.ac.kr`
- 비행교육원: `ftc.kau.ac.kr`
- 항공기술교육원: `amtc.kau.ac.kr`
- 공통 PHP 계열: `fsc.kau.ac.kr`, `grad.kau.ac.kr`, `gradbus.kau.ac.kr`
- LMS: `lms.kau.ac.kr`
- 부트캠프사업단: `asbt.kau.ac.kr`

참고: 박물관/항공안전교육원/평생교육원은 원 사이트에서 `college.kau.ac.kr` 공지 페이지를 연결해 사용하므로, 크롤러도 `college` 페이지 URL을 직접 수집 대상으로 사용합니다.

## robots 정책 처리

- 기본 정책: 사이트별 `robots.txt` 준수
- 예외 정책: `kau_career`는 사용자 요청으로 robots 검사 비활성화(`respect_robots=False`)
- `job_notice`는 1페이지 고유 URL이 적은 경우를 보완하기 위해 `min_pages=2`를 적용

## 비활성 구현

- `kau_eslscat` 클라이언트/파서는 구현되어 있으나, 현재 `NOTICE_BOARDS`에는 포함되지 않아 기본 실행 시 수집하지 않습니다.
