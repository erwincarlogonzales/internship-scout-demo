"""agents/searcher.py — AGENT 1: SEARCHER

Job: turn the profile's target roles into live web searches,
and collect whatever raw results come back.

Tool it uses: Tavily (web search)
"""

import os

from tavily import TavilyClient

from profile import JOB_BOARD_DOMAINS


def run(profile: dict) -> str:
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    chunks = []

    for role in profile["target_roles"]:
        query = f"{role} {profile['location_preference']} apply 2025 2026"
        print(f"  [Searcher] Searching: {query}")

        response = client.search(query=query, max_results=5, include_domains=JOB_BOARD_DOMAINS)
        for result in response.get("results", []):
            chunks.append(f"Title: {result.get('title', '')}\nURL: {result.get('url', '')}\nContent: {result.get('content', '')}")

    return "\n\n---\n\n".join(chunks)
