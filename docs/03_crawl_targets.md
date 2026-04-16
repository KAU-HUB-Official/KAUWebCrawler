# 크롤링 대상

## 대상 게시판 목록

| key | 게시판명 | board_type | 목록 URL | code | 상태 |
|---|---|---|---|---|---|
| general_notice | 일반공지 | kau_official | https://kau.ac.kr/kaulife/notice.php | s1101 | 수집 가능 |
| academic_notice | 학사공지 | kau_official | https://kau.ac.kr/kaulife/acdnoti.php | s1201 | 수집 가능 |
| scholarship_notice | 장학/대출공지 | kau_official | https://kau.ac.kr/kaulife/scholnoti.php | s1301 | 수집 가능 |
| event_notice | 행사공지 | kau_official | https://kau.ac.kr/kaulife/event.php | s1401 | 수집 가능 |
| bid_notice | 입찰공지 | kau_official | https://kau.ac.kr/kaulife/bid.php | s1601 | 수집 가능 |
| covid_notice | 감염병 관리 공지사항 | kau_official | https://kau.ac.kr/kaulife/covidnoti.php | s1701 | 수집 가능 |
| it_notice | IT공지사항 | kau_official | https://kau.ac.kr/kaulife/itnoti.php | s1801 | 수집 가능 |
| job_notice | 취업공지 | kau_career | https://career.kau.ac.kr/ko/dataroom/data | - | robots 차단 |

## 취업공지 차단 사유
`https://career.kau.ac.kr/robots.txt`
```txt
User-agent: *
Disallow: /
Allow: /$
```

현재 구현은 정책을 존중하므로 `job_notice`는 `robots_disallowed`로 실패 로그에 기록됩니다.
