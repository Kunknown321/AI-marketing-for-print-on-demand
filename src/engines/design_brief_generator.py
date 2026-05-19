"""Typography Design Brief Generator.

Turns trending topics and data into actionable design briefs
with exact text, AI image prompts, and mockup directions.
"""

import json
from datetime import datetime
from pathlib import Path

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output" / "designs"


class DesignBriefGenerator:
    """Generate ready-to-create typography design briefs from trend data."""

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def generate_briefs_from_trends(self, trend_report: dict, count: int = 10) -> list[dict]:
        """Generate design briefs from a trend intelligence report.

        Args:
            trend_report: Output from AnimeTrendIntelligence.analyze_trends().
            count: Number of briefs to generate.

        Returns:
            List of complete design briefs.
        """
        prompt = f"""You are an expert print-on-demand typography designer specializing in anime culture.

Based on this trend data:
{json.dumps(trend_report, indent=2)[:3000]}

Generate {count} COMPLETE typography t-shirt design briefs. Each brief must be
immediately actionable — a designer (or AI image generator) should be able to
create the design from this brief alone.

IMPORTANT: These are TYPOGRAPHY designs. Focus on text, fonts, and layout — not illustrations.
Make designs that resonate with hardcore otaku in their 20s.

Provide JSON:
{{
    "briefs": [
        {{
            "brief_id": "BRIEF-001",
            "design_name": "catchy internal name",
            "primary_text": "the main text on the shirt",
            "secondary_text": "optional subtitle or subtext",
            "japanese_text": "Japanese characters if applicable",
            "font_style": "describe the ideal font (e.g., 'bold sans-serif with distressed edges')",
            "layout": "describe text arrangement (e.g., 'centered stack, large primary with small subtitle below')",
            "color_scheme": {{
                "text_colors": ["#hex1", "#hex2"],
                "recommended_shirt_colors": ["black", "white", "navy"]
            }},
            "design_style": "japanese_english | minimalist_streetwear | bold_graphic | retro_vintage",
            "ai_image_prompt": "complete prompt to generate this design in Midjourney/DALL-E",
            "target_anime_fans": "which anime fans this appeals to",
            "trend_source": "what trend this is based on",
            "estimated_demand": "high | medium | low",
            "suggested_price": 24.99,
            "tags_for_listing": ["tag1", "tag2", "..."],
            "mockup_notes": "how this should look on a mockup photo"
        }}
    ]
}}"""

        result = self.ai.generate_json(
            prompt,
            system_prompt="You are a senior print-on-demand designer. Return valid JSON only.",
            temperature=0.8,
            max_tokens=4000,
        )

        briefs = result.get("briefs", [])
        self._save_briefs(briefs)
        return briefs

    def generate_single_brief(
        self,
        text: str,
        style: str = "minimalist_streetwear",
        anime_reference: str = "",
    ) -> dict:
        """Generate a single design brief from a text idea.

        Args:
            text: The text for the shirt.
            style: Typography style.
            anime_reference: Related anime (optional).

        Returns:
            Complete design brief.
        """
        context = f" referencing {anime_reference}" if anime_reference else ""

        prompt = f"""Create a complete typography t-shirt design brief for:
Text: "{text}"
Style: {style}{context}
Target: Anime fans in their 20s, unisex, global market

Provide JSON:
{{
    "design_name": "catchy name",
    "primary_text": "{text}",
    "secondary_text": "optional",
    "japanese_text": "Japanese translation or text if relevant",
    "font_style": "detailed font description",
    "layout": "text arrangement description",
    "color_scheme": {{
        "text_colors": ["hex colors"],
        "recommended_shirt_colors": ["colors"]
    }},
    "ai_image_prompt": "complete AI generation prompt for this typography design — flat vector style, transparent background, print-ready",
    "tags_for_listing": ["15 SEO tags"],
    "mockup_notes": "mockup styling notes"
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=1500)

    def generate_collection(self, theme: str, size: int = 5) -> list[dict]:
        """Generate a themed collection of design briefs.

        Args:
            theme: Collection theme (e.g., "shonen energy", "anime villain quotes").
            size: Number of designs in the collection.

        Returns:
            List of cohesive design briefs.
        """
        prompt = f"""Create a cohesive collection of {size} typography t-shirt designs around:
Theme: "{theme}"
Target: Anime otaku, 20s, unisex, global

The collection should feel unified — like they belong together in a store section.
Mix typography styles but keep a cohesive visual identity.

Provide JSON:
{{
    "collection_name": "name for this collection",
    "collection_description": "2-sentence description for the store",
    "designs": [
        {{
            "design_name": "name",
            "primary_text": "shirt text",
            "japanese_text": "Japanese if applicable",
            "font_style": "font description",
            "layout": "layout description",
            "color_scheme": {{"text_colors": ["#hex"], "recommended_shirt_colors": ["colors"]}},
            "ai_image_prompt": "AI generation prompt",
            "tags_for_listing": ["tags"]
        }}
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.8, max_tokens=3000)

    def _save_briefs(self, briefs: list[dict]) -> Path:
        """Save briefs to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = OUTPUT_DIR / f"briefs_{timestamp}.json"
        with open(filepath, "w") as f:
            json.dump(briefs, f, indent=2)
        return filepath
