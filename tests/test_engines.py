"""Tests for OtakuPrint Marketing Engine modules."""

import pytest
from unittest.mock import patch, MagicMock

from src.utils.ai_client import AIClient
from src.utils.config_loader import load_business_profile


class TestConfigLoader:
    def test_load_business_profile(self):
        profile = load_business_profile()
        assert "business" in profile
        assert "target_audience" in profile
        assert "niche" in profile
        assert profile["product"]["type"] == "t-shirt"
        assert profile["marketing"]["budget"] == 0

    def test_profile_has_social_platforms(self):
        profile = load_business_profile()
        platforms = profile["social_media"]["platforms"]
        assert "instagram" in platforms
        assert "tiktok" in platforms
        assert "pinterest" in platforms
        assert "twitter" in platforms


class TestAIClient:
    def test_init_with_params(self):
        client = AIClient(api_key="test-key", model="gpt-3.5-turbo")
        assert client.api_key == "test-key"
        assert client.model == "gpt-3.5-turbo"

    def test_init_defaults(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "env-key"}):
            client = AIClient()
            assert client.api_key == "env-key"

    @patch("openai.OpenAI")
    def test_generate(self, mock_openai_cls):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "test response"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_cls.return_value = mock_client

        ai = AIClient(api_key="test-key")
        ai._client = mock_client
        result = ai.generate("test prompt")
        assert result == "test response"

    def test_generate_json(self):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"key": "value"}'

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        ai = AIClient(api_key="test-key")
        ai._client = mock_client
        result = ai.generate_json("test prompt")
        assert result == {"key": "value"}


class TestTrendIntelligence:
    @patch("src.engines.trend_intelligence.requests.Session")
    def test_get_top_airing_anime(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "title": "Test Anime",
                    "title_japanese": "テストアニメ",
                    "score": 8.5,
                    "members": 100000,
                    "synopsis": "A test anime.",
                    "genres": [{"name": "Action"}],
                    "themes": [{"name": "School"}],
                    "url": "https://example.com",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_cls.return_value = mock_session

        from src.engines.trend_intelligence import AnimeTrendIntelligence

        engine = AnimeTrendIntelligence(ai_client=AIClient(api_key="test"))
        result = engine.get_top_airing_anime(1)

        assert len(result) == 1
        assert result[0]["title"] == "Test Anime"
        assert result[0]["genres"] == ["Action"]


class TestEngineImports:
    """Verify all engines can be imported without errors."""

    def test_import_trend_intelligence(self):
        from src.engines.trend_intelligence import AnimeTrendIntelligence
        assert AnimeTrendIntelligence is not None

    def test_import_design_brief_generator(self):
        from src.engines.design_brief_generator import DesignBriefGenerator
        assert DesignBriefGenerator is not None

    def test_import_printify_seo(self):
        from src.engines.printify_seo import PrintifySEOEngine
        assert PrintifySEOEngine is not None

    def test_import_social_media_engine(self):
        from src.engines.social_media_engine import SocialMediaEngine
        assert SocialMediaEngine is not None

    def test_import_community_engine(self):
        from src.engines.community_engine import CommunityEngine
        assert CommunityEngine is not None

    def test_import_content_calendar(self):
        from src.engines.content_calendar import ContentCalendar
        assert ContentCalendar is not None

    def test_import_hashtag_research(self):
        from src.engines.hashtag_research import HashtagResearch
        assert HashtagResearch is not None
