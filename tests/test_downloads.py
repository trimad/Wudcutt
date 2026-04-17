import json

from wudcutt.downloads import save_candidate_asset
from wudcutt.models import SearchCandidate


class DummyResponse:
    def __init__(self, content=b"image-bytes"):
        self.content = content

    def raise_for_status(self):
        return None


class DummySession:
    def get(self, url, timeout=None):
        return DummyResponse()


def test_save_candidate_asset_writes_source_and_metadata(tmp_path):
    candidate = SearchCandidate(
        provider="wikimedia",
        title="The Rhinoceros",
        artist="Albrecht Durer",
        year="1515",
        medium="woodcut",
        source_institution="Wikimedia Commons",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/source.jpg",
        preview_url="https://example.com/preview.jpg",
        license_label="public domain",
        license_reason="published before 1929",
        width=4096,
        height=3203,
        tags=["animal", "woodcut"],
        notes="Strong silhouette",
    )

    result = save_candidate_asset(candidate, tmp_path, session=DummySession())

    assert result.source_path.exists()
    assert result.metadata_path.exists()
    assert result.copy_path.exists()
    payload = json.loads(result.metadata_path.read_text())
    assert payload["title"] == "The Rhinoceros"
    assert payload["dimensions"] == "4096x3203"
    assert "public-domain woodcut" in result.copy_path.read_text().lower()
