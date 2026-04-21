# 문서 인덱스

이 디렉터리는 KAU Notice Hub 크롤러 문서를 주제별로 분리해 정리한 공간입니다.

## 문서 목록
1. [프로젝트 개요](./01_project_overview.md)
2. [실행 가이드](./02_quickstart.md)
3. [크롤링 대상](./03_crawl_targets.md)
4. [아키텍처](./04_architecture.md)
5. [파싱 규칙과 셀렉터](./05_parsing_and_selectors.md)
6. [운영/장애 대응](./06_operations_and_failure.md)
7. [확장 가이드](./07_extension_guide.md)
8. [크롤링 규칙 상세](./08_crawling_rules.md)

## 권장 읽기 순서
- 처음 온 경우: `01 -> 02 -> 03`
- 구조 이해가 필요한 경우: `04 -> 05`
- 운영/배포 담당: `06`
- 신규 사이트 추가 개발: `07`
- 수집 정책 확인/변경: `08`

## 관련 경로
- 크롤러 엔트리포인트: `crawler/main.py`
- 공통 설정: `crawler/config.py`
- 보드 수집 엔진: `crawler/services/board_crawler.py`
- 보드 타입 레지스트리: `crawler/services/board_registry.py`
- 수집 정책: `crawler/policies/notice_policy.py`
- 결과 산출물: `output/`
