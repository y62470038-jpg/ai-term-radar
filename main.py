import feedparser
import requests
import re
from datetime import date

# Simple demo: gather new AI terms from RSS feeds and GitHub repos
rss_feeds = [
    'https://hnrss.org/newest?q=AI',
    'https://huggingface.co/blog/feed.xml'
]

keywords = set()

# Fetch RSS entries
def fetch_rss(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:10]:
            title = entry.get('title', '')
            # Extract potential new terms: capitalized words or acronyms
            for word in re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]{2,}\b', title):
                if len(word) > 2:
                    keywords.add(word)
    except Exception as e:
        print(f'Error fetching {feed_url}: {e}')

# Fetch GitHub trending (simple public API)
def fetch_github_trending():
    url = 'https://api.github.com/search/repositories?q=AI+created:>'+date.today().isoformat()+'&sort=stars&order=desc&per_page=10'
    try:
        resp = requests.get(url, timeout=5)
        for repo in resp.json().get('items', []):
            name = repo['name']
            # Extract camelCase or acronyms
            for word in re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', name):
                if len(word) > 2:
                    keywords.add(word)
    except Exception as e:
        print(f'GitHub error: {e}')

for url in rss_feeds:
    fetch_rss(url)
fetch_github_trending()

# Generate simple report
date_str = date.today().isoformat()
report_lines = [f'# AI Term Radar - {date_str}', '', 'New terms detected:', '']
for word in sorted(keywords):
    report_lines.append(f'- {word}')
with open('terms.md', 'w') as f:
    f.write('\n'.join(report_lines))
print('Report written to terms.md')
