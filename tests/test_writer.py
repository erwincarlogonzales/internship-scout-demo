import pytest

from agents import writer


@pytest.fixture
def output_file(tmp_path, monkeypatch):
    path = tmp_path / "internships.md"
    monkeypatch.setattr(writer, "OUTPUT_FILE", path)
    return path


def test_run_handles_listing_with_missing_fields(output_file):
    listings = [{"role": "Data Analyst Intern", "company": "Acme Corp"}]
    profile = {"name": "Carlo"}

    writer.run(listings, profile)

    content = output_file.read_text(encoding="utf-8")
    assert "Data Analyst Intern" in content
    assert "Acme Corp" in content
    assert "Not listed" in content


def test_run_writes_complete_listing(output_file):
    listings = [{
        "role": "Software Engineering Intern",
        "company": "Acme Corp",
        "location": "Manila, Philippines",
        "deadline": "June 30, 2026",
        "apply_url": "https://example.com/jobs/view/123",
        "fit_reason": "Matches Carlo's Python skills.",
    }]
    profile = {"name": "Carlo"}

    writer.run(listings, profile)

    content = output_file.read_text(encoding="utf-8")
    assert "# Internships for Carlo" in content
    assert "## Software Engineering Intern — Acme Corp" in content
    assert "- **Location:** Manila, Philippines" in content
    assert "- **Deadline:** June 30, 2026" in content
    assert "- **Apply here:** https://example.com/jobs/view/123" in content
    assert "- **Why it fits you:** Matches Carlo's Python skills." in content


def test_run_writes_fallback_message_when_no_listings(output_file):
    writer.run([], {"name": "Carlo"})

    content = output_file.read_text(encoding="utf-8")
    assert "# Internships for Carlo" in content
    assert "No real listings found" in content
