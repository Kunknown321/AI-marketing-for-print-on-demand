#!/usr/bin/env python3
"""OtakuPrint Marketing Engine — Main Runner.

Usage:
    python run.py trends              # Analyze current anime trends
    python run.py designs             # Generate design briefs from trends
    python run.py designs --theme "shonen energy"  # Generate themed collection
    python run.py content             # Generate today's content for all platforms
    python run.py content --platform tiktok  # Generate content for specific platform
    python run.py workflow            # Get today's 90-minute workflow
    python run.py calendar            # Generate weekly content calendar
    python run.py calendar --monthly  # Generate monthly strategy
    python run.py seo                 # Generate store SEO strategy
    python run.py seo --keyword "anime shirts"  # Keyword research
    python run.py hashtags            # Generate full hashtag bank
    python run.py community           # Generate community engagement content
    python run.py polls               # Generate poll content
    python run.py cheatsheet "Naruto" # Get anime knowledge cheatsheet
    python run.py niche "shonen"      # Deep dive into a sub-niche
    python run.py launch              # Show the 10-day launch plan
    python run.py full                # Run EVERYTHING (full daily pipeline)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from src.engines.trend_intelligence import AnimeTrendIntelligence
from src.engines.design_brief_generator import DesignBriefGenerator
from src.engines.printify_seo import PrintifySEOEngine
from src.engines.social_media_engine import SocialMediaEngine
from src.engines.community_engine import CommunityEngine
from src.engines.content_calendar import ContentCalendar
from src.engines.hashtag_research import HashtagResearch
from src.utils.ai_client import AIClient


def print_header(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_json(data: dict | list) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def save_output(data: dict | list, name: str) -> Path:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"{name}_{timestamp}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Saved to: {filepath}")
    return filepath


def cmd_trends(args: argparse.Namespace) -> None:
    print_header("ANIME TREND INTELLIGENCE")
    engine = AnimeTrendIntelligence()

    print("Fetching top airing anime...")
    airing = engine.get_top_airing_anime(10)
    print(f"  Found {len(airing)} currently airing anime")

    print("Fetching Reddit trends...")
    reddit = engine.get_trending_reddit_posts("anime", 10)
    print(f"  Found {len(reddit)} trending Reddit posts")

    print("\nRunning AI trend analysis...")
    report = engine.analyze_trends()
    print_json(report)
    save_output(report, "trend_report")


def cmd_designs(args: argparse.Namespace) -> None:
    print_header("DESIGN BRIEF GENERATOR")
    generator = DesignBriefGenerator()

    if args.theme:
        print(f"Generating themed collection: {args.theme}")
        result = generator.generate_collection(args.theme, size=args.count)
        print_json(result)
        save_output(result, f"collection_{args.theme.replace(' ', '_')}")
    else:
        print("Fetching trends first...")
        trends = AnimeTrendIntelligence()
        report = trends.analyze_trends()

        print(f"Generating {args.count} design briefs from trends...")
        briefs = generator.generate_briefs_from_trends(report, count=args.count)
        print_json(briefs)
        save_output(briefs, "design_briefs")


def cmd_content(args: argparse.Namespace) -> None:
    print_header("SOCIAL MEDIA CONTENT ENGINE")
    engine = SocialMediaEngine()

    if args.platform:
        platform = args.platform.lower()
        print(f"Generating content for {platform}...")

        generators = {
            "tiktok": engine.generate_tiktok_content,
            "instagram": engine.generate_instagram_content,
            "pinterest": engine.generate_pinterest_content,
            "twitter": engine.generate_twitter_content,
        }

        if platform not in generators:
            print(f"Unknown platform: {platform}. Use: tiktok, instagram, pinterest, twitter")
            return

        content = generators[platform]()
        print_json(content)
        save_output(content, f"content_{platform}")
    else:
        print("Generating full day's content for all platforms...")
        content = engine.generate_daily_content()
        print_json(content)
        save_output(content, "daily_content")


def cmd_workflow(args: argparse.Namespace) -> None:
    print_header("DAILY WORKFLOW")
    calendar = ContentCalendar()
    workflow = calendar.generate_daily_workflow(focus=args.focus)
    print_json(workflow)
    save_output(workflow, "daily_workflow")


def cmd_calendar(args: argparse.Namespace) -> None:
    calendar = ContentCalendar()

    if args.monthly:
        print_header("MONTHLY CONTENT STRATEGY")
        result = calendar.generate_monthly_strategy()
    else:
        print_header("WEEKLY CONTENT CALENDAR")
        result = calendar.generate_weekly_calendar()

    print_json(result)
    save_output(result, "monthly_strategy" if args.monthly else "weekly_calendar")


def cmd_seo(args: argparse.Namespace) -> None:
    seo = PrintifySEOEngine()

    if args.keyword:
        print_header(f"KEYWORD RESEARCH: {args.keyword}")
        result = seo.keyword_research(args.keyword)
    else:
        print_header("STORE SEO STRATEGY")
        result = seo.generate_store_seo(args.store_name or "My Anime Store")

    print_json(result)
    save_output(result, "seo_research")


def cmd_hashtags(args: argparse.Namespace) -> None:
    print_header("HASHTAG RESEARCH")
    research = HashtagResearch()
    bank = research.generate_hashtag_bank()
    print_json(bank)
    save_output(bank, "hashtag_bank")


def cmd_community(args: argparse.Namespace) -> None:
    print_header("COMMUNITY ENGAGEMENT CONTENT")
    engine = CommunityEngine()
    posts = engine.generate_discussion_posts(count=args.count)
    print_json(posts)
    save_output(posts, "community_posts")


def cmd_polls(args: argparse.Namespace) -> None:
    print_header("POLL CONTENT")
    engine = CommunityEngine()
    polls = engine.generate_polls(count=args.count)
    print_json(polls)
    save_output(polls, "polls")


def cmd_cheatsheet(args: argparse.Namespace) -> None:
    print_header(f"ANIME CHEATSHEET: {args.anime}")
    engine = CommunityEngine()
    cheatsheet = engine.get_anime_knowledge_cheatsheet(args.anime)
    print_json(cheatsheet)
    save_output(cheatsheet, f"cheatsheet_{args.anime.replace(' ', '_')}")


def cmd_niche(args: argparse.Namespace) -> None:
    print_header(f"NICHE DEEP DIVE: {args.niche}")
    engine = AnimeTrendIntelligence()
    analysis = engine.discover_niche_opportunities(args.niche)
    print_json(analysis)
    save_output(analysis, f"niche_{args.niche.replace(' ', '_')}")


def cmd_launch(args: argparse.Namespace) -> None:
    print_header("10-DAY LAUNCH PLAN")
    plan_path = Path(__file__).parent / "strategies" / "10_day_launch_plan.md"
    print(plan_path.read_text())


def cmd_full(args: argparse.Namespace) -> None:
    print_header("FULL DAILY PIPELINE")
    print("Running complete marketing pipeline...\n")

    # 1. Trends
    print("Step 1/6: Analyzing trends...")
    trends_engine = AnimeTrendIntelligence()
    trends = trends_engine.analyze_trends()
    save_output(trends, "trend_report")
    print("  Done.")

    # 2. Design briefs
    print("Step 2/6: Generating design briefs...")
    design_engine = DesignBriefGenerator()
    briefs = design_engine.generate_briefs_from_trends(trends, count=5)
    save_output(briefs, "design_briefs")
    print("  Done.")

    # 3. SEO optimization
    print("Step 3/6: Optimizing listings for SEO...")
    seo_engine = PrintifySEOEngine()
    listings = seo_engine.bulk_optimize(briefs[:3])
    save_output(listings, "seo_listings")
    print("  Done.")

    # 4. Social media content
    print("Step 4/6: Generating social media content...")
    social_engine = SocialMediaEngine()
    content = social_engine.generate_daily_content()
    save_output(content, "daily_content")
    print("  Done.")

    # 5. Community content
    print("Step 5/6: Generating community engagement content...")
    community_engine = CommunityEngine()
    discussions = community_engine.generate_discussion_posts(count=5)
    save_output(discussions, "community_posts")
    print("  Done.")

    # 6. Daily workflow
    print("Step 6/6: Generating today's workflow...")
    calendar = ContentCalendar()
    workflow = calendar.generate_daily_workflow()
    save_output(workflow, "daily_workflow")
    print("  Done.")

    print_header("PIPELINE COMPLETE")
    print("All outputs saved to the output/ directory.")
    print("Run 'python run.py workflow' to see today's step-by-step plan.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OtakuPrint Marketing Engine — AI-powered anime POD marketing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # trends
    subparsers.add_parser("trends", help="Analyze current anime trends")

    # designs
    p_designs = subparsers.add_parser("designs", help="Generate design briefs")
    p_designs.add_argument("--theme", help="Theme for a collection")
    p_designs.add_argument("--count", type=int, default=10, help="Number of briefs")

    # content
    p_content = subparsers.add_parser("content", help="Generate social media content")
    p_content.add_argument("--platform", help="Specific platform")

    # workflow
    p_workflow = subparsers.add_parser("workflow", help="Get today's 90-min workflow")
    p_workflow.add_argument("--focus", default="balanced",
                           choices=["balanced", "content_heavy", "engagement_heavy", "design_day"])

    # calendar
    p_calendar = subparsers.add_parser("calendar", help="Generate content calendar")
    p_calendar.add_argument("--monthly", action="store_true", help="Monthly instead of weekly")

    # seo
    p_seo = subparsers.add_parser("seo", help="SEO strategy and keyword research")
    p_seo.add_argument("--keyword", help="Keyword to research")
    p_seo.add_argument("--store-name", help="Store name for store SEO")

    # hashtags
    subparsers.add_parser("hashtags", help="Generate hashtag bank")

    # community
    p_community = subparsers.add_parser("community", help="Community engagement content")
    p_community.add_argument("--count", type=int, default=10)

    # polls
    p_polls = subparsers.add_parser("polls", help="Generate poll content")
    p_polls.add_argument("--count", type=int, default=5)

    # cheatsheet
    p_cheatsheet = subparsers.add_parser("cheatsheet", help="Anime knowledge cheatsheet")
    p_cheatsheet.add_argument("anime", help="Anime title to learn about")

    # niche
    p_niche = subparsers.add_parser("niche", help="Deep dive into a sub-niche")
    p_niche.add_argument("niche", help="Sub-niche to explore")

    # launch
    subparsers.add_parser("launch", help="Show the 10-day launch plan")

    # full
    subparsers.add_parser("full", help="Run full daily pipeline")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    commands = {
        "trends": cmd_trends,
        "designs": cmd_designs,
        "content": cmd_content,
        "workflow": cmd_workflow,
        "calendar": cmd_calendar,
        "seo": cmd_seo,
        "hashtags": cmd_hashtags,
        "community": cmd_community,
        "polls": cmd_polls,
        "cheatsheet": cmd_cheatsheet,
        "niche": cmd_niche,
        "launch": cmd_launch,
        "full": cmd_full,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
