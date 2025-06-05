import re
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key not found in environment variables")

        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}


# Create a singleton instance
youtube_api = YouTubeAPI()


async def _resolve_channel_id(channel_identifier: str) -> str:
    try:
        # If it's already a channel ID (starts with UC), return it
        if re.match(r"^UC[a-zA-Z0-9_-]{22}$", channel_identifier):
            return channel_identifier

        # If it's a handle (starts with @), remove the @
        if channel_identifier.startswith("@"):
            channel_identifier = channel_identifier[1:]

        # If it's a URL, extract the handle
        if "youtube.com" in channel_identifier:
            # Handle different URL formats
            if "/c/" in channel_identifier:
                channel_identifier = channel_identifier.split("/c/")[-1].split("/")[0]
            elif "/channel/" in channel_identifier:
                channel_identifier = channel_identifier.split("/channel/")[-1].split(
                    "/"
                )[0]
            elif "/user/" in channel_identifier:
                channel_identifier = channel_identifier.split("/user/")[-1].split("/")[
                    0
                ]

        # Search for the channel
        request = youtube_api.youtube.search().list(
            part="snippet", q=channel_identifier, type="channel", maxResults=1
        )
        response = request.execute()

        if not response["items"]:
            raise ValueError(f"Channel not found: {channel_identifier}")

        return response["items"][0]["id"]["channelId"]

    except HttpError as e:
        raise Exception(f"Error resolving channel ID: {str(e)}")


async def _fetch_video_statistics(
    channel_id: str,
    max_results: int = 10,
    months: int = 6,
    min_duration_minutes: int = 3,
) -> List[Dict]:
    try:
        # First get the uploads playlist ID
        request = youtube_api.youtube.channels().list(
            part="contentDetails", id=channel_id
        )
        response = request.execute()

        if not response["items"]:
            raise ValueError(f"Channel not found: {channel_id}")

        uploads_playlist_id = response["items"][0]["contentDetails"][
            "relatedPlaylists"
        ]["uploads"]

        # Then get the videos from the uploads playlist
        request = youtube_api.youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,  # Increased to ensure we get enough videos after filtering
        )
        response = request.execute()

        # Get video IDs
        video_ids = [item["contentDetails"]["videoId"] for item in response["items"]]

        # Fetch statistics and content details for all videos in one request
        stats_request = youtube_api.youtube.videos().list(
            part="statistics,contentDetails,snippet", id=",".join(video_ids)
        )
        stats_response = stats_request.execute()

        # Calculate the cutoff date (X months ago)
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=30 * months)

        # Process and filter statistics
        video_stats = []
        for video in stats_response["items"]:
            try:
                # Parse publish date
                publish_date = datetime.strptime(
                    video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )

                # Parse duration (ISO 8601 format)
                duration_str = video.get("contentDetails", {}).get(
                    "duration", "PT0S"
                )  # Default to 0 seconds if duration is missing
                duration_minutes = 0

                # Handle hours
                if "H" in duration_str:
                    hours_part = duration_str.split("H")[0]
                    if "T" in hours_part:
                        hours = int(hours_part.split("T")[1])
                    else:
                        hours = int(hours_part)
                    duration_minutes += hours * 60

                # Handle minutes
                if "M" in duration_str:
                    minutes_part = duration_str.split("M")[0]
                    if "H" in minutes_part:
                        minutes = int(minutes_part.split("H")[-1])
                    elif "T" in minutes_part:
                        minutes = int(minutes_part.split("T")[-1])
                    else:
                        minutes = int(minutes_part)
                    duration_minutes += minutes

                # Handle seconds (convert to minutes if needed)
                if "S" in duration_str:
                    seconds_part = duration_str.split("S")[0]
                    if "M" in seconds_part:
                        seconds = int(seconds_part.split("M")[-1])
                    elif "H" in seconds_part:
                        seconds = int(seconds_part.split("H")[-1])
                    elif "T" in seconds_part:
                        seconds = int(seconds_part.split("T")[-1])
                    else:
                        seconds = int(seconds_part)
                    duration_minutes += seconds / 60

                # Apply filters
                if (
                    publish_date < cutoff_date
                    or duration_minutes < min_duration_minutes
                ):
                    continue

                stats = video.get("statistics", {})
                video_stats.append(
                    {
                        "videoId": video["id"],
                        "viewCount": int(stats.get("viewCount", 0)),
                        "likeCount": int(stats.get("likeCount", 0)),
                        "commentCount": int(stats.get("commentCount", 0)),
                        "favoriteCount": int(stats.get("favoriteCount", 0)),
                        "durationMinutes": round(duration_minutes, 2),
                        "publishedAt": video["snippet"]["publishedAt"],
                    }
                )

                # Stop if we have enough videos
                if len(video_stats) >= max_results:
                    break
            except Exception as e:
                # Skip videos that cause errors
                continue

        return video_stats
    except HttpError as e:
        raise Exception(f"Error fetching video statistics: {str(e)}")
