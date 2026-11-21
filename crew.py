import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from tavily import TavilyClient
from data_tools import calculate_financial_metrics

@tool("Tavily Market Search")
def tavily_market_search(query: str) -> str:
    """Search the web for current market/company information using Tavily."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not configured. Add it to your .env file."
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, search_depth="advanced", max_results=5)
        results = response.get("results", [])
        if not results:
            return "No search results found."
        return "\n\n".join(
            f"Title: {item.get('title','')}\nURL: {item.get('url','')}\nContent: {item.get('content','')}"
            for item in results
        )
    except Exception as exc:
        return f"Tavily search failed: {exc}"

def build_crew(query: str):
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    researcher = Agent(
        role="Market Research Specialist",
        goal="Find relevant, recent market information and cite source URLs.",
        backstory="You are a careful market researcher who distinguishes verified facts from estimates.",
        tools=[tavily_market_search],
        llm=model,
        verbose=True,
        allow_delegation=False
    )

    analyst = Agent(
        role="Financial Data Analyst",
        goal="Analyze available numerical market data and explain trends accurately.",
        backstory="You are a financial analyst skilled in Pandas and statistical reasoning.",
        tools=[calculate_financial_metrics],
        llm=model,
        verbose=True,
        allow_delegation=False
    )

    writer = Agent(
        role="Technical Reports Writer",
        goal="Create a clear, structured market research report from research and analysis.",
        backstory="You write professional business reports and never invent missing figures.",
        llm=model,
        verbose=True,
        allow_delegation=False
    )

    research_task = Task(
        description=(
            f"Research the topic: {query}. Use Tavily Market Search to find recent, relevant information. "
            "Cover market overview, key companies, growth drivers, risks, and source URLs. "
            "Clearly state dates and distinguish facts from estimates. Do not invent statistics."
        ),
        expected_output="Research notes with source URLs, market overview, companies, drivers and risks.",
        agent=researcher
    )

    analysis_task = Task(
        description=(
            "Analyze the numerical information found by the researcher. If a local CSV exists at "
            "data/market_metrics.csv, use the financial metrics tool on it. Otherwise explain that "
            "no structured CSV metrics were supplied and do not fabricate numerical analysis. "
            "Summarize meaningful trends and data limitations."
        ),
        expected_output="Financial analysis, statistical summary where data is available, and limitations.",
        agent=analyst,
        context=[research_task]
    )

    writing_task = Task(
        description=(
            "Write a professional market research report with: Executive Summary, Market Overview, "
            "Key Players, Financial/Metric Analysis, Growth Drivers, Risks, Conclusion, and Sources. "
            "Use the researcher and analyst outputs. Do not create unsupported facts."
        ),
        expected_output="A complete, well-structured Markdown-ready market research report.",
        agent=writer,
        context=[research_task, analysis_task]
    )

    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.hierarchical,
        manager_llm=model,
        verbose=True
    )
    return crew, ["Lead Researcher", "Data Analyst", "Content Writer"]
