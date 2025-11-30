# Kasparro Agentic Facebook Analyst — <Krishna Rana>

## **Quick Start**

1. Clone the repo:

```bash
git clone https://github.com/<KrishnaRana238>/kasparro-agentic-fb-analyst-<Krishna-Rana>.git
cd kasparro-agentic-fb-analyst-<Krishna_Rana>
```

2. Set up environment:

```bash
python -V  # should be >= 3.10
python -m venv .venv && source .venv/bin/activate  # win: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Run analysis:

```bash
python src/run.py "Analyze ROAS drop in last 7 days"
```

## Data
- Place the full CSV locally and set `DATA_CSV=/path/to/synthetic_fb_ads_undergarments.csv`
- Or copy a small sample to `data/sample_fb_ads.csv`.
- See `data/README.md` for details.

## Config
Edit `config/config.yaml`:
```yaml
python: "3.10"
random_seed: 42
confidence_min: 0.6
use_sample_data: true
```

## Repo Map
- `src/agents/` — planner.py, data_agent.py, insight_agent.py, evaluator.py, creative_generator.py
- `prompts/` — *.md prompt files with variable placeholders
- `reports/` — report.md, insights.json, creatives.json
- `logs/` — json traces
- `tests/` — test_evaluator.py, test_planner.py, test_creative_generator.py

## Run
```bash
make run  # or: python src/run.py "Analyze ROAS drop"
```

## Outputs
- `reports/report.md`
- `reports/insights.json`
- `reports/creatives.json`

## Observability
- Include Langfuse screenshots or JSON logs in `reports/observability/`.

## Release
- Tag: `v1.0` and paste link here.

## Self-Review
- Link to PR describing design choices & tradeoffs.