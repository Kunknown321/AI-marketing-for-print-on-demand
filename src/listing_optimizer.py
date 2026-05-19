"""Product listing optimization using AI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ListingOptimizer:
    """Optimize product listings for print-on-demand marketplaces."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def optimize(
        self,
        product_type: str,
        design_description: str,
        target_platform: str = "etsy",
        style: str = "professional",
    ) -> dict:
        """Generate optimized title, description, and tags for a product listing.

        Args:
            product_type: Type of product (e.g., "t-shirt", "mug", "poster").
            design_description: Description of the design.
            target_platform: Target marketplace (e.g., "etsy", "amazon", "redbubble").
            style: Writing style for the listing.

        Returns:
            Dictionary with optimized title, description, and tags.
        """
        prompt = f"""You are an expert print-on-demand marketplace listing optimizer.

Create an optimized product listing for the following:
- Product Type: {product_type}
- Design Description: {design_description}
- Target Platform: {target_platform}
- Writing Style: {style}

Provide the following in JSON format:
1. "title": An SEO-optimized title (max 140 characters)
2. "description": A compelling product description (200-300 words)
3. "tags": A list of 13 relevant tags/keywords
4. "bullet_points": 5 key selling points

Consider platform-specific best practices for {target_platform}."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return {
            "platform": target_platform,
            "product_type": product_type,
            "optimized_listing": response.choices[0].message.content,
        }

    def bulk_optimize(self, products: list[dict]) -> list[dict]:
        """Optimize multiple product listings.

        Args:
            products: List of dicts with product_type, design_description, and target_platform.

        Returns:
            List of optimized listings.
        """
        return [self.optimize(**product) for product in products]
