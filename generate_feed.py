import feedparser
from feedgen.feed import FeedGenerator
import re
import json
from datetime import datetime

def load_channels(filepath='channels.json'):
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_video_id(entry):
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
    channels = load_channels()

    fg = FeedGenerator()
    fg.title("Combined YouTube Channels Feed")
    fg.link(href="https://www.youtube.com")
    fg.description("Custom RSS feed with embedded YouTube videos from multiple channels")
    fg.language('en')

    all_entries = []

    for channel in channels:
        channel_id = channel['id']
        channel_name = channel.get('name', channel_id)
        feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        parsed = feedparser.parse(feed_url)

        for entry in parsed.entries:
            entry.channel_name = channel_name
            all_entries.append(entry)

    # Sort all videos by published date descending
    all_entries.sort(key=lambda e: datetime(*e.published_parsed[:6]), reverse=True)

    for entry in all_entries:
        video_id = extract_video_id(entry)
        if not video_id:
            continue
        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'

        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(f"[{entry.channel_name}] {entry.title}")
        fe.link(href=entry.link)
        fe.pubDate(entry.published)
        fe.description(iframe)

    fg.rss_file("combined_feed.xml")
    print("✅ combined_feed.xml generated with multiple channels.")

if __name__ == "__main__":
    main()
