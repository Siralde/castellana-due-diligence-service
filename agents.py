#agents.py
import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from crewai_tools import EXASearchTool

#Portkey, fallback to direct OpenAI if not available
try:
    from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL
    PORTKEY_AVAILABLE = True
except ImportError:
    PORTKEY_AVAILABLE = False
    print("Portkey not available, falling back to direct OpenAI usage")

def get_portkey_llm(trace_id=None, span_id=None, agent_name=None):
    if PORTKEY_AVAILABLE:
        headers = createHeaders(
            provider="openai",
            api_key=os.getenv("PORTKEY_API_KEY"),
            trace_id=trace_id,
        )
        if span_id:
            headers['x-portkey-span-id'] = span_id
        if agent_name:
            headers['x-portkey-span-name'] = f'Agent: {agent_name}'

        return ChatOpenAI(
            model="gpt-4o",
            base_url=PORTKEY_GATEWAY_URL,
            default_headers=headers,
            api_key=os.getenv("t")
        )
    else:
        # Fallback to direct OpenAI usage
        return ChatOpenAI(
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )

# EXA Search tool
class CustomEXASearchTool(EXASearchTool):
    def __init__(self):
        super().__init__(
            type='neural',
            use_autoprompt=True,
            startPublishedDate='2021-10-01T00:00:00.000Z',
            endPublishedDate='2023-10-31T23:59:59.999Z',
            excludeText=[
                'OpenAI', 'Anthropic', 'Google', 'Mistral', 'Microsoft', 'Nvidia', 
                'general AI market', 'overall AI industry', 'IBM', 'Mistral'
            ],
            numResults=10
        )

exa_search_tool = CustomEXASearchTool()

# Market Size tool
def estimate_market_size(data: str) -> str:
    return f"Estimated market size based on: {data}"

market_size_tool = Tool(
    name="Market Size Estimator",
    func=estimate_market_size,
    description="Estimates market size based on provided data."
)

# CAGR calculator tool
def calculate_cagr(initial_value: float, final_value: float, num_years: int) -> float:
    cagr = (final_value / initial_value) ** (1 / num_years) - 1
    return cagr

cagr_tool = Tool(
    name="CAGR Calculator",
    func=calculate_cagr,
    description="Calculates CAGR given initial value, final value, and number of years."
)

# Agents
def create_agent(role, goal, backstory, tools, trace_id=None, agent_name=None):
    span_id = os.urandom(16).hex() if trace_id else None
    llm = get_portkey_llm(trace_id, span_id, agent_name)

    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        llm=llm,
        verbose=True,
        allow_delegation=True,
        max_iter=25,
        max_execution_time=300
    )

def get_market_analyst(trace_id=None):
    return create_agent(
        role='Market size Research Analyst',
        goal='Research and analyze the market size TAM of AI subsegment markets focusing on specialized market sizes and growth rates',
        backstory='Expert in doing research and calculating the market size TAM of specific subsegments of the AI market, and growth rates. Also search for sector-specific growth drivers. Known for providing granular market insights rather than general AI market statistics like the overall size of AI market which is irrelevant.',
        tools=[exa_search_tool, market_size_tool, cagr_tool],
        trace_id=trace_id,
        agent_name='market_analyst'
    )

def get_competitor_analyst(trace_id=None):
    return create_agent(
        role='AI Startup Intelligence Specialist',
        goal='Identify and analyze relevant AI startups within specific AI subsegment markets',
        backstory="""Expert in mapping competitive landscapes for specific AI verticals. 
        Specialized in identifying real, named emerging startups and scale-ups rather than tech giants like IBM, OpenAI, Google, META, Anthropic, HuggingFace. Known for finding verifiable information about startups' funding, technology, and market focus.""",
        tools=[exa_search_tool],
        trace_id=trace_id,
        agent_name='competitor_analyst'
    )

def get_strategy_advisor(trace_id=None):
    return create_agent(
        role='Project Manager',
        goal='Efficiently manage the crew and ensure high-quality task completion with a focus on ensuring that the results are very specific and relevant and not generic and too zoom out',
        backstory="""You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and that the results are relevant and specific to the market.""",
        tools=[],
        trace_id=trace_id,
        agent_name='strategy_advisor'
    )

__all__ = ['get_market_analyst', 'get_competitor_analyst', 'get_strategy_advisor']