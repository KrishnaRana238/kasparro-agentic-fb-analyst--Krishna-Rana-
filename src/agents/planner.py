from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Subtask:
    id: str
    desc: str
    params: Dict

class Planner:
    def __init__(self, query: str):
        self.query = query

    def plan(self) -> List[Subtask]:
        subtasks = [
            Subtask(id="load_and_summary", desc="Load CSV and compute aggregate summaries", params={}),
            Subtask(id="trend_analysis", desc="Analyze ROAS / CTR / Spend trends over time", params={"window":7}),
            Subtask(id="segment_analysis", desc="Segment-level analysis: by campaign/adset/audience/creative_type", params={}),
            Subtask(id="hypothesis_generation", desc="Generate hypotheses for observed changes", params={}),
            Subtask(id="validate_hypotheses", desc="Run statistical checks and compute confidence", params={}),
            Subtask(id="creative_generation", desc="Generate new creative messages for low-CTR campaigns", params={}),
            Subtask(id="assemble_report", desc="Write final report and artifacts", params={})
        ]
        return subtasks
