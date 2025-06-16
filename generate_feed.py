# File: generate_feed.py
import feedparser
from feedgen.feed import FeedGenerator
import re

# Your source YouTube channel RSS feed URL
CHANNEL_ID = 'UCsBjURrPoezykLs9EqgamOA'  # Fireship
YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def extract_youtube_id(youtube_url):
    """
    Extract YouTube video ID from URL, e.g.:
    https://www.youtube.com/watch?v=VIDEO_ID
    or https://youtu.be/VIDEO_ID
    """
    # Common YouTube video ID patterns
    patterns = [
        r"v=([^&]+)",       # ?v=VIDEO_ID
        r"youtu\.be/([^?&]+)" # youtu.be/VIDEO_ID
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

def main():
    # Parse the original YouTube RSS feed
    d = feedparser.parse(YOUTUBE_RSS_URL)
    
    fg = FeedGenerator()
    fg.title(d.feed.title)
    fg.link(href=d.feed.link)
    fg.description(d.feed.get('subtitle', 'YouTube Channel RSS Feed with embedded videos'))
    fg.language('en')

    for entry in d.entries:
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.link(href=entry.link)

        video_id = extract_youtube_id(entry.link)
        if video_id:
            iframe_html = f"""<![CDATA[
                <iframe width="560" height="315"
                    src="https://www.youtube.com/embed/{video_id}"
                    frameborder="0" allowfullscreen>
                </iframe>
                <p>{entry.summary}</p>
            ]]>"""
            fe.description(iframe_html)
        else:
            # Fallback: just use plain summary if no video ID found
            fe.description(entry.summary)

    # Save to feed.xml
    fg.rss_file("feed.xml")
    print("feed.xml generated with embedded YouTube iframes.")

if __name__ == "__main__":
    main()

