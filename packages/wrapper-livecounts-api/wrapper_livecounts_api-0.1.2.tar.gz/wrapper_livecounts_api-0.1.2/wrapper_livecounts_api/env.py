import os

PROXY_ENABLED = os.getenv("PROXY_ENABLED", "off")
PROXY_SERVER = os.getenv("PROXY_SERVER", None)
TIKTOK_USER_SEARCH_API = os.getenv("TIKTOK_USER_SEARCH_API", "https://tiktok.livecounts.io/user/search").removesuffix("/")
TIKTOK_USER_STATS_API = os.getenv("TIKTOK_USER_STATS_API", "https://tiktok.livecounts.io/user/stats").removesuffix("/")
TIKTOK_VIDEO_SEARCH_API = os.getenv("TIKTOK_VIDEO_SEARCH_API", "https://tiktok.livecounts.io/video/data").removesuffix("/")
TIKTOK_VIDEO_STATS_API = os.getenv("TIKTOK_VIDEO_STATS_API", "https://tiktok.livecounts.io/video/stats").removesuffix("/")
