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
| job_notice | 취업공지 | 대학일자리센터 | kau_career | https://career.kau.ac.kr/ko/dataroom/data | - | robots 차단 |
| college_gc63585_notice | college.kau.ac.kr 공지(gc63585b) | 국제교류처 | kau_college | http://college.kau.ac.kr/web/pages/gc63585b.do | bbsId=0123 | 수집 가능 |
| research_notice | 산학협력단 공지사항 | 연구협력처 | kau_research | https://research.kau.ac.kr/info/info_011.php | code=s2101 | 수집 가능 |

## 홈페이지 분류
- 공식홈: `kau.ac.kr`
- 대학일자리센터: `career.kau.ac.kr`
- 국제교류처: `college.kau.ac.kr`
- 연구협력처: `research.kau.ac.kr`

## 취업공지 차단 사유
`https://career.kau.ac.kr/robots.txt`
```txt
User-agent: *
Disallow: /
Allow: /$
```

현재 구현은 정책을 존중하므로 `job_notice`는 `robots_disallowed`로 실패 로그에 기록됩니다.
