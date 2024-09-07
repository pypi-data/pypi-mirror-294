class User:
    def __init__(self, user_id: str, username: str, avatar: str):
        self.user_id = user_id
        self.username = username
        self.avatar = avatar

    def __eq__(self, other):
        return self.user_id == other.user_id if isinstance(other, User) else False

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "avatar": self.avatar
        }


class YoutubeUser(User):
    def __init__(self, user_id: str, username: str, avatar: str):
        super().__init__(user_id, username, avatar)

    def __eq__(self, other):
        return super().__eq__(other) if isinstance(other, YoutubeUser) else False

    def __hash__(self):
        return super().__hash__()

    def __dir__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "avatar": self.avatar
        }


class TiktokUser(User):
    def __init__(self, user_id: str, username: str, display_name: str, avatar: str, verified: bool = None):
        super().__init__(user_id, username, avatar)
        self.display_name = display_name
        self.verified = verified

    def __eq__(self, other):
        return super().__eq__(other) if isinstance(other, TiktokUser) else False

    def __hash__(self):
        return super().__hash__()

    def __dir__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "display_name": self.display_name,
            "avatar": self.avatar,
            "verified": self.verified
        }


class TwitterUser(User):
    def __init__(self, user_id: str, username: str, avatar: str, verified: bool = None):
        super().__init__(user_id, username, avatar)
        self.verified = verified

    def __eq__(self, other):
        return super().__eq__(other) if isinstance(other, TwitterUser) else False

    def __hash__(self):
        return super().__hash__()

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "avatar": self.avatar,
            "verified": self.verified
        }


class YoutubeUserCount:
    def __init__(self, user_id: str, follower_count: int, channel_count: list[int]):
        self.user_id = user_id
        self.follower_count = follower_count
        self.channel_count = channel_count

    def __eq__(self, other):
        if not isinstance(other, YoutubeUserCount):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "channel_count": self.channel_count
        }


class TwitterUserCount(YoutubeUserCount):
    def __init__(self, user_id: str, follower_count: int, channel_count: list[int]):
        super().__init__(user_id, follower_count, channel_count)

    def __eq__(self, other):
        return super.__eq__(other) if isinstance(other, TwitterUserCount) else False

    def __hash__(self):
        return super().__hash__()

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "channel_count": self.channel_count
        }


class TiktokUserCount:
    def __init__(self, user_id: str, follower_count: int, like_count: int, following_count: int, video_count: int):
        self.user_id = user_id
        self.follower_count = follower_count
        self.like_count = like_count
        self.following_count = following_count
        self.video_count = video_count

    def __eq__(self, other):
        if not isinstance(other, TiktokUserCount):
            return False
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "follower_count": self.follower_count,
            "like_count": self.like_count,
            "following_count": self.following_count,
            "video_count": self.video_count
        }


class YoutubeVideo:
    def __init__(self, video_id: str, title: str, thumbnail: str):
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail

    def __eq__(self, other):
        if not isinstance(other, YoutubeVideo):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail
        }


class TiktokVideo:
    def __init__(self, video_id: str, title: str, thumbnail: str, user: TiktokUser):
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail
        self.user = user

    def __eq__(self, other):
        if not isinstance(other, TiktokVideo):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "title": self.title,
            "thumbnail": self.thumbnail,
            "user": self.user
        }


class YoutubeVideoCount:
    def __init__(self, video_id: str, likes: int, dis_likes: int, raw_likes: int, raw_dislikes: int, view_count: int, is_delete: bool = None):
        self.video_id = video_id
        self.likes = likes
        self.dis_likes = dis_likes
        self.raw_likes = raw_likes
        self.raw_dislikes = raw_dislikes
        self.view_count = view_count
        self.is_delete = is_delete

    def __eq__(self, other):
        if not isinstance(other, YoutubeVideoCount):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "likes": self.likes,
            "dis_likes": self.dis_likes,
            "raw_likes": self.raw_likes,
            "raw_dislikes": self.raw_dislikes,
            "view_count": self.view_count,
            "is_delete": self.is_delete
        }


class TikTokVideoCount:
    def __init__(self, video_id: str, view_count: int, like_count: int, comment_count: int, share_count: int):
        self.video_id = video_id
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.share_count = share_count

    def __eq__(self, other):
        if not isinstance(other, TikTokVideoCount):
            return False
        return self.video_id == other.video_id

    def __hash__(self):
        return hash(self.video_id)

    def __dict__(self):
        return {
            "video_id": self.video_id,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "share_count": self.share_count
        }
