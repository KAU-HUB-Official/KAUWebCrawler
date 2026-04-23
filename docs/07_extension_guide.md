# 확장 가이드

## 1) 같은 구조 게시판 추가 (권장)
대상: `kau.ac.kr/kaulife/*.php` 유형

작업:
1. `crawler/config.py`의 `NOTICE_BOARDS`에 항목 추가
2. `board_type='kau_official'`, `list_url`, `code` 설정
3. 실행 후 결과/실패 로그 확인

## 2) 다른 사이트 추가
작업:
1. `clients/`에 신규 `XXXClient` 생성
2. `parsers/`에 신규 `XXXParser` 생성
3. `services/board_registry.py`에 `board_type -> BoardAdapter` 매핑 추가
4. `NOTICE_BOARDS`에 신규 board 설정 추가

## 2-0) 현재 재사용 가능한 board_type 예시
- `kau_college`: college API(JSON) 기반 게시판
- `kau_community_php`: `mode=read&seq` 공통 PHP 게시판(fsc/grad/gradbus)
- `kau_lms_ubboard`: LMS `view.php`/`article.php` 게시판
- `kau_asbt`: `ptype=list/view&idx=` 형태 게시판
- `kau_eslscat`: `javascript:goview(id)` + POST 상세 게시판

## 2-1) BoardAdapter 작성 기준
- 목록 URL 생성: `build_list_page_url(board, page)`
- 목록 요청: `fetch_list_html(board, page)`
- 상세 요청: `fetch_detail(board, detail_url)` (`DetailFetchResult` 반환)
- parser 생성: `parser_factory(board)`
- 필요 시 robots 검사 플래그/`min_pages_field` 설정

## 3) 신규 parser 체크리스트
- 목록 selector가 최신 구조와 일치하는가
- 상세 title/content/published_at가 안정적으로 추출되는가
- 첨부파일 링크가 절대경로로 변환되는가
- 본문이 이미지-only일 때 fallback 정책이 필요한가
- 실패 reason이 운영 관점에서 충분히 구분되는가

## 4) 변경 시 권장 검증
```bash
python3 crawler/main.py --max-pages 1
python3 - <<'PY'
import json
from pathlib import Path
p = json.loads(Path('output/kau_official_posts.json').read_text(encoding='utf-8'))
f = json.loads(Path('output/kau_official_failed.json').read_text(encoding='utf-8'))
print('posts=', len(p), 'failed=', len(f))
PY
```
