"""main.py — runs the three internship_scout agents, one after another.

    [1] Searcher  ->  [2] Extractor/Scorer  ->  [3] Writer

Each agent lives in its own file under agents/ and does ONE job.
This file just wires them together and passes each one's output
to the next — that's the whole pipeline.
"""

from dotenv import load_dotenv

from agents import extractor, searcher, writer
from profile import MY_PROFILE, OUTPUT_FILE

load_dotenv()


def main():
    print(f"Looking for internships for {MY_PROFILE['name']}...")

    raw_results = searcher.run(MY_PROFILE)
    listings = extractor.run(raw_results, MY_PROFILE)
    writer.run(listings, MY_PROFILE)

    print(f"Found {len(listings)} real listings")
    print(f"Done! Open {OUTPUT_FILE.name} to see your personalized internship list.")


if __name__ == "__main__":
    main()
