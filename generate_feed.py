import feedparser
from feedgen.feed import FeedGenerator
import re
from datetime import datetime
from html import escape

# Change this to any YouTube channel ID
CHANNEL_ID = 'UCsBjURrPoezykLs9EqgamOA'
YOUTUBE_FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
CHANNEL_LINK = f"https://www.youtube.com/channel/{CHANNEL_ID}"

def extract_video_id(entry):
    """Extract video ID from yt_videoid or entry.id"""
    if hasattr(entry, 'yt_videoid'):
        return entry.yt_videoid
    elif 'id' in entry:
        return entry.id.split(':')[-1]
    elif 'link' in entry:
        match = re.search(r"v=([a-zA-Z0-9_-]+)", entry.link)
        if match:
            return match.group(1)
    return None

def main():
    parsed = feedparser.parse(YOUTUBE_FEED)

    fg = FeedGenerator()
    fg.title(parsed.feed.get('title', 'YouTube Channel'))
    fg.link(href=CHANNEL_LINK)
    fg.description("Custom RSS feed with embedded YouTube videos")
    fg.language('en')

    for entry in parsed.entries:
        video_id = extract_video_id(entry)
        if not video_id:
            continue

        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        description = f"<![CDATA[{iframe}]]>"

        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.pubDate(entry.published)
        fe.description(description)

    fg.rss_file("feed.xml")
    print("✅ feed.xml generated successfully.")

if __name__ == "__main__":
    main()
