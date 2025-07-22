# main.py
import sys
import json
from crewai import Crew, Task, Process
from dotenv import load_dotenv
from agents import get_market_analyst, get_competitor_analyst, get_strategy_advisor

# Load environment variables
load_dotenv()

def run_analysis(market_opportunity, trace_id):
    print(f"Analyzing market opportunity: {market_opportunity}")

    # Initialize agents with trace_id
    market_analyst = get_market_analyst(trace_id)
    competitor_analyst = get_competitor_analyst(trace_id)
    strategy_advisor = get_strategy_advisor(trace_id)

    # Define tasks using initialized agents
    market_task = Task(
        description=f"""Analyze the market size and expected growth rate for market of {market_opportunity}.
        1. Estimate the total market size and growth rate (CAGR). Avoid taking the overall size of the AI market and randomly assuming a percentage of that market goes towards the subsegment market; instead, search for data on the specific subsegment data directly.
        2. Estimate the total number of potential customers in the target market.
        Provide a concise report with clear data points and sources.""",
        expected_output="""A detailed market analysis report including:
        1. Total market size with CAGR
        2. Total number of potential customers
        All with supporting data and sources links.""",
        agent=market_analyst,
        async_execution=False
    )

    competitor_task = Task(
        description=f"""Find the main AI startup player's for {market_opportunity}.
        1. Identify 3-4 specific AI startup competitors by name. Avoid generic players like OpenAI, Microsoft, Google, Anthropic, Hugging Face in results. Instead, focus on finding real company names of highly relevant players with bespoke competing products and focus.
        2. For each competitor, provide:
           - Company full name and website (if available)
           - Total funding and capital raised (ensure it's total funding, not just the last round).
           - Competing product offering.
           - Traction.""",
        expected_output="""A comprehensive competitor analysis including:
        1. Overview of 3-4 main AI startup competitors.
        2. For each competitor:
           - Company name and details
           - Total funding and capital raised.
           - Detailed description of competing product offering.
           - Current known traction revenue, total customer's
           - Recent significant developments.""",
        agent=competitor_analyst,
        async_execution=True
    )

    # Create the crew
    crew = Crew(
        agents=[market_analyst, competitor_analyst],
        tasks=[market_task, competitor_task],
        verbose=True,
        process=Process.hierarchical,
        manager_agent=strategy_advisor,
        planning=True,
    )

    print("Crew created, starting analysis...")
    result = crew.kickoff()
    print("Analysis completed")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the market opportunity and trace ID as arguments.")
        sys.exit(1)

    market_opportunity = sys.argv[1]
    trace_id = sys.argv[2]

    result = run_analysis(market_opportunity, trace_id)

    # Access task outputs
    market_analysis_output = result.tasks_output[0].raw
    competitor_analysis_output = result.tasks_output[1].raw

    # Prepare the final output
    output = {
        "market_analysis": market_analysis_output,
        "competitor_analysis": competitor_analysis_output,
        "trace_id": trace_id
    }

    print("Final output:", json.dumps(output, indent=2))