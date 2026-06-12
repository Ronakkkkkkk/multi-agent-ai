# DataBrief - Multi-Agent AI Research Assistant

DataBrief is an AI-powered research platform that automates the process of gathering information, analyzing sources, generating reports, and evaluating report quality.

The application combines LangChain Agents, LLM Chains, Groq LLMs, Tavily Search, web scraping, and a modern Streamlit interface to deliver comprehensive research reports with minimal user input.

---

## Overview

DataBrief simulates a collaborative AI research workflow using **two specialized agents** and **two LLM chains**.

### Components

* **Search Agent** – Discovers recent and relevant information from the web.
* **Reader Agent** – Scrapes and analyzes source content for deeper insights.
* **Writer Chain** – Produces a structured research report.
* **Critic Chain** – Reviews the report and provides detailed feedback.

### Features

* Autonomous web research
* URL extraction from search results
* Intelligent webpage scraping
* Structured report generation
* Automated report evaluation
* Streamlit-based user interface
* Multi-step workflow visualization
* Source-aware report writing

---

## Architecture

```text
                    User Topic
                         │
                         ▼
              ┌─────────────────┐
              │  Search Agent   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Reader Agent   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Writer Chain   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Critic Chain   │
              └────────┬────────┘
                       │
                       ▼
                Final Report
               + AI Feedback
```

---

## Tech Stack

### Frontend

* Streamlit

### AI Framework

* LangChain
* LangChain Core
* LangChain Community

### Large Language Model

* Groq
* Llama 3.3 70B Versatile

### Search & Retrieval

* Tavily Search API

### Web Scraping

* Requests
* BeautifulSoup4
* lxml

### Utilities

* Python Dotenv
* Rich
* Pandas
* Regex (re)

---

## Project Structure

```text
DataBrief/
│
├── app.py                # Streamlit frontend
├── agents.py             # Agent and chain definitions
├── pipeline.py           # Research pipeline execution
├── tools.py              # Search and scraping tools
├── requirements.txt
├── .env
└── README.md
```

---

## How It Works

1. The user enters a research topic.
2. The Search Agent gathers recent information using Tavily Search.
3. URLs are extracted from the search results.
4. The Reader Agent selects and scrapes the most relevant source.
5. The Writer Chain combines all gathered information into a structured report.
6. The Critic Chain evaluates the report and provides constructive feedback.
7. Results are displayed in the Streamlit dashboard.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Ronakkkkkkk/multi-agent-ai.git

cd multi-agent-ai
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Running the Application

### Streamlit Dashboard

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## Running the CLI Pipeline

```bash
python pipeline.py
```

Example:

```text
Enter a research topic:
Artificial General Intelligence
```

---

## Workflow Components

| Component    | Type  | Responsibility                           |
| ------------ | ----- | ---------------------------------------- |
| Search Agent | Agent | Collects recent information from the web |
| Reader Agent | Agent | Scrapes and analyzes relevant sources    |
| Writer Chain | Chain | Generates a structured research report   |
| Critic Chain | Chain | Reviews and scores the report            |

---

## Example Output

### Search Results

```text
Title: OpenAI Releases New AI Model
URL: https://example.com/openai-model
Snippet: OpenAI announced a new model with improved reasoning and tool-use capabilities...

----

Title: AI Infrastructure Investments Surge
URL: https://example.com/ai-investment
Snippet: Major technology companies continue investing billions into AI infrastructure...
```

### Scraped Content

```text
OpenAI unveiled its latest AI model during a public announcement.

The model demonstrates stronger reasoning capabilities,
improved long-context understanding, and enhanced tool usage.

Industry analysts believe the release marks a significant step
toward more capable AI systems.
```

### Generated Report

```text
Introduction

Artificial General Intelligence (AGI) refers to highly capable AI systems that can perform a wide variety of cognitive tasks.

Key Findings

1. Major AI labs continue scaling foundation models.

2. Alignment and safety research remain critical challenges.

3. Investment in AI infrastructure continues to grow rapidly.

Conclusion

AGI research is progressing rapidly and may significantly impact multiple industries over the coming years.

Sources

https://example-source.com
```

### Critic Feedback

```text
Score: 8.5/10

Strengths:
- Well-structured report
- Good use of evidence

Areas to Improve:
- Include more quantitative analysis
- Compare opposing viewpoints

One line verdict:
A strong research report with room for deeper analysis.
```

---

## Why DataBrief?

Traditional search engines provide links.

Traditional LLMs provide answers.

DataBrief combines both approaches by:

* Researching information
* Reading source material
* Writing detailed reports
* Critiquing its own work

This creates a more transparent and reliable research workflow while demonstrating the power of collaborative AI systems.

---

## Live Demo

https://databrief.streamlit.app/

---

## Author

Ronak Sharma

GitHub:
https://github.com/Ronakkkkkkk
