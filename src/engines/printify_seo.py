"""Printify SEO Engine.

Optimizes product listings for organic search traffic on Printify
and external search engines (Google, Bing).
"""

import json
from datetime import datetime
from pathlib import Path

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output" / "seo"


class PrintifySEOEngine:
    """Generate SEO-optimized titles, descriptions, and tags for Printify listings."""

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def optimize_listing(self, design_brief: dict) -> dict:
        """Generate a fully SEO-optimized Printify listing from a design brief.

        Args:
            design_brief: Design brief from DesignBriefGenerator.

        Returns:
            Complete listing with title, description, tags, and SEO metadata.
        """
        prompt = f"""You are a Printify SEO expert specializing in anime t-shirts.

Create an SEO-optimized product listing for this design:
{json.dumps(design_brief, indent=2)}

Target audience: Hardcore otaku, 20s, unisex, global.
Platform: Printify Pop-Up Store.

RULES:
- Title must be under 140 characters but keyword-rich
- Description must be 150-300 words, compelling, with natural keyword placement
- Tags must be specific and searchable (not generic like "cool shirt")
- Include long-tail keywords that buyers actually search for

Provide JSON:
{{
    "title": "SEO-optimized product title",
    "description": "Full product description with keywords naturally woven in",
    "tags": ["13 highly specific, searchable tags"],
    "bullet_points": [
        "5 key selling points for the listing"
    ],
    "seo_metadata": {{
        "primary_keyword": "main search keyword",
        "secondary_keywords": ["5 secondary keywords"],
        "long_tail_keywords": ["5 long-tail search phrases buyers use"],
        "search_intent": "what the buyer is looking for when they'd find this"
    }},
    "category_suggestion": "best Printify category for this product",
    "pricing_suggestion": {{
        "recommended_price": 24.99,
        "reasoning": "why this price"
    }}
}}"""

        return self.ai.generate_json(
            prompt,
            system_prompt="You are a Printify SEO optimization expert. Return valid JSON.",
            temperature=0.6,
            max_tokens=2000,
        )

    def bulk_optimize(self, design_briefs: list[dict]) -> list[dict]:
        """Optimize multiple listings at once.

        Args:
            design_briefs: List of design briefs.

        Returns:
            List of optimized listings.
        """
        results = []
        for brief in design_briefs:
            listing = self.optimize_listing(brief)
            listing["source_brief"] = brief.get("design_name", "unknown")
            results.append(listing)

        self._save_listings(results)
        return results

    def generate_store_seo(self, store_name: str) -> dict:
        """Generate SEO strategy for the entire Printify store.

        Args:
            store_name: Name of the store.

        Returns:
            Store-level SEO strategy and content.
        """
        prompt = f"""You are an e-commerce SEO strategist.

Create a complete SEO strategy for an anime typography t-shirt store on Printify:
Store Name: {store_name}
Niche: Anime culture, otaku lifestyle
Products: Typography t-shirts with anime references

Provide JSON:
{{
    "store_title": "optimized store title",
    "store_description": "SEO-optimized store description (200 words)",
    "store_announcement": "short store announcement for visitors",
    "collection_ideas": [
        {{
            "name": "collection name",
            "description": "collection description",
            "keywords": ["target keywords for this collection"]
        }}
        // 5-7 collections
    ],
    "keyword_strategy": {{
        "primary_keywords": ["10 main keywords to target"],
        "long_tail": ["15 long-tail phrases"],
        "competitor_gaps": ["5 keywords competitors miss"]
    }},
    "content_strategy": "how to use blog/social for SEO backlinks",
    "google_seo_tips": ["5 tips for ranking in Google Shopping/Search"]
}}"""

        return self.ai.generate_json(prompt, temperature=0.6, max_tokens=2500)

    def keyword_research(self, topic: str) -> dict:
        """Deep keyword research for a specific anime topic.

        Args:
            topic: Topic to research (e.g., "Dragon Ball Z shirts", "anime aesthetic").

        Returns:
            Keyword research results.
        """
        prompt = f"""Perform deep keyword research for anime print-on-demand:
Topic: "{topic}"

Provide JSON:
{{
    "seed_keyword": "{topic}",
    "high_volume_keywords": ["10 high search volume keywords"],
    "medium_competition": ["10 medium competition keywords (best to target)"],
    "low_competition_gems": ["10 low competition keywords with decent volume"],
    "buyer_intent_keywords": ["10 keywords from people ready to buy"],
    "question_keywords": ["5 question-based keywords for content marketing"],
    "related_niches": ["5 related niches to cross-pollinate"]
}}"""

        return self.ai.generate_json(prompt, temperature=0.5, max_tokens=1500)

    def _save_listings(self, listings: list[dict]) -> Path:
        """Save optimized listings to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = OUTPUT_DIR / f"listings_{timestamp}.json"
        with open(filepath, "w") as f:
            json.dump(listings, f, indent=2)
        return filepath
