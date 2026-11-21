# Multi-Agent Market Research & Report Generator with CrewAI

A Python project for researching a market topic with three specialized CrewAI agents, analyzing optional CSV metrics with Pandas, and generating Markdown and PDF reports.

## Features
- Hierarchical CrewAI orchestration with a manager LLM.
- Lead Researcher, Data Analyst, and Content Writer agents.
- Tavily web search tool.
- Pandas statistical summaries (count, mean, standard deviation, min, max).
- A4 PDF report with header and `Page X of Y` footer.
- JSON execution benchmark and routing summary.
- Automated tests with pytest.

## Requirements
- Python 3.10–3.12 recommended.
- OpenAI API key.
- Tavily API key for live web research.
- Internet connection for API-based research.

## Installation
1. Create and activate a virtual environment.
   - Windows: `python -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python -m venv .venv` then `source .venv/bin/activate`
2. Install packages: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Add your own `OPENAI_API_KEY` and `TAVILY_API_KEY` to `.env`. Never commit `.env`.

## Run
```bash
python main.py --query "Tech Sector Q3 Analysis"
```

Generated files:
- `output/market_report.md`
- `output/market_report.pdf`
- `output/benchmarks.json`

## CSV analysis
The example CSV is at `data/market_metrics.csv`. The Data Analyst agent is instructed to use it when present. Replace it with your own sourced dataset before relying on the figures. The included rows are illustrative sample data, not real company financial results.

## Tests
```bash
pytest -q
```

## GitHub submission
Create a public repository named `market-research-crewai`, then run:
```bash
git init
git add .
git commit -m "Initial project structure"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/market-research-crewai.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your GitHub username. The repository URL will then be:
`https://github.com/YOUR_USERNAME/market-research-crewai`

For the assessment's requested development history, make separate commits as you build and test the project. Do not create fake commits or claim work was completed if it was not.

## Assessment checklist
- [ ] Three agents configured under `Process.hierarchical`.
- [ ] Tavily search configured and tested with a valid API key.
- [ ] Pandas metrics validated against a real or clearly labelled dataset.
- [ ] PDF includes title, report sections, data and page numbering.
- [ ] `benchmarks.json` generated.
- [ ] `pytest` passes.
- [ ] Public GitHub repository created.
- [ ] Sample Markdown and PDF reports uploaded.
- [ ] Loom/YouTube demo recorded and link added to the submission form.

## Notes and limitations
- Live research requires valid API keys and network access.
- CrewAI APIs can change between releases; if installation reports a compatibility error, check the installed CrewAI version's documentation.
- The benchmark file records total runtime and an explicit workflow trace. Fine-grained per-agent timing can be added using CrewAI callbacks/events if required by the installed CrewAI release.
