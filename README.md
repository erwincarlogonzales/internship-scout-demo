# internship-scout

A tiny 3-agent pipeline that searches the web for internships matching your
profile and writes the real ones (with working apply links) into `internships.md`.

## Setup

**Prerequisites:** Python 3.10+ and [uv](https://docs.astral.sh/uv/)

1. Install dependencies:
   ```
   uv sync
   ```
2. Copy `.env.example` to `.env` and add your keys:
   - `ANTHROPIC_API_KEY` from https://console.anthropic.com
   - `TAVILY_API_KEY` from https://tavily.com
3. Open `profile.py` and edit the `MY_PROFILE` dict with your own
   major, skills, interests, and target roles. That's the only file
   you need to touch.

## Run it

```
uv run python main.py
```

Open the generated `internships.md` to see your personalized list.

## How it works

Three small agents, each in its own file under `agents/`, chained together
by `main.py`:

```
[1] Searcher  ->  [2] Extractor/Scorer  ->  [3] Writer
```

1. **`agents/searcher.py`** — searches the web (via Tavily) for internships
   matching your target roles and location. Returns raw, messy results.
2. **`agents/extractor.py`** — has Claude read those messy results and pull
   out only the real listings, each with a one-line "why this fits you."
   It's told explicitly never to invent a deadline, a contact person, or
   an application link that isn't actually there.
3. **`agents/writer.py`** — formats the clean listings into `internships.md`.

`main.py` just runs the three in order, passing each one's output to the
next — that's the whole pipeline. `profile.py` holds your info and the
shared settings (output file path, which job-board domains to search).
