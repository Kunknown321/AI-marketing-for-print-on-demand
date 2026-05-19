"""Social media content generation for print-on-demand marketing using AI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SocialMediaGenerator:
    """Generate engaging social media content for POD product promotion."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def generate_post(
        self,
        product_type: str,
        design_description: str,
        platform: str = "instagram",
        post_type: str = "promotional",
    ) -> dict:
        """Generate a social media post for a POD product.

        Args:
            product_type: Type of product.
            design_description: Description of the design.
            platform: Social media platform.
            post_type: Type of post (promotional, educational, engagement, story).

        Returns:
            Generated social media post content.
        """
        prompt = f"""You are a social media marketing expert for print-on-demand brands.

Create a {post_type} social media post for:
- Product: {product_type}
- Design: {design_description}
- Platform: {platform}

Provide in JSON format:
1. "caption": Engaging caption with emojis (platform-appropriate length)
2. "hashtags": 20-30 relevant hashtags (mix of popular and niche)
3. "call_to_action": Clear CTA
4. "best_posting_time": Recommended posting time
5. "content_tip": Tip for the visual content to pair with this post
6. "engagement_hook": Opening hook to stop scrolling"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1000,
        )

        return {
            "platform": platform,
            "post_type": post_type,
            "content": response.choices[0].message.content,
        }

    def create_content_calendar(
        self,
        niche: str,
        days: int = 7,
        platforms: list[str] | None = None,
    ) -> dict:
        """Generate a content calendar for POD social media marketing.

        Args:
            niche: The product niche.
            days: Number of days to plan for.
            platforms: Target social media platforms.

        Returns:
            Content calendar with daily post ideas.
        """
        if platforms is None:
            platforms = ["instagram", "pinterest", "tiktok"]

        prompt = f"""You are a social media strategist for print-on-demand businesses.

Create a {days}-day content calendar for:
- Niche: {niche}
- Platforms: {', '.join(platforms)}

For each day, provide in JSON format:
1. Day number
2. Platform
3. Content type (reel, carousel, story, pin, etc.)
4. Post idea/theme
5. Caption outline
6. Hashtag suggestions (5 per post)
7. Best posting time

Mix content types: promotional (30%), educational (30%), engagement (20%), behind-the-scenes (20%)."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=3000,
        )

        return {
            "niche": niche,
            "days": days,
            "platforms": platforms,
            "calendar": response.choices[0].message.content,
        }
