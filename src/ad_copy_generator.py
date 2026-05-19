"""Ad copy generation for print-on-demand products using AI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AdCopyGenerator:
    """Generate compelling ad copy for POD products across platforms."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        product_type: str,
        design_description: str,
        ad_platform: str = "facebook",
        tone: str = "engaging",
        target_audience: str = "",
    ) -> dict:
        """Generate ad copy for a specific platform.

        Args:
            product_type: Type of product.
            design_description: Description of the design.
            ad_platform: Advertising platform (facebook, instagram, pinterest, google).
            tone: Desired tone of the ad copy.
            target_audience: Description of target audience.

        Returns:
            Generated ad copy with variations.
        """
        audience_info = f"\nTarget Audience: {target_audience}" if target_audience else ""

        prompt = f"""You are an expert digital advertising copywriter for print-on-demand products.

Create ad copy for the following:
- Product: {product_type}
- Design: {design_description}
- Platform: {ad_platform}
- Tone: {tone}{audience_info}

Provide in JSON format:
1. "primary_text": Main ad copy (platform-appropriate length)
2. "headline": Attention-grabbing headline
3. "description": Short description/subheadline
4. "cta": Call-to-action text
5. "variations": 3 alternative versions of the primary text
6. "hashtags": 10 relevant hashtags (for social platforms)
7. "ad_tips": Platform-specific tips for this ad"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1500,
        )

        return {
            "product_type": product_type,
            "ad_platform": ad_platform,
            "ad_copy": response.choices[0].message.content,
        }

    def generate_campaign(
        self,
        product_type: str,
        design_description: str,
        platforms: list[str] | None = None,
    ) -> list[dict]:
        """Generate ad copy for multiple platforms at once.

        Args:
            product_type: Type of product.
            design_description: Description of the design.
            platforms: List of platforms to generate for.

        Returns:
            List of ad copy for each platform.
        """
        if platforms is None:
            platforms = ["facebook", "instagram", "pinterest", "google"]

        return [
            self.generate(product_type, design_description, platform)
            for platform in platforms
        ]
