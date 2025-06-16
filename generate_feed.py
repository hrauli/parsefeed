# File: generate_feed.py

import feedparser
from feedgen.feed import FeedGenerator

CHANNEL_ID = 'UCsBjURrPoezykLs9EqgamOA'  # Fireship
YOUTUBE_FEED = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'

def generate_feed():
    parsed = feedparser.parse(YOUTUBE_FEED)

    fg = FeedGenerator()
    fg.title('Fireship YouTube Feed (with embeds)')
    fg.link(href=f'https://www.youtube.com/channel/{CHANNEL_ID}', rel='alternate')
    fg.description('Custom RSS feed for Fireship with embedded YouTube players')

    for entry in parsed.entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link(href=entry.link)
        video_id = entry.link.split('v=')[-1] if 'v=' in entry.link else entry.link.split('/')[-1]
        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        fe.description(f"<![CDATA[{iframe}]]>")
        fe.pubDate(entry.published)

    fg.rss_file('feed.xml')  # Writes the RSS feed to feed.xml

if __name__ == '__main__':
    generate_feed()
