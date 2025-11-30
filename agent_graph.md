# Multi-Agent Architecture for Facebook Ads Analysis

## Overview
This multi-agent system autonomously diagnoses Facebook Ads performance by decomposing user queries into subtasks, analyzing data, generating/validating hypotheses, and recommending creatives. It uses a Planner-Evaluator loop for agentic reasoning.

## Agent Roles and Data Flow
- **Planner Agent**: Decomposes user query into subtasks (e.g., load data, analyze trends, generate hypotheses).
- **Data Agent**: Loads and summarizes the dataset (e.g., aggregates metrics, computes trends).
- **Insight Agent**: Generates hypotheses explaining patterns (e.g., CTR drops due to audience fatigue).
- **Evaluator Agent**: Validates hypotheses quantitatively (e.g., t-tests for statistical significance).
- **Creative Generator**: Produces new creative ideas for low-CTR campaigns, grounded in existing data.

## Data Flow Diagram
```
graph TD
    A[User Query] --> B[Planner Agent]
    B --> C[Data Agent: Load & Summarize CSV]
    C --> D[Insight Agent: Generate Hypotheses]
    D --> E[Evaluator Agent: Validate Hypotheses]
    E --> F[Creative Generator: Recommend Creatives]
    F --> G[Assemble Report & Outputs]
    G --> H[insights.json, creatives.json, report.md]
```

## Key Features
- **Agentic Loop**: Planner drives subtasks; Evaluator provides feedback/reflection for low-confidence results.
- **Prompt Design**: Structured prompts with Think → Analyze → Conclude, JSON schemas, and data summaries.
- **Validation**: Quantitative checks (e.g., p-values, confidence scores) ensure grounded insights.
- **Creatives**: Data-driven recommendations using clustering and n-gram recombination.

