"""SEO optimization for print-on-demand stores and listings using AI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SEOOptimizer:
    """AI-powered SEO optimization for POD stores and listings."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def research_keywords(self, niche: str, platform: str = "etsy") -> dict:
        """Research keywords for a specific niche and platform.

        Args:
            niche: The niche to research.
            platform: Target marketplace or website.

        Returns:
            Keyword research results with search intent analysis.
        """
        prompt = f"""You are an SEO expert specializing in print-on-demand marketplaces.

Perform keyword research for:
- Niche: {niche}
- Platform: {platform}

Provide in JSON format:
1. "primary_keywords": 10 high-volume primary keywords
2. "long_tail_keywords": 15 long-tail keyword phrases
3. "trending_keywords": 5 currently trending related keywords
4. "seasonal_keywords": keywords with seasonal relevance
5. "competitor_keywords": keywords competitors are likely targeting
6. "search_intent": categorize keywords by search intent (informational, transactional, navigational)
7. "keyword_strategy": recommended strategy for using these keywords"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1500,
        )

        return {
            "niche": niche,
            "platform": platform,
            "keywords": response.choices[0].message.content,
        }

    def optimize_store_page(self, store_name: str, niche: str, current_description: str = "") -> dict:
        """Generate SEO-optimized content for a POD store page.

        Args:
            store_name: Name of the store.
            niche: Store's primary niche.
            current_description: Current store description (if any).

        Returns:
            SEO-optimized store page content.
        """
        context = f"\nCurrent Description: {current_description}" if current_description else ""

        prompt = f"""You are an SEO expert for e-commerce stores.

Optimize the store page for:
- Store Name: {store_name}
- Niche: {niche}{context}

Provide in JSON format:
1. "store_title": SEO-optimized store title
2. "meta_description": Meta description (155 characters max)
3. "store_description": Optimized store description (150-200 words)
4. "about_section": Compelling about section
5. "seo_tips": 5 actionable SEO tips for this store"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return {
            "store_name": store_name,
            "optimization": response.choices[0].message.content,
        }
