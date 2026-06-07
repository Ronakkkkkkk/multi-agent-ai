from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain, extract_urls

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ── Step 1 · Search agent ─────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 1 - Search agent is working ...")
    print("=" * 50)
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content
    print("\nSearch result:\n", state["search_results"])

    # ── Step 2 · Reader agent ─────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    # ✅ FIXED PART STARTS HERE
    urls = extract_urls(state["search_results"])
    top_urls = list(dict.fromkeys(urls))[:2]   # max 2 URLs, deduplicated
    urls_str = "\n".join(top_urls) if top_urls else "(no URLs found)"
    # ✅ FIXED PART ENDS HERE

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on these URLs, pick the most relevant one and scrape it for deeper content.\n\n"
            f"URLs:\n{urls_str}\n\n"
            f"Topic: {topic}"
        )]
    })

    state["scraped_content"] = reader_result["messages"][-1].content
    print("\nScraped content:\n", state["scraped_content"])

    # ── Step 3 · Writer chain ─────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    # Extract only real URLs that appear in the research text
    found_urls = extract_urls(research_combined)
    urls_str = "\n".join(found_urls) if found_urls else "(none)"

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
        "urls": urls_str,
    })
    print("\nFinal Report:\n", state["report"])

    # ── Step 4 · Critic chain ─────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report ...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic feedback:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)