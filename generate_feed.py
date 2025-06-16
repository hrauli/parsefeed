import feedparser
from feedgen.feed import FeedGenerator
import re

CHANNEL_ID = 'UCsBjURrPoezykLs9EqgamOA'
YOUTUBE_FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def extract_youtube_id(entry):
    """
    Extracts YouTube video ID from <yt:videoId> or <id> fields
    """
    # feedparser exposes it as 'yt_videoid'
    if hasattr(entry, 'yt_videoid'):
        return entry.yt_videoid
    elif 'id' in entry:
        # Example: 'yt:video:VIDEO_ID'
        parts = entry.id.split(':')
        return parts[-1] if len(parts) > 0 else None
    elif 'link' in entry:
        match = re.search(r"v=([a-zA-Z0-9_-]+)", entry.link)
        if match:
            return match.group(1)
    return None

def main():
    feed = feedparser.parse(YOUTUBE_FEED)

    fg = FeedGenerator()
    fg.title("Fireship Videos (With Embeds)")
    fg.link(href=f"https://www.youtube.com/channel/{CHANNEL_ID}")
    fg.description("Custom RSS feed with embedded YouTube videos")
    fg.language('en')

    for entry in feed.entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.pubDate(entry.published)

        video_id = extract_youtube_id(entry)
        if video_id:
            iframe_html = f"""
            <iframe width="560" height="315" 
                src="https://www.youtube.com/embed/{video_id}" 
                frameborder="0" allowfullscreen>
            </iframe>
            """
            fe.description(f"<![CDATA[{iframe_html}]]>")
        else:
            fe.description(entry.get('summary', ''))

    fg.rss_file("feed.xml")
    print("✅ feed.xml generated with embedded videos!")

if __name__ == "__main__":
    main()
