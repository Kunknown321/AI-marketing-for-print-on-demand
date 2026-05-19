"""Content Calendar & Daily Workflow System.

Generates structured daily, weekly, and monthly content plans
optimized for 1-2 hours of daily work.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output" / "content"


class ContentCalendar:
    """Generate and manage content calendars for all platforms."""

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def generate_weekly_calendar(self, week_start: str | None = None) -> dict:
        """Generate a full week's content calendar across all platforms.

        Designed for 1-2 hours of daily work.

        Args:
            week_start: Start date (YYYY-MM-DD). Defaults to next Monday.

        Returns:
            7-day content calendar with specific tasks and time allocations.
        """
        if week_start is None:
            today = datetime.now()
            days_until_monday = (7 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7
            week_start = (today + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")

        prompt = f"""Create a 7-day content calendar for an anime t-shirt brand.

Constraints:
- Owner has 1-2 hours per day
- $0 budget (all organic)
- Platforms: TikTok, Instagram, Pinterest, X/Twitter
- Niche: Anime typography t-shirts
- Content style: aesthetic/clean + community discussion
- Week starting: {week_start}

Daily content quotas:
- TikTok: 1-2 videos
- Instagram: 1-2 posts (mix reels, carousels, stories)
- Pinterest: 5-10 pins
- X/Twitter: 3-5 tweets

Provide JSON:
{{
    "week_start": "{week_start}",
    "theme_of_the_week": "overarching theme",
    "days": [
        {{
            "day": "Monday",
            "date": "YYYY-MM-DD",
            "daily_theme": "theme for the day",
            "time_allocation": {{
                "content_creation": "30 min",
                "posting_and_engagement": "30 min",
                "community_interaction": "30 min"
            }},
            "tasks": [
                {{
                    "time": "9:00 AM",
                    "task": "what to do",
                    "platform": "which platform",
                    "content_type": "type",
                    "details": "specific instructions",
                    "duration": "15 min"
                }}
            ],
            "posts": [
                {{
                    "platform": "platform",
                    "time": "posting time",
                    "content_type": "reel | carousel | pin | tweet | tiktok",
                    "concept": "what to post",
                    "caption_outline": "caption direction"
                }}
            ]
        }}
    ],
    "weekly_goals": ["3 measurable goals for the week"],
    "batch_content_tip": "how to batch-create content to save time"
}}"""

        result = self.ai.generate_json(prompt, temperature=0.7, max_tokens=4000)
        self._save_calendar(result, "weekly")
        return result

    def generate_daily_workflow(self, focus: str = "balanced") -> dict:
        """Generate today's specific workflow — exactly what to do in 90 minutes.

        Args:
            focus: Focus area — "balanced", "content_heavy", "engagement_heavy", "design_day".

        Returns:
            Minute-by-minute daily workflow.
        """
        today = datetime.now().strftime("%A, %B %d")

        prompt = f"""Create a detailed 90-minute daily workflow for today ({today}).

Focus: {focus}
Brand: Anime typography t-shirts
Platforms: TikTok, Instagram, Pinterest, X/Twitter

This should be a SPECIFIC, step-by-step checklist that someone can follow
without thinking. Include exact times and actions.

Provide JSON:
{{
    "date": "{today}",
    "focus": "{focus}",
    "workflow": [
        {{
            "minute_range": "0-10",
            "task": "specific task",
            "platform": "platform or 'all'",
            "details": "exactly what to do, click, type, post",
            "tip": "pro tip for efficiency"
        }}
    ],
    "content_to_create": [
        {{
            "platform": "platform",
            "type": "content type",
            "concept": "what to create",
            "quick_caption": "ready-to-use caption"
        }}
    ],
    "engagement_checklist": [
        "Reply to comments on yesterday's posts",
        "Engage with 10 posts in anime hashtags",
        "..."
    ],
    "end_of_day_review": [
        "Check analytics on yesterday's posts",
        "Note what performed well",
        "Plan tomorrow's hero content"
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=2500)

    def generate_monthly_strategy(self, month: str | None = None) -> dict:
        """Generate a monthly content strategy.

        Args:
            month: Month name (e.g., "June 2026"). Defaults to current month.

        Returns:
            Monthly strategy with weekly themes and goals.
        """
        if month is None:
            month = datetime.now().strftime("%B %Y")

        prompt = f"""Create a monthly content strategy for {month}.

Brand: Anime typography t-shirt brand
Goal: Grow followers and drive organic sales

Provide JSON:
{{
    "month": "{month}",
    "monthly_theme": "overarching theme for the month",
    "content_pillars": [
        {{
            "pillar": "pillar name",
            "percentage": "% of content",
            "examples": ["example post ideas"]
        }}
    ],
    "weekly_themes": [
        {{
            "week": 1,
            "theme": "weekly theme",
            "focus_platform": "platform to push extra this week",
            "campaign": "any mini-campaign to run",
            "product_launches": "any new designs to drop"
        }}
    ],
    "key_dates": ["any relevant dates/events this month for anime content"],
    "growth_targets": {{
        "instagram_followers": "+X followers",
        "tiktok_followers": "+X followers",
        "pinterest_monthly_views": "+X views",
        "store_visits": "+X visits",
        "sales_target": "X sales"
    }},
    "experiments": ["2-3 new content strategies to test this month"]
}}"""

        result = self.ai.generate_json(prompt, temperature=0.7, max_tokens=2500)
        self._save_calendar(result, "monthly")
        return result

    def _save_calendar(self, calendar: dict, cal_type: str) -> Path:
        """Save calendar to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = OUTPUT_DIR / f"{cal_type}_calendar_{timestamp}.json"
        with open(filepath, "w") as f:
            json.dump(calendar, f, indent=2)
        return filepath
