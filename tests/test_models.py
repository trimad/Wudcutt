from pathlib import Path

from wudcutt.models import AssetMetadata, SearchCandidate, slugify


def test_slugify_handles_unicode_and_punctuation():
    assert slugify("Dürer", "The Rhinoceros", "1515") == "durer-the-rhinoceros-1515"


def test_asset_metadata_generates_slug_and_roundtrips_tags():
    metadata = AssetMetadata(
        title="The Rhinoceros",
        artist="Albrecht Durer",
        year="1515",
        medium="woodcut",
        source_institution="Wikimedia Commons",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/file.jpg",
        license_label="public domain",
        license_reason="published before 1929",
        notes="Strong silhouette",
        tags=["animal", "renaissance"],
    )

    assert metadata.slug == "durer-the-rhinoceros-1515"
    payload = metadata.to_dict()
    assert payload["tags"] == ["animal", "renaissance"]

    restored = AssetMetadata.from_dict(payload)
    assert restored.slug == metadata.slug
    assert restored.tags == metadata.tags


def test_search_candidate_to_metadata_uses_resolution_hint():
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
        license_reason="public domain mark",
        width=4000,
        height=2500,
        tags=["apocalypse", "horsemen"],
        notes="Dense linework",
    )

    metadata = candidate.to_metadata()

    assert metadata.dimensions == "4000x2500"
    assert metadata.title == "The Four Horsemen"
    assert metadata.tags == ["apocalypse", "horsemen"]


def test_asset_metadata_requires_key_fields():
    try:
        AssetMetadata(
            title="",
            artist="Unknown",
            year="1500",
            medium="woodcut",
            source_institution="Archive",
            source_page_url="https://example.com/page",
            source_file_url="https://example.com/file.jpg",
            license_label="public domain",
            license_reason="old",
        )
    except ValueError as exc:
        assert "title" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError for empty title")
