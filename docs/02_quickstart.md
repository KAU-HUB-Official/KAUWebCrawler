# 실행 가이드

## 요구사항
- Python 3.9+
- 네트워크 접근 가능 환경

## 설치
```bash
pip install requests beautifulsoup4
```

## 기본 실행
```bash
python3 crawler/main.py
```

## 옵션
```bash
python3 crawler/main.py --max-pages 3
python3 crawler/main.py --output output/custom_posts.json
```

옵션 설명:
- `--max-pages`: 게시판별 목록 페이지 수 (기본값: 1)
- `--output`: 결과 JSON 저장 경로

## 실행 결과
- 게시글 결과: `output/kau_official_posts.json`
- 실패 내역: `output/kau_official_failed.json`
- 실행 로그: `output/crawler.log`

## 증분 수집 동작(중복 오버헤드 절감)
- 크롤러는 기존 `output/kau_official_posts.json`을 먼저 읽어 `original_url` 캐시로 사용합니다.
- 이미 수집한 URL은 상세 요청을 생략합니다.
- 목록 페이지에서 신규 URL이 0개면 해당 게시판의 다음 페이지 순회를 조기 종료합니다.

## 빠른 점검
```bash
python3 - <<'PY'
import json
from pathlib import Path
p = Path('output/kau_official_posts.json')
posts = json.loads(p.read_text(encoding='utf-8'))
print('count=', len(posts))
print('first_title=', posts[0]['title'] if posts else None)
PY
```
