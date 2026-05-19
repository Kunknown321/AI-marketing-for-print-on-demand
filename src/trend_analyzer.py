"""Trend analysis for print-on-demand niches using AI."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class TrendAnalyzer:
    """Analyze and identify trending niches, designs, and keywords for POD."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

    def analyze_niche(self, niche: str, platform: str = "etsy") -> dict:
        """Analyze a niche for print-on-demand potential.

        Args:
            niche: The niche to analyze (e.g., "cat lovers", "hiking").
            platform: Target marketplace.

        Returns:
            Analysis including competition level, demand, and recommendations.
        """
        prompt = f"""You are a print-on-demand market research expert.

Analyze the following niche for print-on-demand potential on {platform}:
Niche: {niche}

Provide analysis in JSON format:
1. "demand_level": estimated demand (high/medium/low)
2. "competition_level": estimated competition (high/medium/low)
3. "profitability_score": 1-10 score
4. "trending_keywords": list of 10 trending keywords in this niche
5. "design_ideas": list of 5 design concept ideas
6. "target_audience": description of the ideal customer
7. "seasonal_trends": any seasonal patterns
8. "recommendations": strategic recommendations"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )

        return {
            "niche": niche,
            "platform": platform,
            "analysis": response.choices[0].message.content,
        }

    def suggest_niches(self, interests: list[str], count: int = 5) -> dict:
        """Suggest profitable niches based on user interests.

        Args:
            interests: List of user interests or themes.
            count: Number of niche suggestions to generate.

        Returns:
            Suggested niches with potential analysis.
        """
        prompt = f"""You are a print-on-demand niche research expert.

Based on these interests: {', '.join(interests)}

Suggest {count} profitable print-on-demand niches. For each niche provide:
1. Niche name
2. Why it's profitable
3. Example design ideas (3 per niche)
4. Estimated competition level
5. Target demographic

Format as JSON."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000,
        )

        return {
            "interests": interests,
            "suggestions": response.choices[0].message.content,
        }
