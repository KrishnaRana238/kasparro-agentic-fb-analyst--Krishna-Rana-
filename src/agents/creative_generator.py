from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import numpy as np
import random
import re
from typing import List, Dict

class CreativeGenerator:
    """
    Rule-based creative generator:
    - cluster existing creative messages
    - extract frequent n-grams
    - recombine to produce headline + CTA variants
    """
    def __init__(self, df, random_seed=42):
        self.df = df
        random.seed(random_seed)

    def preprocess(self, text):
        txt = str(text).lower()
        txt = re.sub(r"[^a-z0-9\s]", "", txt)
        return txt

    def _algorithmic_suggestions(self, n_per_cluster=4):
        df = self.df.copy()
        df["msg_clean"] = df["creative_message"].fillna("").apply(self.preprocess)
        msgs = [m for m in df["msg_clean"].unique().tolist() if m.strip()]
        if not msgs:
            return {}
        vec = CountVectorizer(ngram_range=(1,2), min_df=1)
        X = vec.fit_transform(msgs)
        k = min(6, max(2, len(msgs)//5))
        if X.shape[0] < k:
            k = max(1, X.shape[0])
        km = KMeans(n_clusters=k, random_state=0).fit(X)
        labels = km.labels_
        clusters = {}
        for lbl, m in zip(labels, msgs):
            clusters.setdefault(lbl, []).append(m)
        suggestions = {}
        for c, members in clusters.items():
            token_counts = {}
            for m in members:
                for token in m.split():
                    token_counts[token] = token_counts.get(token, 0) + 1
            top_tokens = sorted(token_counts.items(), key=lambda x:-x[1])[:8]
            tokens = [t for t,_ in top_tokens]
            suggestions[f"cluster_{c}"] = []
            for i in range(n_per_cluster):
                if tokens:
                    headline = " ".join(random.sample(tokens, min(3, len(tokens))))
                    cta = random.choice(["Shop now", "Limited stock", "Grab yours", "Buy today", "See more"])
                    variant = f"{headline.title()} — {cta}!"
                else:
                    variant = random.choice(members).title()
                suggestions[f"cluster_{c}"].append(variant)
        return suggestions

    def generate(self, target_campaigns: List[str] = None, n_per_campaign=6) -> Dict[str, List[str]]:
        df = self.df
        alg = self._algorithmic_suggestions(n_per_cluster=6)
        if target_campaigns:
            out = {}
            for camp in target_campaigns:
                out[camp] = []
                camp_msgs = df[df["campaign_name"]==camp]["creative_message"].dropna().unique().tolist()
                # map clusters to campaigns by message overlap (preprocessed)
                camp_pre = [self.preprocess(m) for m in camp_msgs]
                for cl, members in alg.items():
                    if any(m in members for m in camp_pre):
                        out[camp].extend(alg[cl][:n_per_campaign])
                if not out[camp]:
                    # fallback sample
                    all_s = sum(list(alg.values()), [])[:n_per_campaign]
                    out[camp] = all_s
            return out
        return alg
