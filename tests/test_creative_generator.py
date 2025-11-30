import pandas as pd
from src.agents.creative_generator import CreativeGenerator

def test_creative_generator_clusters_and_generates():
    data = {
        "creative_message": [
            "Buy now and save big!",
            "Limited time offer on lingerie",
            "Hot deals for cozy nights",
            "Exclusive styles just for you",
            "Save on summer lingerie sale"
        ]
    }
    df = pd.DataFrame(data)
    gen = CreativeGenerator(df, random_seed=42)
    suggestions = gen._algorithmic_suggestions(n_per_cluster=2)
    assert isinstance(suggestions, dict)
    assert len(suggestions) > 0  # At least one cluster
    for cluster, recs in suggestions.items():
        assert len(recs) == 2  # n_per_cluster
        assert all(isinstance(r, str) for r in recs)  # Strings