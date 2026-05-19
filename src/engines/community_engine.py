"""Community Engagement Engine.

Generates discussion-driven content that builds community and drives engagement
WITHOUT requiring deep anime knowledge from the brand owner.
"""

import json
from datetime import datetime

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


class CommunityEngine:
    """Generate community engagement content for anime audiences.

    Designed for brand owners who may not be anime experts — the AI handles
    the cultural knowledge while generating authentic-feeling content.
    """

    def __init__(self, ai_client: AIClient | None = None):
        self.ai = ai_client or AIClient()
        self.profile = load_business_profile()

    def generate_discussion_posts(self, count: int = 10) -> list[dict]:
        """Generate "which anime is GOAT?" style discussion posts.

        These drive massive engagement because anime fans LOVE debating.

        Args:
            count: Number of discussion prompts to generate.

        Returns:
            List of discussion posts with expected engagement strategies.
        """
        prompt = f"""You are an anime community manager who knows how to start VIRAL debates.

Generate {count} discussion posts for an anime brand's social media. These should
spark massive comment sections. Anime fans are PASSIONATE about their opinions.

Types to mix:
- "Hot take" posts that make people comment to agree/disagree
- "This or that" / "Choose one" posts
- "Unpopular opinion" posts
- "Rate my taste" posts
- "Who would win?" posts
- Nostalgia bait
- "Tell me your favorite X without telling me"

IMPORTANT: These should feel like they come from a real anime fan,
not a corporate brand. Keep it fun and slightly chaotic.

Provide JSON:
{{
    "discussion_posts": [
        {{
            "post_text": "the full post text",
            "post_type": "hot_take | this_or_that | unpopular_opinion | rate_my_taste | who_would_win | nostalgia | challenge",
            "platform": "best platform for this post",
            "expected_engagement": "why this will get comments",
            "response_strategy": "how to reply to comments to keep the thread going",
            "tie_to_product": "how to subtly connect this to your merch (optional — not every post needs this)",
            "visual_suggestion": "what image/video to pair with this",
            "hashtags": ["relevant hashtags"],
            "virality_score": "1-10"
        }}
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.9, max_tokens=3000).get(
            "discussion_posts", []
        )

    def generate_polls(self, count: int = 5) -> list[dict]:
        """Generate poll content for Twitter and Instagram Stories.

        Args:
            count: Number of polls.

        Returns:
            List of poll content.
        """
        prompt = f"""Create {count} anime-related polls for social media.

These should be IRRESISTIBLE to vote on for anime fans.
Mix fun/silly polls with ones that subtly relate to merchandise.

Provide JSON:
{{
    "polls": [
        {{
            "question": "poll question",
            "options": ["option1", "option2", "option3", "option4"],
            "platform": "twitter | instagram_story | both",
            "follow_up": "what to post after the poll ends (results commentary)",
            "product_tie_in": "optional way to tie results to merch"
        }}
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.9, max_tokens=1500).get(
            "polls", []
        )

    def generate_comment_responses(self, comment_themes: list[str]) -> list[dict]:
        """Generate response templates for common comment types.

        Args:
            comment_themes: Types of comments to respond to.

        Returns:
            Response templates.
        """
        prompt = f"""You are a witty anime brand social media manager.

Generate response templates for these types of comments on our anime merch posts:
{json.dumps(comment_themes)}

For each theme, provide 5 response variations. Tone: funny, relatable,
otaku-insider. Like a friend who runs an anime page, not a brand.

Provide JSON:
{{
    "response_templates": [
        {{
            "comment_theme": "theme",
            "responses": [
                "response 1",
                "response 2",
                "response 3",
                "response 4",
                "response 5"
            ],
            "tone": "witty | wholesome | chaotic | supportive"
        }}
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.9, max_tokens=2000).get(
            "response_templates", []
        )

    def generate_ugc_campaigns(self, count: int = 3) -> list[dict]:
        """Generate user-generated content campaign ideas.

        UGC is the most powerful free marketing tool. Get fans to create
        content featuring your shirts.

        Args:
            count: Number of campaign ideas.

        Returns:
            UGC campaign strategies.
        """
        prompt = f"""Create {count} user-generated content campaigns for an anime t-shirt brand.

These campaigns should encourage fans to post photos/videos wearing the shirts
or engaging with the brand in creative ways. Budget: $0.

Provide JSON:
{{
    "ugc_campaigns": [
        {{
            "campaign_name": "catchy campaign name",
            "campaign_hashtag": "#CampaignHashtag",
            "concept": "what fans do",
            "launch_post": "the post that kicks off the campaign",
            "incentive": "what fans get (feature on page, shoutout, etc. — NO paid prizes)",
            "duration": "how long the campaign runs",
            "platform": "best platform for this campaign",
            "expected_content": "what kind of UGC this generates",
            "amplification_strategy": "how to maximize the campaign's reach"
        }}
    ]
}}"""

        return self.ai.generate_json(prompt, temperature=0.85, max_tokens=2000).get(
            "ugc_campaigns", []
        )

    def get_anime_knowledge_cheatsheet(self, topic: str) -> dict:
        """Generate a quick knowledge cheatsheet about an anime topic.

        This is for when you need to respond to comments or create content
        about an anime you haven't watched.

        Args:
            topic: Anime title or topic to learn about quickly.

        Returns:
            Quick reference guide.
        """
        prompt = f"""Create a quick cheatsheet about "{topic}" for someone who
hasn't watched it but needs to sound knowledgeable in social media comments.

Provide JSON:
{{
    "topic": "{topic}",
    "one_sentence_summary": "what it's about in one sentence",
    "key_characters": [
        {{"name": "char name", "nickname": "fan nickname", "known_for": "why fans love them"}}
    ],
    "iconic_quotes": ["5 most famous quotes fans reference"],
    "fan_inside_jokes": ["5 inside jokes/memes the community uses"],
    "common_debates": ["3 common debates/arguments in the fandom"],
    "do_say": ["5 things that show you 'get it'"],
    "dont_say": ["5 things that would expose you as not a real fan"],
    "related_anime": ["similar anime fans of this also like"],
    "merchandise_angle": "what type of merch fans of this anime buy most"
}}"""

        return self.ai.generate_json(prompt, temperature=0.7, max_tokens=2000)
