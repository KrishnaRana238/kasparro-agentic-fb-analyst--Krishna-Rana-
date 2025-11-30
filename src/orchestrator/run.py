#!/usr/bin/env python3
import argparse, os, json, logging
from src.utils.config import load_config
from src.utils.utils import ensure_dirs, write_json, log_trace
from src.agents.planner import Planner
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import Evaluator
from src.agents.creative_generator import CreativeGenerator
import pandas as pd

logging.basicConfig(level=logging.INFO)

def main(query, config_path="config/config.yaml"):
    cfg = load_config(config_path)
    ensure_dirs(cfg["report_dir"], cfg["log_dir"])
    planner = Planner(query)
    plan = planner.plan()
    trace = {"query": query, "plan": [p.__dict__ for p in plan], "steps": []}

    # Load data
    csv = cfg["data_csv"]
    if not os.path.exists(csv):
        raise FileNotFoundError(f"CSV not found at {csv}")
    data_agent = DataAgent(csv)
    df = data_agent.load()
    summary = data_agent.summary()
    trace["steps"].append({"step":"load_and_summary", "summary": summary})

    # Insights
    insight_agent = InsightAgent(df)
    hypotheses = insight_agent.generate(top_n=12)
    trace["steps"].append({"step":"hypothesis_generation", "hypotheses": hypotheses})

    # Validate hypotheses
    evaluator = Evaluator(df, confidence_min=cfg.get("confidence_min", 0.6))
    validated = []
    for h in hypotheses:
        if h.get("type") == "ctr_drop":
            res = evaluator.validate_ctr_drop(h.get("campaign"))
            validated.append({"hypothesis":h, "validation": res})
        elif h.get("type") == "spend_drop":
            res = evaluator.validate_spend_drop()
            validated.append({"hypothesis":h, "validation": res})
        else:
            validated.append({"hypothesis":h, "validation": {"status":"not_validated"}})
    trace["steps"].append({"step":"validate_hypotheses", "results": validated})

    # Generate creatives for low CTR campaigns (campaigns with avg ctr < overall_mean * 0.75)
    campaign_ctr = df.groupby("campaign_name")["ctr"].mean()
    overall_ctr = df["ctr"].mean()
    low_ctr_campaigns = campaign_ctr[campaign_ctr < overall_ctr * 0.75].index.tolist() if not pd.isna(overall_ctr) else []
    cg = CreativeGenerator(df)
    creatives = cg.generate(target_campaigns=low_ctr_campaigns, n_per_campaign=6)
    trace["steps"].append({"step":"creative_generation", "low_ctr_campaigns": low_ctr_campaigns, "creatives_sample_count": {k: len(v) for k,v in creatives.items()}})

    # write outputs
    report_dir = cfg["report_dir"]
    write_json(validated, os.path.join(report_dir, "insights.json"))
    write_json(creatives, os.path.join(report_dir, "creatives.json"))

    # summary report.md
    report_md = []
    report_md.append(f"# Agentic Facebook Performance Analyst Report\n\n**Query:** {query}\n")
    report_md.append("## Data Summary\n")
    report_md.append(f"- Rows: {summary['rows']}\n- Date range: {summary['date_range']}\n")
    report_md.append("## Hypotheses & Validations\n")
    for v in validated:
        report_md.append("### Hypothesis\n")
        report_md.append(f"- {v['hypothesis'].get('desc')}\n")
        report_md.append("**Validation:**\n")
        report_md.append(json.dumps(v["validation"], indent=2))
        report_md.append("\n\n")
    report_md.append("## Creative Suggestions\n")
    report_md.append(json.dumps(creatives, indent=2))

    with open(os.path.join(report_dir, "report.md"), "w") as f:
        f.write("\n".join(report_md))

    # logs
    log_path = os.path.join(cfg["log_dir"], f"trace_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json")
    log_trace(trace, log_path)
    print(f"Reports written to {report_dir}. Insights + creatives generated.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="User query, e.g. 'Analyze ROAS drop in last 7 days'")
    args = parser.parse_args()
    main(args.query)
