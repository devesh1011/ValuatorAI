from typing import Annotated, List, Dict
from .helper.helpers import _resolve_channel_id, _fetch_video_statistics


async def resolve_channel_id(
    channel_identifier: Annotated[
        str,
        """
        The identifier of the YouTube channel, which can be one of the following:
        - Channel handle (e.g., "@channelname")
        - Custom URL (e.g., "youtube.com/c/channelname")
        - Channel ID (e.g., "UC...")
        The function will resolve this identifier to the YouTube channel ID.
        Example: For "@channelname", "youtube.com/c/channelname", or "UCxxxxxxx", it will return the resolved channel ID.
    """,
    ],
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


# import asyncio

# response = asyncio.run(resolve_channel_id("Matthew Berman"))
# print(response)


async def fetch_video_statistics(
    channel_id: Annotated[
        str,
        """
        The unique identifier of the YouTube channel.
        This is the part of the YouTube URL after '/channel/'. For example:
        - For the URL 'https://www.youtube.com/channel/UCxxxxxxx', the `channel_id` would be 'UCxxxxxxx'.
        - This can also be the channel ID directly (e.g., 'UC1234567890').
    """,
    ],
    max_results: Annotated[
        int,
        """
        The maximum number of videos to fetch statistics for.
        This value controls how many recent videos will be analyzed.
        Default is 10, but can be set to any integer value.
    """,
    ] = 10,
    months: Annotated[
        int,
        """
        Only include videos published within this number of months.
        Default is 6 months.
    """,
    ] = 6,
    min_duration_minutes: Annotated[
        int,
        """
        Only include videos that are at least this many minutes long.
        Default is 3 minutes.
    """,
    ] = 3,
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
