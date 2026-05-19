"""Demo script showing how to use AI Marketing for Print on Demand tools."""

from src.listing_optimizer import ListingOptimizer
from src.trend_analyzer import TrendAnalyzer
from src.ad_copy_generator import AdCopyGenerator
from src.seo_optimizer import SEOOptimizer
from src.social_media import SocialMediaGenerator


def demo_listing_optimizer():
    """Demo: Optimize a product listing."""
    print("=" * 60)
    print("LISTING OPTIMIZER DEMO")
    print("=" * 60)

    optimizer = ListingOptimizer()
    result = optimizer.optimize(
        product_type="t-shirt",
        design_description="minimalist mountain landscape with sunset colors",
        target_platform="etsy",
    )
    print(result["optimized_listing"])


def demo_trend_analyzer():
    """Demo: Analyze a niche."""
    print("\n" + "=" * 60)
    print("TREND ANALYZER DEMO")
    print("=" * 60)

    analyzer = TrendAnalyzer()
    result = analyzer.analyze_niche(niche="cat lovers", platform="etsy")
    print(result["analysis"])


def demo_ad_copy():
    """Demo: Generate ad copy."""
    print("\n" + "=" * 60)
    print("AD COPY GENERATOR DEMO")
    print("=" * 60)

    generator = AdCopyGenerator()
    result = generator.generate(
        product_type="hoodie",
        design_description="funny programmer humor design",
        ad_platform="facebook",
        target_audience="software developers aged 25-40",
    )
    print(result["ad_copy"])


def demo_seo():
    """Demo: SEO keyword research."""
    print("\n" + "=" * 60)
    print("SEO OPTIMIZER DEMO")
    print("=" * 60)

    seo = SEOOptimizer()
    result = seo.research_keywords(niche="dog lovers", platform="etsy")
    print(result["keywords"])


def demo_social_media():
    """Demo: Generate social media content."""
    print("\n" + "=" * 60)
    print("SOCIAL MEDIA GENERATOR DEMO")
    print("=" * 60)

    social = SocialMediaGenerator()
    result = social.generate_post(
        product_type="mug",
        design_description="inspirational quote with floral design",
        platform="instagram",
        post_type="promotional",
    )
    print(result["content"])


if __name__ == "__main__":
    print("AI Marketing for Print on Demand - Demo")
    print("Make sure to set OPENAI_API_KEY in your .env file\n")

    demo_listing_optimizer()
    demo_trend_analyzer()
    demo_ad_copy()
    demo_seo()
    demo_social_media()
