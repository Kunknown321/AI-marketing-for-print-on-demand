"""Anime Trend Intelligence Engine.

Discovers trending anime topics, characters, quotes, and cultural moments
from free sources so you always know what's hot — without watching anime.
"""

import json
import re
from datetime import datetime

import requests

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


class AnimeTrendIntelligence:
    """Scrape and analyze trending anime topics for design and content ideas."""

    JIKAN_BASE = "https://api.jikan.moe/v4"  # Free MyAnimeList API
    REDDIT_BASE = "https://www.reddit.com"

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OtakuPrintMarketingEngine/1.0"
        })

    # ------------------------------------------------------------------
    # Data collection from free APIs
    # ------------------------------------------------------------------

    def get_top_airing_anime(self, limit: int = 25) -> list[dict]:
        """Get currently airing top anime from MyAnimeList (via Jikan API).

        Returns:
            List of anime with title, score, synopsis, genres.
        """
        resp = self.session.get(
            f"{self.JIKAN_BASE}/top/anime",
            params={"filter": "airing", "limit": limit},
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

        return [
            {
                "title": anime["title"],
                "title_japanese": anime.get("title_japanese", ""),
                "score": anime.get("score"),
                "members": anime.get("members"),
                "synopsis": (anime.get("synopsis") or "")[:200],
                "genres": [g["name"] for g in anime.get("genres", [])],
                "themes": [t["name"] for t in anime.get("themes", [])],
                "url": anime.get("url", ""),
            }
            for anime in data
        ]

    def get_top_anime_alltime(self, limit: int = 25) -> list[dict]:
        """Get all-time top-rated anime."""
        resp = self.session.get(
            f"{self.JIKAN_BASE}/top/anime",
            params={"limit": limit},
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

        return [
            {
                "title": anime["title"],
                "title_japanese": anime.get("title_japanese", ""),
                "score": anime.get("score"),
                "members": anime.get("members"),
                "genres": [g["name"] for g in anime.get("genres", [])],
            }
            for anime in data
        ]

    def get_trending_reddit_posts(
        self, subreddit: str = "anime", limit: int = 25
    ) -> list[dict]:
        """Get trending posts from anime subreddits.

        Args:
            subreddit: Subreddit to scrape (anime, animemes, goodanimemes, etc.).
            limit: Number of posts.

        Returns:
            List of trending posts with titles and engagement.
        """
        try:
            resp = self.session.get(
                f"{self.REDDIT_BASE}/r/{subreddit}/hot.json",
                params={"limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
        except requests.RequestException:
            return []

        posts = resp.json()["data"]["children"]

        return [
            {
                "title": post["data"]["title"],
                "score": post["data"]["score"],
                "num_comments": post["data"]["num_comments"],
                "subreddit": subreddit,
                "url": post["data"]["url"],
                "created": datetime.fromtimestamp(
                    post["data"]["created_utc"]
                ).isoformat(),
            }
            for post in posts
            if not post["data"].get("stickied")
        ]

    def get_anime_quotes(self, anime_title: str | None = None) -> list[dict]:
        """Get popular anime quotes via the Animechan API.

        Args:
            anime_title: Optional specific anime to get quotes from.

        Returns:
            List of quotes with character and anime info.
        """
        url = "https://animechan.io/api/v1/quotes/random"
        params = {}
        if anime_title:
            params["anime"] = anime_title

        quotes = []
        for _ in range(10):
            try:
                resp = self.session.get(url, params=params, timeout=5)
                if resp.ok:
                    data = resp.json().get("data", resp.json())
                    if isinstance(data, dict):
                        quotes.append({
                            "quote": data.get("content", ""),
                            "character": data.get("character", {}).get("name", "Unknown"),
                            "anime": data.get("anime", {}).get("name", "Unknown"),
                        })
            except (requests.RequestException, KeyError):
                continue

        return quotes

    # ------------------------------------------------------------------
    # AI-powered trend analysis
    # ------------------------------------------------------------------

    def analyze_trends(self) -> dict:
        """Run full trend analysis combining all data sources.

        Returns:
            Comprehensive trend report with design opportunities.
        """
        airing = self.get_top_airing_anime(15)
        alltime = self.get_top_anime_alltime(15)

        reddit_anime = self.get_trending_reddit_posts("anime", 15)
        reddit_memes = self.get_trending_reddit_posts("animemes", 15)

        reddit_section = ""
        if reddit_anime:
            reddit_section += f"\nTRENDING REDDIT r/anime:\n{json.dumps(reddit_anime, indent=2)}"
        if reddit_memes:
            reddit_section += f"\nTRENDING REDDIT r/animemes:\n{json.dumps(reddit_memes, indent=2)}"
        if not reddit_section:
            reddit_section = "\n(Reddit data unavailable — use your own knowledge of current anime community trends)"

        prompt = f"""You are an anime culture and print-on-demand market research expert.

Analyze this data to identify the HOTTEST opportunities for anime typography t-shirt designs.

CURRENTLY AIRING TOP ANIME:
{json.dumps(airing, indent=2)}

ALL-TIME TOP ANIME (evergreen):
{json.dumps(alltime, indent=2)}
{reddit_section}

Provide a JSON report with:
{{
    "trending_now": [top 5 anime/topics that are HOT right now],
    "evergreen_goldmines": [top 5 anime that ALWAYS sell],
    "viral_meme_themes": [top 5 meme themes from Reddit that could be t-shirt designs],
    "typography_design_ideas": [
        {{
            "text": "the exact text for the shirt",
            "style": "japanese_english | minimalist_streetwear | bold_graphic | retro_vintage",
            "related_anime": "which anime it references",
            "target_emotion": "what feeling it evokes",
            "virality_score": 1-10
        }}
        // Generate 15 design ideas
    ],
    "trending_hashtags": [20 trending hashtags in the anime community right now],
    "content_hooks": [10 social media post hooks that would go viral in the anime community],
    "key_insight": "one paragraph summary of the biggest opportunity right now"
}}"""

        return self.ai.generate_json(
            prompt,
            system_prompt="You are a data-driven anime market research AI. Always return valid JSON.",
            temperature=0.8,
            max_tokens=3000,
        )

    def get_seasonal_trends(self) -> dict:
        """Identify seasonal anime trends and events.

        Returns:
            Seasonal trends and event-based design opportunities.
        """
        now = datetime.now()
        month = now.strftime("%B")
        season = _get_anime_season(now.month)

        prompt = f"""You are an anime culture expert. It's currently {month} ({season} anime season).

Identify seasonal opportunities for anime t-shirt designs:

Provide JSON:
{{
    "current_season": "{season}",
    "seasonal_anime": [top anime this season],
    "upcoming_events": [anime conventions, movie releases, game launches in the next 30 days],
    "seasonal_design_ideas": [
        {{
            "text": "typography text for shirt",
            "occasion": "what event/season it's for",
            "urgency": "how time-sensitive (1-10)",
            "style": "design style"
        }}
        // 10 ideas
    ],
    "holiday_tie_ins": [any holidays or cultural moments to capitalize on]
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=2000)

    def discover_niche_opportunities(self, sub_niche: str) -> dict:
        """Deep dive into a specific anime sub-niche.

        Args:
            sub_niche: Specific sub-niche to explore (e.g., "shonen", "isekai", "slice_of_life").

        Returns:
            Sub-niche analysis with design ideas.
        """
        prompt = f"""You are an anime print-on-demand niche research expert.

Deep dive into the "{sub_niche}" anime sub-niche for t-shirt typography designs.

Provide JSON:
{{
    "sub_niche": "{sub_niche}",
    "audience_size": "estimated audience size and engagement level",
    "top_series": [top 10 anime/manga in this sub-niche],
    "iconic_phrases": [15 iconic phrases, quotes, and catchphrases from this sub-niche],
    "slang_terms": [10 community slang terms that insiders would love on a shirt],
    "design_ideas": [
        {{
            "text": "exact text for the shirt",
            "japanese_text": "Japanese version if applicable",
            "explanation": "what it means and why fans love it",
            "style": "typography style",
            "estimated_demand": "high/medium/low"
        }}
        // 10 ideas
    ],
    "competition_level": "high/medium/low",
    "recommendation": "should we pursue this sub-niche and why"
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=2500)


def _get_anime_season(month: int) -> str:
    """Map month to anime season."""
    if month in (1, 2, 3):
        return "Winter"
    if month in (4, 5, 6):
        return "Spring"
    if month in (7, 8, 9):
        return "Summer"
    return "Fall"
