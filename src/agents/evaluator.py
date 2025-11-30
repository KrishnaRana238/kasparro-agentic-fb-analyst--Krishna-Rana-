import scipy.stats as stats
import numpy as np
import pandas as pd

class Evaluator:
    """
    Quantitatively validate candidate hypotheses.
    """
    def __init__(self, df: pd.DataFrame, confidence_min=0.6):
        self.df = df
        self.confidence_min = confidence_min

    def validate_ctr_drop(self, campaign_name, days_recent=7, days_prev=21):
        df = self.df
        max_date = df["date"].max()
        recent = df[(df["campaign_name"]==campaign_name) & (df["date"] > max_date - pd.Timedelta(days=days_recent))]
        prev = df[(df["campaign_name"]==campaign_name) & (df["date"] <= max_date - pd.Timedelta(days=days_recent)) & (df["date"] > max_date - pd.Timedelta(days=days_recent+days_prev))]
        if len(recent) < 3 or len(prev) < 3:
            return {"campaign":campaign_name, "status":"insufficient_data", "confidence":0.0}
        try:
            stat, p = stats.ttest_ind(prev["ctr"].dropna(), recent["ctr"].dropna(), equal_var=False)
        except Exception:
            p = 1.0
        mean_prev = float(prev["ctr"].mean())
        mean_recent = float(recent["ctr"].mean())
        drop = (mean_prev - mean_recent) / mean_prev if mean_prev else 0.0
        confidence = float(max(0.0, min(1.0, 1 - p)))
        return {"campaign":campaign_name, "p_value":float(p), "drop_pct":float(drop), "mean_prev":mean_prev, "mean_recent":mean_recent, "confidence":confidence, "validated": confidence >= self.confidence_min}

    def validate_spend_drop(self, days_recent=7, days_prev=21):
        df = self.df
        max_date = df["date"].max()
        spend_daily = df.groupby("date")["spend"].sum().reset_index()
        last = spend_daily[spend_daily["date"] > max_date - pd.Timedelta(days=days_recent)]
        prev = spend_daily[(spend_daily["date"] <= max_date - pd.Timedelta(days=days_recent)) & (spend_daily["date"] > max_date - pd.Timedelta(days=days_recent+days_prev))]
        if len(last) < 3 or len(prev) < 3:
            return {"status":"insufficient_data", "confidence":0.0}
        try:
            stat, p = stats.ttest_ind(prev["spend"], last["spend"], equal_var=False)
        except Exception:
            p = 1.0
        mean_prev = float(prev["spend"].mean())
        mean_recent = float(last["spend"].mean())
        drop = (mean_prev - mean_recent)/mean_prev if mean_prev else 0.0
        confidence = float(max(0.0, min(1.0, 1 - p)))
        return {"p_value":float(p), "drop_pct":float(drop), "mean_prev":mean_prev, "mean_recent":mean_recent, "confidence":confidence, "validated": confidence >= self.confidence_min}
