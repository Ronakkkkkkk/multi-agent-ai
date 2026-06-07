from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import re

load_dotenv()

# ── Model setup ───────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ── Agent 1 · Search ──────────────────────────────────────────────────────────
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# ── Agent 2 · Reader ──────────────────────────────────────────────────────────
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# ── Helper: extract real URLs from raw text ───────────────────────────────────
def extract_urls(text: str) -> list[str]:
    """Pull every http/https URL that actually appears in the research text."""
    return re.findall(r'https?://[^\s\)\]\,\"\'<>]+', text)

# ── Writer chain ──────────────────────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

URLs found in the research (may be empty):
{urls}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources: list ONLY the URLs provided above under "URLs found in the research".
  If that list is empty, write "Sources: No URLs were available in the research data."
  Do NOT invent, guess, or add any URLs or publication names that are not in that list.

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ── Critic chain ──────────────────────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()