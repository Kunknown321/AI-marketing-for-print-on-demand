"""Hashtag & SEO Research Module.

Platform-specific hashtag research and strategy for organic discoverability.
"""

import json
from datetime import datetime

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


class HashtagResearch:
    """Generate platform-specific hashtag strategies for anime POD content."""

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()

    def generate_hashtag_bank(self) -> dict:
        """Generate a complete hashtag bank organized by category and platform.

        Returns:
            Categorized hashtag bank for all platforms.
        """
        prompt = """Create a comprehensive hashtag bank for an anime typography t-shirt brand.

Organize by platform AND category. Include hashtag sizes (approximate post counts).

Provide JSON:
{
    "instagram": {
        "mega_hashtags": [{"tag": "#anime", "approx_posts": "100M+", "use": "sparingly"}],
        "large_hashtags": [{"tag": "#otaku", "approx_posts": "10M-100M", "use": "1-2 per post"}],
        "medium_hashtags": [{"tag": "#animeshirt", "approx_posts": "100K-10M", "use": "5-8 per post"}],
        "small_niche": [{"tag": "#otakufashion", "approx_posts": "10K-100K", "use": "5-8 per post"}],
        "micro_niche": [{"tag": "#animetypography", "approx_posts": "<10K", "use": "3-5 per post"}],
        "branded": ["#YourBrandName", "#WearYourAnime"],
        "optimal_count": 25,
        "strategy": "how to mix sizes for maximum reach"
    },
    "tiktok": {
        "trending": [{"tag": "#animetiktok", "note": "trending context"}],
        "niche": [{"tag": "#animemerch", "note": "why it works"}],
        "community": [{"tag": "#animecommunity", "note": "context"}],
        "optimal_count": 5,
        "strategy": "TikTok hashtag best practices"
    },
    "pinterest": {
        "seo_keywords": [{"tag": "anime t-shirt", "search_volume": "high"}],
        "long_tail": [{"tag": "anime aesthetic clothing for men", "search_volume": "medium"}],
        "strategy": "Pinterest SEO approach (keywords > hashtags)"
    },
    "twitter": {
        "community": ["#AnimeTwitter", "#Otaku"],
        "trending_to_watch": ["hashtags that trend regularly"],
        "optimal_count": "2-3 max",
        "strategy": "Twitter hashtag approach"
    },
    "hashtag_sets": [
        {
            "name": "Product Launch Set",
            "use_when": "posting a new product",
            "instagram": ["30 hashtags"],
            "tiktok": ["5 hashtags"],
            "twitter": ["3 hashtags"]
        },
        {
            "name": "Community Engagement Set",
            "use_when": "posting discussion/meme content",
            "instagram": ["30 hashtags"],
            "tiktok": ["5 hashtags"],
            "twitter": ["3 hashtags"]
        },
        {
            "name": "Aesthetic/Vibe Set",
            "use_when": "posting aesthetic content",
            "instagram": ["30 hashtags"],
            "tiktok": ["5 hashtags"],
            "twitter": ["3 hashtags"]
        }
    ]
}

Make sure hashtags are REAL and commonly used in the anime community."""

        return self.ai.generate_json(
            prompt,
            system_prompt="You are a social media hashtag expert for anime brands.",
            temperature=0.6,
            max_tokens=4000,
        )

    def get_trending_hashtags(self, platform: str = "all") -> dict:
        """Get currently trending anime hashtags.

        Args:
            platform: Specific platform or "all".

        Returns:
            Trending hashtags with context.
        """
        today = datetime.now().strftime("%B %d, %Y")

        prompt = f"""What anime-related hashtags are likely trending or performing well
as of {today}? Consider current anime seasons, recent releases, and ongoing trends.

Platform focus: {platform}

Provide JSON:
{{
    "date": "{today}",
    "trending_hashtags": [
        {{
            "hashtag": "#hashtag",
            "platform": "platform",
            "reason": "why it's trending",
            "relevance_to_merch": "how to tie it to t-shirt sales",
            "shelf_life": "how long this trend will last"
        }}
    ],
    "emerging_hashtags": ["hashtags starting to gain traction"],
    "evergreen_performers": ["hashtags that consistently perform well"]
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=2000)

    def optimize_hashtags_for_post(self, post_caption: str, platform: str) -> dict:
        """Optimize hashtags for a specific post.

        Args:
            post_caption: The post caption/content.
            platform: Target platform.

        Returns:
            Optimized hashtag set.
        """
        prompt = f"""Optimize hashtags for this {platform} post about anime merch:

"{post_caption}"

Provide JSON:
{{
    "recommended_hashtags": ["optimized list of hashtags"],
    "hashtag_count": "total number",
    "placement": "where to put them (caption, comment, etc.)",
    "reasoning": "why these hashtags were chosen"
}}"""

        return self.ai.generate_json(prompt, temperature=0.6, max_tokens=1000)
