from pathlib import Path

BASE_URL = "https://kau.ac.kr"
START_URL = "https://kau.ac.kr/index/main.php"
NOTICE_LIST_URL = "https://kau.ac.kr/kaulife/notice.php"
CAREER_BASE_URL = "https://career.kau.ac.kr"
CAREER_NOTICE_LIST_URL = "https://career.kau.ac.kr/ko/dataroom/data"

SOURCE_NAME = "한국항공대학교 공식 홈페이지"
SOURCE_TYPE = "university_official_notice"
CAREER_SOURCE_NAME = "한국항공대학교 대학일자리플러스센터"
CAREER_SOURCE_TYPE = "university_career_notice"

USER_AGENT = (
    "Mozilla/5.0 (compatible; KAU-Notice-Crawler/1.0; +https://kau.ac.kr)"
)
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_DELAY_SECONDS = (0.5, 1.2)
VERIFY_SSL = True

DEFAULT_MAX_PAGES = 1

NOTICE_BOARDS = [
    {
        "key": "general_notice",
        "name": "일반공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/notice.php",
        "code": "s1101",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "academic_notice",
        "name": "학사공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/acdnoti.php",
        "code": "s1201",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "scholarship_notice",
        "name": "장학/대출공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/scholnoti.php",
        "code": "s1301",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "event_notice",
        "name": "행사공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/event.php",
        "code": "s1401",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "bid_notice",
        "name": "입찰공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/bid.php",
        "code": "s1601",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "covid_notice",
        "name": "감염병 관리 공지사항",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/covidnoti.php",
        "code": "s1701",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "it_notice",
        "name": "IT공지사항",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/itnoti.php",
        "code": "s1801",
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "job_notice",
        "name": "취업공지",
        "board_type": "kau_career",
        "list_url": CAREER_NOTICE_LIST_URL,
        "source_name": CAREER_SOURCE_NAME,
        "source_type": CAREER_SOURCE_TYPE,
    },
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "kau_official_posts.json"
FAILED_OUTPUT_FILE = OUTPUT_DIR / "kau_official_failed.json"
LOG_FILE = OUTPUT_DIR / "crawler.log"
