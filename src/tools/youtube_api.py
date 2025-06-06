from typing import Annotated, List, Dict
from .helper.helpers import (
    _resolve_channel_id,
    _fetch_video_statistics,
    _fetch_video_details,
    _search_youtube_channel_videos,
    _fetch_channel_info,
    _fetch_videos,
    _fetch_comments,
    _introspect_channel,
    _search_youtube_channels,
    _search_and_introspect_channel,
)
from llama_index.core.tools import FunctionTool


def fetch_video_details(video_id: str) -> Dict:
    """
    Fetch detailed information about a specific video.

    Args:
        video_id (str): The YouTube video ID

    Returns:
        Dict: Video information including:
            - id: Video ID
            - title: Video title
            - description: Video description
            - publishedAt: Publication date
            - viewCount: Number of views
            - likeCount: Number of likes
            - commentCount: Number of comments
            - duration: Video duration
            - thumbnails: Video thumbnails
    """
    return _fetch_video_details(video_id)


def search_youtube_channel_videos(
    channel_id: str,
    search_term: str,
    max_results: int = 10,
) -> List[Dict]:
    """
    Search for videos within a specific channel that match the search term.

    Args:
        channel_id (str): The YouTube channel ID
        search_term (str): The term to search for in video titles and descriptions
        max_results (int): Maximum number of videos to return (default: 10)

    Returns:
        List[Dict]: List of video information including:
            - id: Video ID
            - title: Video title
            - description: Video description
            - publishedAt: Publication date
            - viewCount: Number of views
            - likeCount: Number of likes
            - commentCount: Number of comments
            - duration: Video duration
            - thumbnails: Video thumbnails
    """
    return _search_youtube_channel_videos(channel_id, search_term, max_results)


def fetch_channel_info(
    channel_id: str,
) -> Dict:
    """
    Fetch basic channel information including subscriber count, view count, and video count.

    Args:
        channel_id (str): The YouTube channel ID

    Returns:
        Dict: Channel information including:
            - id: Channel ID
            - title: Channel title
            - description: Channel description
            - subscriberCount: Number of subscribers
            - viewCount: Total view count
            - videoCount: Number of videos
            - thumbnails: Channel thumbnails
    """
    return _fetch_channel_info(channel_id)


async def resolve_channel_id(
    channel_identifier: str,
) -> str:
    """
    Resolve a YouTube channel handle, custom URL, or channel ID to a channel ID.

    Args:
        channel_identifier (str): Can be:
            - Channel handle (e.g., "@channelname")
            - Custom URL (e.g., "youtube.com/c/channelname")
            - Channel ID (e.g., "UC...")

    Returns:
        str: The resolved channel ID

    Raises:
        ValueError: If the channel cannot be found
    """
    return await _resolve_channel_id(channel_identifier)


async def fetch_video_statistics(
    channel_id: str,
    max_results: int = 10,
    months: int = 6,
    min_duration_minutes: int = 3,
) -> List[Dict]:
    """
    Fetch statistics for recent videos on a channel.

    Args:
        channel_id (str): The YouTube channel ID
        max_results (int): Maximum number of videos to fetch statistics for (default: 10)
        months (int): Only include videos from the last X months (default: 6)
        min_duration_minutes (int): Minimum video duration in minutes (default: 3)

    Returns:
        List[Dict]: List of video statistics including:
            - videoId: Video ID
            - viewCount: Number of views
            - likeCount: Number of likes
            - commentCount: Number of comments
            - favoriteCount: Number of times the video was favorited
            - durationMinutes: Duration of the video in minutes
            - publishedAt: Publication date of the video
    """
    return await _fetch_video_statistics(
        channel_id, max_results, months, min_duration_minutes
    )


def fetch_videos(
    channel_id: str,
    max_results: int = 10,
) -> List[Dict]:
    """
    Fetch recent videos from a channel.

    Args:
        channel_id (str): The YouTube channel ID
        max_results (int): Maximum number of videos to fetch (default: 10)

    Returns:
        List[Dict]: List of video information including:
            - id: Video ID
            - title: Video title
            - description: Video description
            - publishedAt: Publication date
            - viewCount: Number of views
            - likeCount: Number of likes
            - commentCount: Number of comments
            - duration: Video duration
            - thumbnails: Video thumbnails
    """
    return _fetch_videos(channel_id, max_results)


def fetch_comments(
    video_id: str,
    max_results: int = 100,
) -> List[Dict]:
    """
    Fetch comments for a video.

    Args:
        video_id (str): The YouTube video ID
        max_results (int): Maximum number of comments to fetch (default: 100)

    Returns:
        List[Dict]: List of comment information including:
            - id: Comment ID
            - author: Author name
            - text: Comment text
            - likeCount: Number of likes
            - publishedAt: Publication date
    """
    return _fetch_comments(video_id, max_results)


def introspect_channel(
    identifier: str,
    max_videos: int = 10,
) -> Dict:
    """
    Resolve the identifier to a channel ID, fetch channel info and recent videos.
    """
    return _introspect_channel(identifier, max_videos)


def search_youtube_channels(
    query: str,
    max_results: int = 5,
) -> List[Dict]:
    """
    Search YouTube for channels related to the query.
    Returns a list of channel summaries including ID, title, description, and thumbnail.
    """
    return _search_youtube_channels(query, max_results)


def search_and_introspect_channel(
    query: str,
    video_count: int = 5,
) -> Dict:
    """
    Searches for YouTube channels by query, then fetches full info and videos for the top result.
    """
    return _search_and_introspect_channel(query, video_count)


fetch_video_details_tool = FunctionTool.from_defaults(fetch_video_details)
search_youtube_channel_videos_tool = FunctionTool.from_defaults(
    search_youtube_channel_videos
)
fetch_channel_info_tool = FunctionTool.from_defaults(fetch_channel_info)
resolve_channel_id_tool = FunctionTool.from_defaults(resolve_channel_id)
fetch_video_statistics_tool = FunctionTool.from_defaults(fetch_video_statistics)
fetch_videos_tool = FunctionTool.from_defaults(fetch_videos)
fetch_comments_tool = FunctionTool.from_defaults(fetch_comments)
introspect_channel_tool = FunctionTool.from_defaults(introspect_channel)
search_youtube_channels_tool = FunctionTool.from_defaults(search_youtube_channels)
search_and_introspect_channel_tool = FunctionTool.from_defaults(
    search_and_introspect_channel
)
