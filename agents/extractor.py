"""agents/extractor.py — AGENT 2: EXTRACTOR / SCORER

Job: read the messy raw search results and pull out only the REAL
listings, each scored against the profile ("why it fits you").

Tool it uses: Claude (reads, filters, reasons)
"""

import json
import os

import anthropic

PROMPT = """\
You're helping {name}, a {major} student, find real internships.

Looking for: {target_roles}
Skills: {skills} | Interests: {interests} | Location: {location_preference}

Go through these raw search results and:
1. Only include a listing if the text contains a URL pointing directly to THAT SPECIFIC posting
   (e.g. a /jobs/view/... or posting-detail link) — never a generic search-results, category,
   or company-listing page, and never invented. If no such direct link exists, skip the listing.
2. Write "Not listed" for missing deadlines — never invent one.
3. One short sentence per listing on why it fits {name}'s skills/interests specifically.
4. No "contact person" field — internship posts rarely name one and inventing it would mislead {name}.
5. Skip duplicates and anything expired or fake.

{raw_text}

Reply with ONLY a JSON list like this (empty list if nothing real found):
[{{"company": "...", "role": "...", "location": "...", "deadline": "...", "apply_url": "...", "fit_reason": "..."}}]
"""


def _strip_code_fence(text: str) -> str:
    """Remove a ```...``` wrapper Claude sometimes adds around its JSON reply."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text.strip()


def _parse_listings(reply: str) -> list[dict]:
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        print(f"  [Extractor] Claude's reply wasn't valid JSON:\n  {reply}")
        return []


def ask_claude(prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return _strip_code_fence(response.content[0].text)


def run(raw_text: str, profile: dict) -> list[dict]:
    prompt = PROMPT.format(
        name=profile["name"],
        major=profile["major"],
        target_roles=", ".join(profile["target_roles"]),
        skills=", ".join(profile["skills"]),
        interests=", ".join(profile["interests"]),
        location_preference=profile["location_preference"],
        raw_text=raw_text,
    )
    reply = ask_claude(prompt)
    return _parse_listings(reply)
