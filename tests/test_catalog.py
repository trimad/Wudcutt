import json
from pathlib import Path

from wudcutt.catalog import AssetCatalog
from wudcutt.models import AssetMetadata


def make_metadata():
    return AssetMetadata(
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


def test_asset_catalog_creates_expected_folder_layout(tmp_path):
    catalog = AssetCatalog(tmp_path)
    metadata = make_metadata()

    paths = catalog.ensure_asset_dirs(metadata.slug)

    assert paths.raw_dir.exists()
    assert paths.processed_dir.exists()
    assert paths.copy_dir.exists()
    assert paths.metadata_dir.exists()


def test_asset_catalog_writes_metadata_json(tmp_path):
    catalog = AssetCatalog(tmp_path)
    metadata = make_metadata()

    metadata_path = catalog.write_metadata(metadata)

    payload = json.loads(metadata_path.read_text())
    assert payload["slug"] == metadata.slug
    assert payload["artist"] == "Albrecht Durer"


def test_asset_catalog_writes_copy_markdown(tmp_path):
    catalog = AssetCatalog(tmp_path)
    metadata = make_metadata()

    path = catalog.write_copy_markdown(metadata, "Short description here")

    text = path.read_text()
    assert metadata.title in text
    assert "Short description here" in text
