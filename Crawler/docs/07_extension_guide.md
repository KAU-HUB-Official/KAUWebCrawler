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
3. `main.py`에 `board_type` 분기 추가
4. `NOTICE_BOARDS`에 신규 board 설정 추가

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
