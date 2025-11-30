from typing import List, Dict
import numpy as np
import pandas as pd

class InsightAgent:
    """
    Rule-based insight generation:
    - finds CTR drops per campaign
    - finds spend drops
    - finds creative messages with low ROAS
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate(self, top_n=10) -> List[Dict]:
        hypotheses = []
        df = self.df
        if df.empty:
            return hypotheses
        max_date = df["date"].max()
        # recent 7 days vs prev 21 days window
        recent = df[df["date"] >= max_date - pd.Timedelta(days=7)]
        prev = df[(df["date"] < max_date - pd.Timedelta(days=7)) & (df["date"] >= max_date - pd.Timedelta(days=28))]

        # 1) CTR drops by campaign
        if not recent.empty and not prev.empty:
            camp_recent = recent.groupby("campaign_name")["ctr"].mean()
            camp_prev = prev.groupby("campaign_name")["ctr"].mean()
            for camp in camp_recent.index:
                r = camp_recent.get(camp, np.nan)
                p = camp_prev.get(camp, np.nan)
                if np.isnan(p) or np.isnan(r) or p == 0:
                    continue
                drop_pct = (p - r) / p
                if drop_pct > 0.12:
                    hypotheses.append({
                        "campaign": camp,
                        "type": "ctr_drop",
                        "desc": f"CTR dropped by {drop_pct:.2%} comparing last 7 days to previous 21 days",
                        "evidence": {"ctr_prev": float(p), "ctr_recent": float(r), "drop_pct": float(drop_pct)}
                    })
        # 2) Spend drops (site-wide)
        spend_daily = df.groupby("date")["spend"].sum()
        if len(spend_daily) >= 14:
            last = spend_daily.iloc[-7:].mean()
            prev_avg = spend_daily.iloc[-21:-7].mean() if len(spend_daily) >= 21 else spend_daily.iloc[:-7].mean()
            if prev_avg > 0 and (last / prev_avg) < 0.8:
                hypotheses.append({"type":"spend_drop","desc":"Daily spend dropped >20% recently","evidence":{"last_avg_spend":float(last),"prev_avg_spend":float(prev_avg)}})

        # 3) Creative underperformance by average ROAS
        if "creative_message" in df.columns:
            creative_roas = df.groupby("creative_message")["roas"].mean().sort_values()
            low_roas = creative_roas.head(5).to_dict()
            if low_roas:
                hypotheses.append({"type":"creative_underperform","desc":"Some creative messages have low average ROAS","evidence":{"low_roas_examples": low_roas}})

        # 4) Audience fatigue: high impressions but low CTR over time per audience_type
        if "audience_type" in df.columns:
            aud_trends = df.groupby(["audience_type","date"])["ctr"].mean().reset_index()
            for aud in aud_trends["audience_type"].unique():
                series = aud_trends[aud_trends["audience_type"]==aud].sort_values("date")
                if len(series) >= 14:
                    first = series["ctr"].iloc[-21:-14].mean() if len(series) >= 21 else series["ctr"].iloc[:len(series)//2].mean()
                    recent = series["ctr"].iloc[-7:].mean()
                    if not np.isnan(first) and first>0 and (recent/first) < 0.8:
                        hypotheses.append({"type":"audience_fatigue","desc":f"Audience {aud} CTR dropped >20% vs earlier period","evidence":{"audience":aud,"ctr_prev":float(first),"ctr_recent":float(recent)}})

        return hypotheses[:top_n]
