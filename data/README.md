# Dataset Description

## Overview
This synthetic eCommerce + Facebook Ads dataset simulates real ad performance data for analysis. It includes quantitative metrics and creative messaging to diagnose ROAS fluctuations and generate recommendations.

## Columns
- `campaign_name`: Name of the Facebook ad campaign (string).
- `adset_name`: Name of the ad set within the campaign (string).
- `date`: Date of the ad performance data (YYYY-MM-DD format).
- `spend`: Amount spent on ads in USD (float).
- `impressions`: Number of times the ad was shown (int).
- `clicks`: Number of clicks on the ad (int).
- `ctr`: Click-through rate as a decimal (0-1, e.g., 0.05 for 5%).
- `purchases`: Number of purchases attributed to the ad (int).
- `revenue`: Revenue generated from purchases in USD (float).
- `roas`: Return on ad spend (revenue / spend, float).
- `creative_type`: Type of creative (e.g., "image", "video", string).
- `creative_message`: Text message in the ad (string, may include headlines/CTAs).
- `audience_type`: Target audience segment (e.g., "lookalike", "interest-based", string).
- `platform`: Platform where ad ran (e.g., "facebook", "instagram", string).
- `country`: Country of the audience (string, e.g., "US").

## Sample Rows
| campaign_name | adset_name | date       | spend | impressions | clicks | ctr  | purchases | revenue | roas | creative_type | creative_message          | audience_type | platform | country |
|---------------|------------|------------|-------|-------------|--------|------|-----------|---------|------|---------------|---------------------------|---------------|----------|---------|
| Summer Sale   | Lookalike  | 2025-11-01 | 500   | 10000       | 200    | 0.02 | 10        | 1000    | 2.0  | image         | "Hot deals on lingerie!"  | lookalike     | facebook | US      |
| Winter Promo  | Interest   | 2025-11-02 | 300   | 8000        | 160    | 0.02 | 8         | 800     | 2.67 | video         | "Cozy up with new styles" | interest      | instagram| CA      |

## Preprocessing Notes
- `ctr`: May be provided as % (e.g., "4.5%"); normalized to float (0.045) in code.
- Missing values: Filled with NaN or defaults where applicable.
- Dates: Parsed as datetime for trend analysis.
- Use this for ROAS/CTR diagnostics, hypothesis validation, and creative generation.