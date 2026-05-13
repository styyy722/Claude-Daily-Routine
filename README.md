# Claude Daily Finance Routine

An automated daily financial news reporting system powered by Claude. Every morning the routine researches the previous day's market activity and generates bilingual reports — in English and Simplified Chinese — saved to this repository and delivered to Discord.

## How It Works

```text
Claude Scheduled Task (7:00 AM daily, Sydney time)
    ↓
Determines target date (yesterday in Australia/Sydney timezone)
    ↓
Researches previous day's financial news via public sources
    ↓
Generates English report + Chinese (Simplified) translation
    ↓
Commits and pushes both reports to GitHub
    ↓
Sends full report content to Discord (English first, then Chinese)
```

## Report Contents

Each report follows a consistent one-page structure:

- **Executive Summary** — 3 key market-moving bullet points
- **Market Snapshot** — code block table covering S&P 500, Nasdaq, Dow Jones, ASX 200, AUD/USD, US 10-year yield, gold, oil, and iron ore
- **Key Financial News** — 5–7 bullets covering global equities, rates, FX, commodities, and major company/sector news
- **Investment Implications** — 3 bullets on what the news means for markets
- **Watchlist for Today** — 3 items for investors to monitor

*Reports do not constitute personalised financial advice.*

## Output Files

Reports are saved to `outputs/daily-finance/` with the following naming convention:

| File | Description |
|---|---|
| `YYYY-MM-DD-financial-news-report.md` | English report |
| `YYYY-MM-DD-financial-news-report-zh.md` | Chinese (Simplified) report |

## Discord Delivery

Both the English and Chinese reports are sent as full-content Discord messages after each run. The Market Snapshot table uses a monospace code block format for clean rendering in Discord.

## Sources

Reports draw on publicly available financial sources including Reuters, Yahoo Finance, CNBC, MarketWatch, the Federal Reserve, the Reserve Bank of Australia, ASX market data, and commodity market pages.

## Repository Structure

```
Claude-Daily-Routine/
├── CLAUDE.md                          # Routine instructions for Claude
├── templates/
│   ├── daily-financial-report-template.md      # English report template
│   └── daily-financial-report-template-zh.md   # Chinese report template
└── outputs/
    └── daily-finance/
        ├── YYYY-MM-DD-financial-news-report.md
        └── YYYY-MM-DD-financial-news-report-zh.md
```
