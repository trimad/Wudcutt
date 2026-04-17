import csv
import json
import subprocess
import sys
from pathlib import Path


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "wudcutt.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_export_marketplace_csv(tmp_path):
    metadata_root = tmp_path / "assets" / "metadata" / "durer-the-rhinoceros-1515"
    metadata_root.mkdir(parents=True)
    (metadata_root / "metadata.json").write_text(json.dumps({
        "title": "The Rhinoceros",
        "artist": "Albrecht Durer",
        "year": "1515",
        "medium": "woodcut",
        "source_institution": "Wikimedia Commons",
        "source_page_url": "https://example.com/page",
        "source_file_url": "https://example.com/file.jpg",
        "license_label": "public domain",
        "license_reason": "public domain",
        "notes": "Armored silhouette",
        "tags": ["animal", "woodcut"],
        "slug": "durer-the-rhinoceros-1515",
        "provider": "wikimedia",
        "quality_score": 92,
        "quality_grade": "A",
        "quality_reasons": ["Excellent resolution", "Strong silhouette"]
    }))
    output = tmp_path / "marketplace.csv"

    result = run_cli("export-marketplace", str(tmp_path / "assets"), "--output", str(output), cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    rows = list(csv.DictReader(output.read_text().splitlines()))
    assert len(rows) == 1
    assert rows[0]["slug"] == "durer-the-rhinoceros-1515"
    assert "Rhinoceros" in rows[0]["title"]
    assert rows[0]["quality_grade"] == "A"


def test_cli_export_curation_csv(tmp_path):
    metadata_root = tmp_path / "assets" / "metadata" / "durer-the-rhinoceros-1515"
    metadata_root.mkdir(parents=True)
    (metadata_root / "metadata.json").write_text(json.dumps({
        "title": "The Rhinoceros",
        "artist": "Albrecht Durer",
        "year": "1515",
        "medium": "woodcut",
        "source_institution": "Wikimedia Commons",
        "source_page_url": "https://example.com/page",
        "source_file_url": "https://example.com/file.jpg",
        "license_label": "public domain",
        "license_reason": "public domain",
        "notes": "Armored silhouette",
        "tags": ["animal", "woodcut"],
        "slug": "durer-the-rhinoceros-1515",
        "provider": "wikimedia",
        "quality_score": 92,
        "quality_grade": "A",
        "quality_reasons": ["Excellent resolution", "Strong silhouette"]
    }))
    output = tmp_path / "curation.csv"

    result = run_cli("export-curation", str(tmp_path / "assets"), "--output", str(output), cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    rows = list(csv.DictReader(output.read_text().splitlines()))
    assert len(rows) == 1
    assert rows[0]["slug"] == "durer-the-rhinoceros-1515"
    assert rows[0]["quality_score"] == "92"
