import pandas as pd
from src.agents.evaluator import Evaluator

def test_evaluator_on_small_sample():
    data = {
        "date": pd.to_datetime(["2025-11-01","2025-11-02","2025-11-03","2025-11-04","2025-11-05","2025-11-06","2025-11-07","2025-11-08"]),
        "campaign_name": ["A"]*8,
        "ctr": [0.05,0.05,0.04,0.035,0.03,0.025,0.02,0.018],
        "spend": [100,110,90,95,60,50,45,40],
    }
    df = pd.DataFrame(data)
    ev = Evaluator(df, confidence_min=0.5)
    res = ev.validate_ctr_drop("A", days_recent=3, days_prev=5)
    assert "confidence" in res
