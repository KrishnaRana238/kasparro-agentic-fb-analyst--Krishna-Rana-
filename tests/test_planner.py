from src.agents.planner import Planner

def test_planner_generates_subtasks():
    query = "Analyze ROAS drop last 7 days"
    planner = Planner(query)
    plan = planner.plan()

    assert len(plan) >= 5
    ids = [p.id for p in plan]

    expected = {
        "load_and_summary",
        "trend_analysis",
        "segment_analysis",
        "hypothesis_generation",
        "validate_hypotheses",
        "creative_generation",
        "assemble_report"
    }

    assert expected.issubset(set(ids))
