# Claude Instructions for Daily Finance Routine

This repository stores automated daily financial news reports.

## Main task

Generate one markdown report per run and save it to:

outputs/daily-finance/YYYY-MM-DD-financial-news-report.md

Use Australia/Sydney time. The report date should be the previous calendar day.

## Important rules

- Use the report template in templates/daily-financial-report-template.md.
- Keep each report around one page.
- Include source links where possible.
- Do not provide personalised financial advice.
- Do not invent financial data.
- If data is unavailable, clearly state that it is unavailable.
- Save only the final report file.
- Do not create unnecessary files.
- Do not overwrite old reports unless fixing an error in the same report date.

## Suggested public sources

Use reliable public financial sources where accessible, such as:
- Reuters business and markets coverage
- Yahoo Finance / market data pages
- MarketWatch
- CNBC Markets
- Federal Reserve official releases
- Reserve Bank of Australia releases
- ASX market information
- Major exchange/index pages
- Commodity market pages for gold, oil, and iron ore

Prioritise market-moving information over general news.
