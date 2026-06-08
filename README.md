# internship-scout

A tiny project that automatically searches the web for internships that match
*you* — your major, skills, and interests — and writes the real ones (with
working apply links) into a file called `internships.md`.

If you've never built anything with AI or run a Python project from a
terminal before, this is a good first one: it's small enough to read top to
bottom, and every file does exactly one simple thing. Nothing below requires
you to write any code — just copy, paste, and fill in a few blanks.

## What you'll need

- **Python 3.10+** — check what you have by running `python --version` in a
  terminal.
- **[uv](https://docs.astral.sh/uv/)** — a tool that downloads and manages
  this project's dependencies for you. Install it once by following the
  instructions on that page (one command, nothing to configure).
- **Two API keys** (free to get, see step 2 below) — these let the project
  "borrow" two services for you: a web search engine (Tavily) and an AI model
  (Claude). Tavily's free tier comfortably covers running this many times;
  Claude is pay-as-you-go but each run only costs a few cents.

## Setup

1. **Install dependencies.** From inside this folder, run:
   ```
   uv sync
   ```
   This downloads everything the project needs into a local `.venv` folder —
   it won't touch anything else on your machine.

2. **Add your API keys.**
   - Make a copy of `.env.example`, name the copy `.env`, and open it.
   - Get an `ANTHROPIC_API_KEY` from https://console.anthropic.com
   - Get a `TAVILY_API_KEY` from https://tavily.com
   - Paste each key into `.env` in place of the placeholder text.

   `.env` is already listed in `.gitignore`, so it's never committed or
   shared — treat your keys like passwords and keep them in that file only.

3. **Tell it about yourself.** Open `profile.py` — the *only* file you need
   to edit — and fill in the `MY_PROFILE` dict with your major, skills,
   interests, location, and the kind of roles you're after.

## Run it

```
uv run python main.py
```

You'll see it print what it's searching for, and after a minute or so it'll
report `Found N real listings`. Open the generated `internships.md` for your
personalized list — each entry has a real apply link and a one-line note on
why it's a good fit for you.

**Got `Found 0 real listings`?** That's not necessarily a bug — it usually
means this run's searches didn't turn up postings with a real, direct apply
link (the project deliberately skips anything it can't verify, rather than
guessing). Try broadening `target_roles` in `profile.py`, or simply run it
again later — new postings appear all the time.

## How it works

You don't need to understand this before running the project — come back to
it afterwards, once you've seen the output and have something concrete to map
these pieces onto.

Three small "agents" — plain Python files that each do one job — are chained
together by `main.py`:

```
[1] Searcher  ->  [2] Extractor/Scorer  ->  [3] Writer
```

1. **`agents/searcher.py`** — searches the web (via Tavily) for internships
   matching your target roles and location. Returns raw, messy results: some
   real listings, some search-results pages, some irrelevant noise.
2. **`agents/extractor.py`** — hands those messy results to Claude and asks
   it to pick out only the *real* listings, each with a one-line "why this
   fits you." It's told explicitly never to invent a deadline, a contact
   person, or an application link that isn't actually written in the text.
3. **`agents/writer.py`** — formats the clean listings into `internships.md`.

`main.py` just runs the three in order, passing each one's output to the
next — that's the whole pipeline. `profile.py` holds your info and the
shared settings (output file path, which job boards to search).
