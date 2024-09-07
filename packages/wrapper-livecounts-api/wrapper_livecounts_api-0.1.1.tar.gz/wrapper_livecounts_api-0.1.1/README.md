# 🎶 Wrapper Livecounts.io API

**Wrapper API for live counts of users and videos on TikTok, YouTube, Twitter, Twitch, KickLive, Vlive, and Odysee Live via Livecounts.io.**

## 📝 Supported API

- **YouTube**: User/Video Count
- **TikTok**: User/Video Count
- **Twitter**: User Count
- **Twitch**: To be supported
- **Vlive**: To be supported
- **Kicklive**: To be supported
- **Odysee-live**: To be supported

## 🕵️ Usage

```shell
pip install wrapper_livecounts_api
```

### Tiktok Live Count API

- **User API**

```python
from wrapper_livecounts_api.tiktok_agent import TiktokAgent

# Find users by username or full name
users = TiktokAgent.find_users("best")

# Find exact user by username
user = TiktokAgent.find_users("best", True)

# Live count user by username
user_metrics = TiktokAgent.fetch_user_metrics(query="best")

# Live count user by user id
user_metrics = TiktokAgent.fetch_user_metrics(user_id="123456789")
```

- **Video API**

```python
from wrapper_livecounts_api.tiktok_agent import TiktokAgent

# Find video by given URL
video = TiktokAgent.find_video(query="https://tiktok.com/@test/video/122222223233232?test1=value1")

# Find video by video_id
video = TiktokAgent.find_video(video_id="122222223233232")

# Live count video by video url
video_metrics = TiktokAgent.fetch_video_metrics(query="https://tiktok.com/@test/video/122222223233232?test1=value1")

# Live count video by video id
video_metrics = TiktokAgent.fetch_video_metrics(video_id="122222223233232")
```

### YouTube API

[Placeholder]

### Twitter API

[Placeholder]

## 📛 Disclaimer

This project aimed to security research, testing purpose. Any misuse of this tool for malicious purposes is not condoned.
The developers of this API are not responsible for any illegal or unethical activities carried out using this API.
