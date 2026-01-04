"""
Job Alerts Service - Fetches govt job alerts from RSS feeds
"""
import aiohttp
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# RSS Feed URLs for govt jobs
RSS_FEEDS = {
    "central": "https://www.freejobalert.com/central-govt-jobs/feed/",
    "railway": "https://www.freejobalert.com/railway-jobs/feed/",
    "bank": "https://www.freejobalert.com/bank-jobs/feed/",
    "ssc": "https://www.freejobalert.com/ssc-jobs/feed/",
    "upsc": "https://www.freejobalert.com/upsc-jobs/feed/",
    "state": "https://www.freejobalert.com/state-govt-jobs/feed/",
}

async def fetch_rss_feed(url: str, limit: int = 5) -> List[Dict]:
    """Fetch and parse RSS feed, return list of job items."""
    jobs = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    content = await response.text()
                    root = ET.fromstring(content)
                    
                    # Parse RSS items
                    for item in root.findall('.//item')[:limit]:
                        title = item.find('title')
                        link = item.find('link')
                        pub_date = item.find('pubDate')
                        
                        if title is not None and link is not None:
                            jobs.append({
                                "title": title.text or "No Title",
                                "link": link.text or "",
                                "date": pub_date.text[:16] if pub_date is not None and pub_date.text else "Recent"
                            })
    except Exception as e:
        logger.error(f"Error fetching RSS feed {url}: {e}")
    
    return jobs

async def get_job_alerts(category: str = "central", limit: int = 5) -> List[Dict]:
    """Get job alerts for a specific category."""
    url = RSS_FEEDS.get(category.lower(), RSS_FEEDS["central"])
    return await fetch_rss_feed(url, limit)

async def get_all_latest_jobs(limit_per_category: int = 2) -> Dict[str, List[Dict]]:
    """Get latest jobs from all categories."""
    all_jobs = {}
    for category, url in RSS_FEEDS.items():
        jobs = await fetch_rss_feed(url, limit_per_category)
        if jobs:
            all_jobs[category] = jobs
    return all_jobs

# Category display names
CATEGORY_NAMES = {
    "central": "🏛️ Central Govt",
    "railway": "🚂 Railway",
    "bank": "🏦 Bank",
    "ssc": "📝 SSC",
    "upsc": "🎖️ UPSC",
    "state": "🗺️ State Govt"
}

def get_category_emoji(category: str) -> str:
    """Get emoji for job category."""
    emojis = {
        "central": "🏛️",
        "railway": "🚂",
        "bank": "🏦",
        "ssc": "📝",
        "upsc": "🎖️",
        "state": "🗺️"
    }
    return emojis.get(category.lower(), "💼")
