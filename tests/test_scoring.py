from wudcutt.models import SearchCandidate
from wudcutt.scoring import score_candidate


def test_score_candidate_rewards_resolution_and_useful_tags():
    candidate = SearchCandidate(
        provider="wikimedia",
        title="The Four Horsemen",
        artist="Albrecht Durer",
        year="1498",
        medium="woodcut",
        source_institution="Wikimedia Commons",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/file.jpg",
        preview_url="https://example.com/preview.jpg",
        license_label="public domain",
        license_reason="public domain",
        width=5000,
        height=3800,
        tags=["horsemen", "apocalypse", "woodcut"],
        notes="dramatic centered composition",
    )

    scored = score_candidate(candidate)

    assert scored.quality_score >= 80
    assert scored.quality_grade == "A"
    assert any("resolution" in reason.lower() for reason in scored.quality_reasons)


def test_score_candidate_penalizes_low_resolution():
    candidate = SearchCandidate(
        provider="wikimedia",
        title="Small Scan",
        artist="Unknown",
        year="1600",
        medium="woodcut",
        source_institution="Archive",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/file.jpg",
        preview_url=None,
        license_label="public domain",
        license_reason="public domain",
        width=900,
        height=700,
        tags=["misc"],
        notes="",
    )

    scored = score_candidate(candidate)

    assert scored.quality_score < 60
    assert scored.quality_grade in {"B", "C"}
