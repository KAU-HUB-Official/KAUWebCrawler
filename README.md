# KAU Notice Hub Crawler

한국항공대학교 주요 공지 게시판을 하나의 포맷으로 수집하는 통합 크롤러입니다.

## 프로젝트 구조

```text
Crawler/
├─ crawler/
│  ├─ clients/      # 사이트별 HTTP 요청/robots 처리
│  ├─ parsers/      # 목록/상세 파싱
│  ├─ policies/     # 최근성/상시공지 정책
│  ├─ services/     # 보드 수집 엔진/레지스트리/중복 제거
│  ├─ models/       # Post 데이터 모델
│  ├─ utils/        # 로깅/JSON 저장
│  ├─ config.py     # 보드 설정 및 공통 상수
│  └─ main.py       # 엔트리포인트
├─ docs/            # 운영/개발 문서
└─ output/          # 실행 산출물(JSON, 로그)
```

## 현재 수집 범위

현재 기본 설정(`NOTICE_BOARDS`) 기준 69개 게시판을 수집합니다.

- `kau.ac.kr` 공식 공지 7종
- `career.kau.ac.kr` 대학일자리센터 공지 1종
- `college.kau.ac.kr` 계열 공지 42종
- `aisw.kau.ac.kr`, `ai.kau.ac.kr`, `sw.kau.ac.kr`, `ave.kau.ac.kr` 카드형 학과/대학 공지 8종
- `research.kau.ac.kr` 산학협력단 공지 1종
- `ibhak.kau.ac.kr` 입학처 공지 1종
- `ctl.kau.ac.kr` 교수학습센터 공지 1종
- `lib.kau.ac.kr` 학술정보관 공지 1종
- `ftc.kau.ac.kr` 비행교육원 공지 1종
- `amtc.kau.ac.kr` 항공기술교육원 공지 1종
- `fsc.kau.ac.kr`, `grad.kau.ac.kr`, `gradbus.kau.ac.kr` 공지 3종
- `lms.kau.ac.kr` LMS 공지 1종 (`id=55398`)
- `asbt.kau.ac.kr` 첨단분야 부트캠프사업단 공지 1종

참고: `kau_eslscat` 구현은 존재하지만 기본 수집 대상(`NOTICE_BOARDS`)에는 포함되어 있지 않습니다.

## 핵심 동작

- 기본 실행은 페이지 상한 없이 순회하며, 최근성 정책으로 보드별 중단 시점을 결정
- 목록 항목은 `url + is_permanent_notice`로 관리
- 기존 결과 파일의 `original_url`을 캐시로 사용해 상세 요청 중복 방지
- 이미 수집된 URL은 상세 요청을 생략하되, 기존 `published_at`으로 중단 여부 판단
- 상시공지는 날짜와 무관하게 수집
- 일반공지는 최근 1년(`RECENT_NOTICE_DAYS = 365`)만 수집
- 일반공지는 상시공지 제외 목록에서 최신순이라는 전제로, 기준일 이전/같은 날짜 또는 게시일 미확인 항목을 만나면 해당 보드 수집 중단
- 저장 전 URL 기준 1차, 제목 정규화 기준 2차 중복 제거

## 증분 수집 최적화

기존 결과 파일을 URL 캐시로 활용해 이미 수집된 상세 페이지 요청을 생략합니다. 실측 기준으로 초기 전체 수집 약 45분에서 이후 증분 수집 약 3분 30초로 단축되어, 소요 시간이 약 92.2% 감소했고 약 12.9배 빠르게 실행됩니다.

- 최종 저장 게시글 수: 2,229건
- 초기 전체 수집: 약 45분(2,700초)
- 증분 수집: 약 3분 30초(210초)
- 개선 효과: 소요 시간 약 92.2% 감소, 처리 시간 약 12.9배 단축

## 빠른 실행

```bash
pip install requests beautifulsoup4
python3 crawler/main.py
```

## 기본 산출물

- 게시글: `output/kau_official_posts.json`
- 실패 내역: `output/kau_official_failed.json`
- 로그: `output/crawler.log`

참고: `--output`으로 결과 파일 경로를 바꾸면, 다음 실행 시 해당 파일이 증분 수집 기준 파일로 사용됩니다.

## 문서 안내

- [문서 인덱스](./docs/README.md)
- [프로젝트 개요](./docs/01_project_overview.md)
- [실행 가이드](./docs/02_quickstart.md)
- [크롤링 대상](./docs/03_crawl_targets.md)
- [아키텍처](./docs/04_architecture.md)
- [파싱 규칙과 셀렉터](./docs/05_parsing_and_selectors.md)
- [운영/장애 대응](./docs/06_operations_and_failure.md)
- [확장 가이드](./docs/07_extension_guide.md)
- [크롤링 규칙 상세](./docs/08_crawling_rules.md)
