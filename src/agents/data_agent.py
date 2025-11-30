import pandas as pd
from typing import Dict
import numpy as np

class DataAgent:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load(self, nrows=None):
        self.df = pd.read_csv(self.csv_path, parse_dates=["date"], dayfirst=False)
        if nrows:
            self.df = self.df.head(nrows)
        expected = ["campaign_name","adset_name","date","spend","impressions","clicks","ctr","purchases","revenue","roas","creative_type","creative_message","audience_type","platform","country"]
        for c in expected:
            if c not in self.df.columns:
                self.df[c] = np.nan
        # normalize CTR strings like "4.5%" to float 0.045
        if self.df["ctr"].dtype == object:
            self.df["ctr"] = self.df["ctr"].astype(str).str.replace("%","").replace("", "nan")
            self.df["ctr"] = pd.to_numeric(self.df["ctr"], errors="coerce")/100.0
        return self.df

    def summary(self) -> Dict:
        df = self.df
        out = {}
        out["rows"] = int(len(df))
        out["date_range"] = {"min": str(df["date"].min()), "max": str(df["date"].max())}
        out["metrics"] = {
            "total_spend": float(df["spend"].sum()),
            "total_revenue": float(df["revenue"].sum()),
            "avg_roas": float(df["roas"].dropna().mean()) if not df["roas"].dropna().empty else None,
            "avg_ctr": float(df["ctr"].dropna().mean()) if not df["ctr"].dropna().empty else None
        }
        out["top_spend_campaigns"] = df.groupby("campaign_name")["spend"].sum().sort_values(ascending=False).head(5).to_dict()
        out["low_roas_campaigns"] = df.groupby("campaign_name")["roas"].mean().sort_values().head(5).to_dict()
        return out

    def rolling_trends(self, metric="roas", window=7):
        df = self.df.sort_values("date")
        series = df.groupby("date")[metric].mean().rolling(window=window, min_periods=1).mean()
        return series.reset_index().rename(columns={metric: f"{metric}_rolling"})
