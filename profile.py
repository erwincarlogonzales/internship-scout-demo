"""profile.py — your info. Edit this file, nothing else, to personalize the agents."""

from pathlib import Path

MY_PROFILE = {
    "name": "Carlo",
    "major": "Computer Science",
    "skills": ["Python", "data analysis", "public speaking"],
    "interests": ["AI", "fintech", "data analysis"],
    "location_preference": "Manila, Philippines (open to remote)",
    "target_roles": ["Software Engineering Intern", "Data Analyst Intern"],
}

OUTPUT_FILE = Path(__file__).parent / "internships.md"
JOB_BOARD_DOMAINS = ["jobstreet.com.ph", "kalibrr.com", "linkedin.com"]
