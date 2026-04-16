from pathlib import Path

BASE_URL = "https://kau.ac.kr"
START_URL = "https://kau.ac.kr/index/main.php"
NOTICE_LIST_URL = "https://kau.ac.kr/kaulife/notice.php"
CAREER_BASE_URL = "https://career.kau.ac.kr"
CAREER_NOTICE_LIST_URL = "https://career.kau.ac.kr/ko/community/notice"
COLLEGE_BASE_URL = "http://college.kau.ac.kr"
COLLEGE_NOTICE_LIST_URL = "http://college.kau.ac.kr/web/pages/gc63585b.do"
RESEARCH_BASE_URL = "https://research.kau.ac.kr"
RESEARCH_NOTICE_LIST_URL = "https://research.kau.ac.kr/info/info_011.php"
ADMISSION_BASE_URL = "https://ibhak.kau.ac.kr"
ADMISSION_NOTICE_LIST_URL = "https://ibhak.kau.ac.kr/admission/html/guide/notice.asp"

SOURCE_NAME = "한국항공대학교 공식 홈페이지"
SOURCE_TYPE = "university_official_notice"
CAREER_SOURCE_NAME = "한국항공대학교 대학일자리플러스센터"
CAREER_SOURCE_TYPE = "university_career_notice"
COLLEGE_SOURCE_NAME = "한국항공대학교 college.kau.ac.kr 공지"
COLLEGE_SOURCE_TYPE = "university_college_notice"
RESEARCH_SOURCE_NAME = "한국항공대학교 산학협력단"
RESEARCH_SOURCE_TYPE = "university_research_notice"
ADMISSION_SOURCE_NAME = "한국항공대학교 입학처"
ADMISSION_SOURCE_TYPE = "university_admission_notice"

USER_AGENT = (
    "Mozilla/5.0 (compatible; KAU-Notice-Crawler/1.0; +https://kau.ac.kr)"
)
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_DELAY_SECONDS = (0.5, 1.2)
VERIFY_SSL = True

DEFAULT_MAX_PAGES = 1
DEFAULT_POSTS_PER_BOARD = 20

NOTICE_BOARDS = [
    {
        "key": "general_notice",
        "name": "일반공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/notice.php",
        "code": "s1101",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "academic_notice",
        "name": "학사공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/acdnoti.php",
        "code": "s1201",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "scholarship_notice",
        "name": "장학/대출공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/scholnoti.php",
        "code": "s1301",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "event_notice",
        "name": "행사공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/event.php",
        "code": "s1401",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "bid_notice",
        "name": "입찰공지",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/bid.php",
        "code": "s1601",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "covid_notice",
        "name": "감염병 관리 공지사항",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/covidnoti.php",
        "code": "s1701",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "it_notice",
        "name": "IT공지사항",
        "board_type": "kau_official",
        "list_url": "https://kau.ac.kr/kaulife/itnoti.php",
        "code": "s1801",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": SOURCE_NAME,
        "source_type": SOURCE_TYPE,
    },
    {
        "key": "job_notice",
        "name": "대학일자리센터 공지사항",
        "board_type": "kau_career",
        "list_url": CAREER_NOTICE_LIST_URL,
        "min_pages": 2,
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": CAREER_SOURCE_NAME,
        "source_type": CAREER_SOURCE_TYPE,
    },
    {
        "key": "college_gc63585_notice",
        "name": "college.kau.ac.kr 공지(gc63585b)",
        "board_type": "kau_college",
        "list_url": COLLEGE_NOTICE_LIST_URL,
        "site_flag": "inter_www",
        "bbs_id": "0123",
        "mnu_id": "gc63585b",
        "bbs_auth": "30",
        "page_unit": DEFAULT_POSTS_PER_BOARD,
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": COLLEGE_SOURCE_NAME,
        "source_type": COLLEGE_SOURCE_TYPE,
    },
    {
        "key": "research_notice",
        "name": "산학협력단 공지사항",
        "board_type": "kau_research",
        "list_url": RESEARCH_NOTICE_LIST_URL,
        "code": "s2101",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": RESEARCH_SOURCE_NAME,
        "source_type": RESEARCH_SOURCE_TYPE,
    },
    {
        "key": "admission_notice",
        "name": "입학처 공지사항",
        "board_type": "kau_admission",
        "list_url": ADMISSION_NOTICE_LIST_URL,
        "board_id": "BBS0004",
        "site_type": "MAM0001",
        "max_posts": DEFAULT_POSTS_PER_BOARD,
        "source_name": ADMISSION_SOURCE_NAME,
        "source_type": ADMISSION_SOURCE_TYPE,
    },
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "kau_official_posts.json"
FAILED_OUTPUT_FILE = OUTPUT_DIR / "kau_official_failed.json"
LOG_FILE = OUTPUT_DIR / "crawler.log"
