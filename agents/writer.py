"""agents/writer.py — AGENT 3: WRITER

Job: take the clean, scored listings and format them into a
personalized markdown report.

Tool it uses: none — just text formatting.
"""

from profile import OUTPUT_FILE


def run(listings: list[dict], profile: dict) -> None:
    lines = [f"# Internships for {profile['name']}\n"]

    if not listings:
        lines.append("No real listings found — try broadening MY_PROFILE and running again.")

    for listing in listings:
        lines.append(f"## {listing.get('role', 'Not listed')} — {listing.get('company', 'Not listed')}")
        lines.append(f"- **Location:** {listing.get('location', 'Not listed')}")
        lines.append(f"- **Deadline:** {listing.get('deadline', 'Not listed')}")
        lines.append(f"- **Apply here:** {listing.get('apply_url', 'Not listed')}")
        lines.append(f"- **Why it fits you:** {listing.get('fit_reason', 'Not listed')}")
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
