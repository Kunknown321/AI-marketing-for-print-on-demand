# OtakuPrint Marketing Engine

**AI-powered, data-driven, 100% organic marketing system for anime print-on-demand.**

Built for sellers who want to build a real anime merch brand with $0 ad spend. The system handles trend research, design ideation, SEO optimization, social media content generation, and community building — even if you don't know anything about anime.

---

## What This Does

| Module | What It Does |
|--------|-------------|
| **Trend Intelligence** | Scrapes MyAnimeList, Reddit, and more to find what's trending in anime right now |
| **Design Brief Generator** | Turns trends into ready-to-create typography t-shirt design briefs with AI image prompts |
| **Printify SEO Engine** | Generates SEO-optimized titles, descriptions, and tags for your Printify listings |
| **Social Media Engine** | Creates platform-specific content for TikTok, Instagram, Pinterest, and X/Twitter |
| **Community Engine** | Generates engagement content (polls, debates, memes) that builds community without requiring anime knowledge |
| **Content Calendar** | Plans your daily, weekly, and monthly content with exact time allocations for 1-2 hours/day |
| **Hashtag Research** | Platform-specific hashtag banks and SEO keyword strategies |

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Kunknown321/AI-marketing-for-print-on-demand.git
cd AI-marketing-for-print-on-demand
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your AI API key
```

**Free API options:**
- [Groq](https://console.groq.com/) — free tier with fast inference
- [Together AI](https://www.together.ai/) — free tier available
- [Ollama](https://ollama.ai/) — run models locally for free
- [OpenAI](https://platform.openai.com/) — pay-per-use

### 3. Edit Your Business Profile

Edit `config/business_profile.yaml` with your brand details.

### 4. Run

```bash
# See the 10-day launch plan
python run.py launch

# Analyze what's trending in anime right now
python run.py trends

# Generate design briefs from trends
python run.py designs

# Generate today's social media content (all platforms)
python run.py content

# Get your 90-minute daily workflow
python run.py workflow

# Run the full daily pipeline (everything at once)
python run.py full
```

---

## All Commands

```bash
# TRENDS & RESEARCH
python run.py trends                        # Current anime trends + design opportunities
python run.py niche "shonen"                # Deep dive into a sub-niche
python run.py cheatsheet "Attack on Titan"  # Quick knowledge about an anime you haven't watched

# DESIGN
python run.py designs                       # Design briefs from current trends
python run.py designs --theme "villain quotes" --count 5  # Themed collection

# SEO
python run.py seo                           # Full store SEO strategy
python run.py seo --keyword "anime t-shirts"  # Keyword research

# CONTENT
python run.py content                       # Today's content for ALL platforms
python run.py content --platform tiktok     # Content for specific platform
python run.py community                     # Community engagement posts
python run.py polls                         # Poll content for Twitter/IG

# PLANNING
python run.py workflow                      # Today's 90-minute step-by-step plan
python run.py workflow --focus content_heavy # Focus on content creation today
python run.py calendar                      # Weekly content calendar
python run.py calendar --monthly            # Monthly strategy

# HASHTAGS
python run.py hashtags                      # Full hashtag bank for all platforms

# FULL PIPELINE
python run.py full                          # Run everything at once
```

---

## Project Structure

```
AI-marketing-for-print-on-demand/
├── run.py                          # Main CLI — run everything from here
├── config/
│   └── business_profile.yaml       # YOUR business settings (edit this!)
├── src/
│   ├── engines/
│   │   ├── trend_intelligence.py   # Anime trend scraping & analysis
│   │   ├── design_brief_generator.py  # Typography design brief creation
│   │   ├── printify_seo.py         # Printify listing SEO optimization
│   │   ├── social_media_engine.py  # TikTok, IG, Pinterest, X content
│   │   ├── community_engine.py     # Community engagement & anime cheatsheets
│   │   ├── content_calendar.py     # Daily/weekly/monthly planning
│   │   └── hashtag_research.py     # Platform-specific hashtag strategy
│   └── utils/
│       ├── ai_client.py            # Unified AI provider client
│       └── config_loader.py        # Business profile loader
├── strategies/
│   └── 10_day_launch_plan.md       # Step-by-step first sale plan
├── output/                         # Generated content saved here
│   ├── designs/                    # Design briefs
│   ├── content/                    # Social media content
│   └── seo/                        # SEO research
├── requirements.txt
├── .env.example
└── LICENSE
```

---

## The "I Don't Know Anime" Feature

The **Anime Knowledge Cheatsheet** engine is built specifically for brand owners who picked the anime niche for business reasons (smart move!) but haven't watched much anime.

```bash
# Before engaging with fans about Naruto:
python run.py cheatsheet "Naruto"
```

This gives you:
- One-sentence summary of the anime
- Key characters and their fan nicknames
- Iconic quotes fans reference constantly
- Inside jokes and memes in the community
- Things to say (and NOT say) to sound authentic
- Common debates to reference in content

---

## Daily Workflow (1-2 Hours)

The system is designed for a **90-minute daily routine**:

| Time | Task | Tool |
|------|------|------|
| 0-10 min | Check trends & plan | `python run.py trends` |
| 10-25 min | Create hero content | `python run.py content` |
| 25-40 min | Post to all platforms | Manual posting |
| 40-55 min | Engage with community | Comment, reply, interact |
| 55-70 min | Pinterest power session | Pin 5-10 pins |
| 70-80 min | Respond to comments | Reply to everything |
| 80-90 min | Plan tomorrow | `python run.py workflow` |

---

## Revenue Strategy: $0 → $10K/month

### Phase 1: Foundation (Days 1-10)
- Launch 10-15 products
- Build social presence on all 4 platforms
- Focus on Pinterest SEO (long-term traffic)
- Get first sale through community engagement

### Phase 2: Growth (Days 11-60)
- Scale to 50+ products
- Post consistently daily
- Build email list from social followers
- Start getting organic search traffic from Pinterest/Google

### Phase 3: Scale (Days 61-180)
- 100+ products across multiple sub-niches
- Established social media following
- Organic traffic driving consistent sales
- Micro-influencer collaborations
- UGC campaigns generating free content

### Phase 4: Dominance (Days 181-365)
- 200+ products
- Strong brand recognition in anime merch space
- Multiple revenue streams (shirts, hoodies, accessories)
- Community-driven product development
- $10K/month target

---

## Free Tools You'll Need

| Tool | Purpose | Link |
|------|---------|------|
| **Canva** (free) | Design mockups & social media graphics | [canva.com](https://canva.com) |
| **Printify** (free) | Print-on-demand fulfillment | [printify.com](https://printify.com) |
| **Leonardo AI** (free tier) | AI image generation for designs | [leonardo.ai](https://leonardo.ai) |
| **Groq** (free tier) | AI API for this marketing engine | [groq.com](https://groq.com) |
| **Later/Buffer** (free tier) | Social media scheduling | [later.com](https://later.com) |
| **Pinterest** | #1 free traffic source for POD | [pinterest.com](https://pinterest.com) |
| **Google Trends** | Validate trending topics | [trends.google.com](https://trends.google.com) |

---

## License

MIT License — see [LICENSE](LICENSE) for details.
