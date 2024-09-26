import os
from googleapiclient.discovery import build
from bitlyshortener import Shortener

# Set up YouTube API credentials and Bitly API token
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
BITLY_ACCESS_TOKEN = 'YOUR_BITLY_ACCESS_TOKEN'

# YouTube video ID and URL
video_id = 'aem3s8O5uFU'
video_url = f"https://www.youtube.com/watch?v={video_id}"

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to get YouTube video statistics
def get_video_stats(video_id):
    request = youtube.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    stats = response['items'][0]['statistics']
    return stats

# Function to shorten URL using Bitly
def shorten_url(url):
    shortener = Shortener(tokens=[BITLY_ACCESS_TOKEN], max_cache_size=256)
    short_url = shortener.shorten_urls([url])[0]
    return short_url

if __name__ == "__main__":
    # Get video statistics
    stats = get_video_stats(video_id)
    print(f"Video Statistics for Video ID {video_id}:")
    print(f"Views: {stats.get('viewCount')}")
    print(f"Likes: {stats.get('likeCount')}")
    print(f"Comments: {stats.get('commentCount')}")

    # Shorten the YouTube video URL
    short_url = shorten_url(video_url)
    print(f"Shortened URL: {short_url}")

    # Share the short URL and track the number of clicks via the Bitly dashboard
