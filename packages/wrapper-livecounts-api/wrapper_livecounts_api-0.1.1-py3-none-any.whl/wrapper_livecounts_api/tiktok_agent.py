import re
import warnings

from wrapper_livecounts_api import env
from wrapper_livecounts_api.error import TiktokError
from wrapper_livecounts_api.models import TiktokUser, TiktokUserCount, TiktokVideo, TikTokVideoCount
from wrapper_livecounts_api.utils import send_request


class TiktokAgent:

    @staticmethod
    def find_users(query: str, exact: bool = False) -> list[TiktokUser] | TiktokUser:
        """
        Finds TikTok users based on the provided query.

        Args:
            query (str): The search query to find users.
            exact (bool): If True, finds an exact match for the query. Defaults to False.

        Returns:
            list[TiktokUser] | TiktokUser

        Raises:
            TiktokError - if the user is not found.
        """
        return TiktokAgent.__find_exact_user(query) if exact else TiktokAgent.__find_users(query)

    @staticmethod
    def __find_users(query: str) -> list[TiktokUser]:
        data = send_request(f"{env.TIKTOK_USER_SEARCH_API}/{query}")
        return [
            TiktokUser(
                user_id=item.get("userId", ""),
                username=item.get("id", ""),
                display_name=item.get("username", ""),
                verified=item.get("verified", False),
                avatar=item.get("avatar", ""),
            )
            for item in data.get("userData", [])
        ]

    @staticmethod
    def __find_exact_user(query: str) -> TiktokUser:
        users = TiktokAgent.__find_users(query)
        for user in users:
            if user.username == query:
                return user
        raise TiktokError("TikTok user is not found")

    @staticmethod
    def fetch_user_metrics(query: str = None, user_id: str = None) -> TiktokUserCount:
        """
        Fetches user metrics from TikTok API.

        Args:
            query (str): The username of the TikTok user.
            user_id (str): The ID of the TikTok user.

        Returns:
            TiktokUserCount: An object containing user metrics.

        Raises:
            TiktokError: If neither 'query' nor 'tiktok_id' is provided.
        """
        if user_id is not None:
            return TiktokAgent.__fetch_user_metrics_by_tiktok_id(user_id)
        elif query is not None:
            return TiktokAgent.__fetch_user_metrics_by_query(query)
        else:
            raise TiktokError("Must provide either 'query' or 'tiktok_id'")

    @staticmethod
    def __fetch_user_metrics_by_tiktok_id(tiktok_id: str) -> TiktokUserCount:
        data = send_request(f"{env.TIKTOK_USER_STATS_API}/{tiktok_id}")
        return TiktokUserCount(
            user_id=tiktok_id,
            follower_count=data.get("followerCount", 0),
            like_count=data.get("likeCount", 0),
            following_count=data.get("followingCount", 0),
            video_count=data.get("videoCount", 0)
        )

    @staticmethod
    def __fetch_user_metrics_by_query(query) -> TiktokUserCount:
        user = TiktokAgent.find_users(query, True)
        return TiktokAgent.__fetch_user_metrics_by_tiktok_id(user.user_id)

    @staticmethod
    def find_video(query: str = None, video_id: str = None) -> TiktokVideo:
        """
        Finds a TikTok video by its ID or URL.

        Args:
            query (str): The URL of the TikTok video.
            video_id (str): The ID of the TikTok video.

        Returns:
            TiktokVideo: An object containing video information.

        Raises:
            TiktokError: If neither 'query' nor 'video_id' is provided.
        """
        if query is not None:
            video_id = TiktokAgent.__extract_video_id_from_given_url(query)
        if video_id is None:
            raise TiktokError("Must provide either 'query' or 'video_id'")
        return TiktokAgent.__find_video_by_id(video_id)

    @staticmethod
    def __find_video_by_id(video_id: str) -> TiktokVideo:
        video = send_request(url=f"{env.TIKTOK_VIDEO_SEARCH_API}/{video_id}")
        user = video.get("author", {})
        return TiktokVideo(
            video_id=video_id,
            title=video.get("title", ""),
            thumbnail=video.get("cover", ""),
            user=TiktokUser(
                user_id=user.get("userId", ""),
                username=user.get("id", ""),
                display_name=user.get("username", ""),
                avatar=user.get("avatar", "")
            ) if user else None
        )

    @staticmethod
    def __extract_video_id_from_given_url(query) -> str | None:
        try:
            return re.search(r"video/(\d+)", query)[1]
        except Exception as e:
            warnings.warn(f"Failed to extract video ID from Tiktok Video URL: {e}")
            return None

    @staticmethod
    def fetch_video_metrics(query: str = None, video_id: str = None) -> TikTokVideoCount:
        """
        Fetches the metrics of a TikTok video.

        Args:
            query (str, optional): The URL of the TikTok video. Defaults to None.
            video_id (str, optional): The ID of the TikTok video. Defaults to None.

        Returns:
            TikTokVideoCount: An object containing the metrics of the TikTok video.

        Raises:
            TiktokError: If neither 'query' nor 'video_id' is provided.
        """
        if query is not None:
            video_id = TiktokAgent.__extract_video_id_from_given_url(query)
        elif video_id is None:
            raise TiktokError("Must provide either 'query' or 'video_id'")

        data = send_request(f"{env.TIKTOK_VIDEO_STATS_API}/{video_id}")
        return TikTokVideoCount(
            video_id=video_id,
            like_count=data.get("likeCount", 0),
            comment_count=data.get("commentCount", 0),
            share_count=data.get("shareCount", 0),
            view_count=data.get("viewCount", 0)
        )
