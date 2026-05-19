"""Social Media Content Engine.

Generates platform-specific content for TikTok, Instagram, Pinterest, and X/Twitter.
All content is designed for organic reach — no paid ads.
"""

import json
from datetime import datetime
from pathlib import Path

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output" / "content"


class SocialMediaEngine:
    """Generate platform-optimized social media content for anime POD marketing."""

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # TikTok
    # ------------------------------------------------------------------

    def generate_tiktok_content(self, product: dict | None = None, count: int = 5) -> list[dict]:
        """Generate TikTok video ideas and scripts for anime merch promotion.

        Args:
            product: Optional specific product to promote.
            count: Number of content pieces to generate.

        Returns:
            List of TikTok content with scripts, hooks, and hashtags.
        """
        product_context = ""
        if product:
            product_context = f"\nProduct to subtly promote: {json.dumps(product)}"

        prompt = f"""You are a viral TikTok content strategist for anime brands.

Create {count} TikTok video concepts for an anime t-shirt brand targeting
hardcore otaku in their 20s. The content should feel NATIVE to anime TikTok,
not like ads. Mix promotional and community content.{product_context}

Content style: aesthetic/clean vibes + community discussion
Tone: relatable, otaku-insider, fun, slightly unhinged

IMPORTANT: These should feel like organic anime content that HAPPENS to come
from a shirt brand — not ads. Think "anime page that also sells merch."

Provide JSON:
{{
    "tiktok_content": [
        {{
            "concept": "video concept in one line",
            "hook": "first 3 seconds hook (CRITICAL for retention)",
            "script": "full script/shot list (15-60 seconds)",
            "text_overlay": "on-screen text to display",
            "sound_suggestion": "trending sound or music type to use",
            "hashtags": ["15 hashtags mixing trending + niche"],
            "caption": "post caption",
            "content_type": "trend | discussion | product_showcase | meme | educational",
            "estimated_reach": "low | medium | high | viral_potential",
            "product_mention": "how/when to mention the product (if at all)",
            "posting_time": "best time to post (EST)"
        }}
    ]
}}"""

        result = self.ai.generate_json(prompt, temperature=0.9, max_tokens=3000)
        return result.get("tiktok_content", [])

    # ------------------------------------------------------------------
    # Instagram
    # ------------------------------------------------------------------

    def generate_instagram_content(self, product: dict | None = None, count: int = 5) -> list[dict]:
        """Generate Instagram content — reels, carousels, stories, and posts.

        Args:
            product: Optional specific product to promote.
            count: Number of content pieces to generate.

        Returns:
            List of Instagram content with captions, hashtags, and creative direction.
        """
        product_context = ""
        if product:
            product_context = f"\nProduct to feature: {json.dumps(product)}"

        prompt = f"""You are an Instagram growth strategist for anime brands.

Create {count} Instagram content pieces for an anime t-shirt brand. Mix content types.{product_context}

Audience: Hardcore otaku, 20s, global, unisex
Style: Aesthetic/clean + community discussion

Provide JSON:
{{
    "instagram_content": [
        {{
            "content_type": "reel | carousel | story | static_post",
            "concept": "content concept",
            "visual_direction": "what the visual should look like",
            "caption": "full caption with line breaks and emojis",
            "hashtags": ["30 hashtags — mix of big (500K+), medium (50K-500K), small (<50K)"],
            "call_to_action": "what action to drive",
            "story_slides": ["slide descriptions if carousel/story"],
            "reel_script": "script if reel",
            "posting_time": "best time to post",
            "engagement_strategy": "how to drive comments/saves/shares"
        }}
    ]
}}"""

        result = self.ai.generate_json(prompt, temperature=0.85, max_tokens=3000)
        return result.get("instagram_content", [])

    # ------------------------------------------------------------------
    # Pinterest
    # ------------------------------------------------------------------

    def generate_pinterest_content(self, products: list[dict] | None = None, count: int = 10) -> list[dict]:
        """Generate Pinterest pin ideas — the #1 free traffic source for POD.

        Args:
            products: List of products to create pins for.
            count: Number of pins to generate.

        Returns:
            List of pin concepts with SEO-optimized descriptions.
        """
        product_context = ""
        if products:
            product_context = f"\nProducts to pin: {json.dumps(products[:5])}"

        prompt = f"""You are a Pinterest marketing expert for print-on-demand.

Pinterest is the BEST free organic traffic source for POD. Create {count} pin concepts
for an anime typography t-shirt brand.{product_context}

IMPORTANT Pinterest rules:
- Pinterest is a search engine, not social media. SEO matters most.
- Vertical images (2:3 ratio) perform best
- Keyword-rich descriptions drive discovery
- Link every pin to the product page

Provide JSON:
{{
    "pins": [
        {{
            "pin_title": "SEO-optimized pin title (max 100 chars)",
            "pin_description": "keyword-rich description (max 500 chars)",
            "visual_direction": "what the pin image should look like",
            "board_name": "which Pinterest board this belongs to",
            "keywords": ["10 Pinterest SEO keywords"],
            "link_to": "product page or collection",
            "pin_type": "product_pin | inspiration | outfit_idea | gift_guide | listicle",
            "seasonal_relevance": "any seasonal angle"
        }}
    ],
    "board_strategy": [
        {{
            "board_name": "board name",
            "board_description": "SEO-optimized board description",
            "pin_frequency": "how often to pin to this board"
        }}
        // 5-8 boards
    ]
}}"""

        result = self.ai.generate_json(prompt, temperature=0.7, max_tokens=3000)
        return result.get("pins", [])

    # ------------------------------------------------------------------
    # X / Twitter
    # ------------------------------------------------------------------

    def generate_twitter_content(self, count: int = 10) -> list[dict]:
        """Generate X/Twitter content — tweets, threads, and polls.

        Args:
            count: Number of tweets to generate.

        Returns:
            List of tweet content.
        """
        prompt = f"""You are a Twitter/X content strategist for anime brands.

Create {count} tweets for an anime t-shirt brand. The goal is to build a community
of anime fans who eventually buy merch — NOT to sell directly.

Mix: anime takes, polls, memes, threads, and subtle product features.
Tone: relatable, otaku-insider, fun, slightly unhinged. Like your friend who
happens to sell anime shirts.

Provide JSON:
{{
    "tweets": [
        {{
            "tweet_text": "full tweet text (max 280 chars)",
            "tweet_type": "take | poll | meme | thread | product | question | quote_rt_bait",
            "poll_options": ["option1", "option2", "option3", "option4"],
            "thread_tweets": ["tweet2", "tweet3", "..."],
            "media_suggestion": "image/video to attach (if any)",
            "hashtags": ["relevant hashtags (use sparingly on X)"],
            "engagement_goal": "replies | retweets | likes | profile_visits",
            "posting_time": "best time to post"
        }}
    ]
}}"""

        result = self.ai.generate_json(prompt, temperature=0.9, max_tokens=2500)
        return result.get("tweets", [])

    # ------------------------------------------------------------------
    # Cross-platform batch generation
    # ------------------------------------------------------------------

    def generate_daily_content(self, product: dict | None = None) -> dict:
        """Generate a full day's content across all platforms.

        Args:
            product: Optional product to weave into content.

        Returns:
            Dictionary with content for all platforms.
        """
        content = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tiktok": self.generate_tiktok_content(product, count=2),
            "instagram": self.generate_instagram_content(product, count=2),
            "pinterest": self.generate_pinterest_content(count=5),
            "twitter": self.generate_twitter_content(count=5),
        }

        self._save_content(content)
        return content

    def _save_content(self, content: dict) -> Path:
        """Save generated content to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = OUTPUT_DIR / f"daily_content_{timestamp}.json"
        with open(filepath, "w") as f:
            json.dump(content, f, indent=2)
        return filepath
