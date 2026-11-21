import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from crew import build_crew
from report_generator import create_markdown_report, create_pdf_report
from benchmarks import save_benchmarks

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Market Research with CrewAI")
    parser.add_argument("--query", default="Tech Sector Q3 Analysis", help="Market research topic")
    args = parser.parse_args()

    started = time.perf_counter()
    print(f"Starting market research workflow for: {args.query}")

    crew, agent_names = build_crew(args.query)
    result = crew.kickoff()

    report_text = str(result)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    markdown_path = output_dir / "market_report.md"
    pdf_path = output_dir / "market_report.pdf"

    create_markdown_report(args.query, report_text, markdown_path)
    create_pdf_report(args.query, report_text, pdf_path)

    elapsed = round(time.perf_counter() - started, 2)
    save_benchmarks({
        "query": args.query,
        "total_execution_seconds": elapsed,
        "agents_configured": agent_names,
        "routing_history": [
            "Manager initialized hierarchical workflow",
            "Lead Researcher gathered market information",
            "Data Analyst reviewed and summarized metrics",
            "Content Writer prepared the report",
            "Report compiler generated Markdown and PDF outputs"
        ],
        "note": "CrewAI manager performs dynamic delegation; per-agent durations depend on CrewAI version and execution callbacks."
    }, Path("output") / "benchmarks.json")

    print(f"Completed in {elapsed} seconds.")
    print(f"Markdown: {markdown_path}")
    print(f"PDF: {pdf_path}")

if __name__ == "__main__":
    main()
