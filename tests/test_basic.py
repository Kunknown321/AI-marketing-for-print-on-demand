"""Basic tests for AI Marketing for Print on Demand modules."""

import pytest
from unittest.mock import patch, MagicMock

from src.listing_optimizer import ListingOptimizer
from src.trend_analyzer import TrendAnalyzer
from src.ad_copy_generator import AdCopyGenerator
from src.seo_optimizer import SEOOptimizer
from src.social_media import SocialMediaGenerator


@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"test": "response"}'
    return mock_response


class TestListingOptimizer:
    def test_init_with_defaults(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            optimizer = ListingOptimizer(api_key="test-key")
            assert optimizer.api_key == "test-key"

    @patch("src.listing_optimizer.OpenAI")
    def test_optimize(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_client

        optimizer = ListingOptimizer(api_key="test-key")
        result = optimizer.optimize("t-shirt", "cool design", "etsy")

        assert result["platform"] == "etsy"
        assert result["product_type"] == "t-shirt"
        assert "optimized_listing" in result


class TestTrendAnalyzer:
    @patch("src.trend_analyzer.OpenAI")
    def test_analyze_niche(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_client

        analyzer = TrendAnalyzer(api_key="test-key")
        result = analyzer.analyze_niche("cat lovers")

        assert result["niche"] == "cat lovers"
        assert "analysis" in result


class TestAdCopyGenerator:
    @patch("src.ad_copy_generator.OpenAI")
    def test_generate(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_client

        generator = AdCopyGenerator(api_key="test-key")
        result = generator.generate("hoodie", "funny design", "facebook")

        assert result["product_type"] == "hoodie"
        assert result["ad_platform"] == "facebook"
        assert "ad_copy" in result


class TestSEOOptimizer:
    @patch("src.seo_optimizer.OpenAI")
    def test_research_keywords(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_client

        seo = SEOOptimizer(api_key="test-key")
        result = seo.research_keywords("dog lovers")

        assert result["niche"] == "dog lovers"
        assert "keywords" in result


class TestSocialMediaGenerator:
    @patch("src.social_media.OpenAI")
    def test_generate_post(self, mock_openai_cls, mock_openai_response):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai_cls.return_value = mock_client

        social = SocialMediaGenerator(api_key="test-key")
        result = social.generate_post("mug", "floral design")

        assert result["platform"] == "instagram"
        assert "content" in result
