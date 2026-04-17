import json
from io import BytesIO

from PIL import Image

from wudcutt.downloads import save_candidate_asset
from wudcutt.models import SearchCandidate


class DummyResponse:
    def __init__(self, content=b"image-bytes"):
        self.content = content

    def raise_for_status(self):
        return None


class DummySession:
    def __init__(self):
        self.calls = []
        image = Image.new("RGB", (8, 8), color=(255, 255, 255))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        self.png = buffer.getvalue()

    def get(self, url, timeout=None):
        self.calls.append(url)
        return DummyResponse(self.png)


def test_save_candidate_asset_writes_preview_and_processed_outputs(tmp_path):
    candidate = SearchCandidate(
        provider="wikimedia",
        title="The Rhinoceros",
        artist="Albrecht Durer",
        year="1515",
        medium="woodcut",
        source_institution="Wikimedia Commons",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/source.png",
        preview_url="https://example.com/preview.png",
        license_label="public domain",
        license_reason="published before 1929",
        width=4096,
        height=3203,
        tags=["animal", "woodcut"],
        notes="Strong silhouette",
    )

    result = save_candidate_asset(candidate, tmp_path, session=DummySession(), save_preview=True, auto_process=True, threshold=128)

    assert result.source_path.exists()
    assert result.preview_path.exists()
    assert result.transparent_path.exists()
    assert result.threshold_path.exists()
    payload = json.loads(result.metadata_path.read_text())
    assert payload["title"] == "The Rhinoceros"
