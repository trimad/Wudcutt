import json
import subprocess
import sys


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "wudcutt.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_search_with_mock_provider(tmp_path):
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "wikimedia.json").write_text(
        json.dumps(
            {
                "query": {
                    "pages": {
                        "1": {
                            "title": "File:The Rhinoceros.jpg",
                            "imageinfo": [{
                                "url": "https://example.com/file.jpg",
                                "width": 4096,
                                "height": 3203,
                                "extmetadata": {"LicenseShortName": {"value": "Public domain"}},
                            }],
                            "categories": [{"title": "Category:woodcuts"}],
                        }
                    }
                }
            }
        )
    )

    result = run_cli(
        "search",
        "wikimedia",
        "rhinoceros",
        "--fixture-dir",
        str(fixtures),
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload[0]["provider"] == "wikimedia"
    assert payload[0]["title"] == "The Rhinoceros"


def test_cli_ingest_reports_empty_results_cleanly(tmp_path):
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "wikimedia.json").write_text(json.dumps({"query": {"pages": {}}}))

    result = run_cli(
        "ingest",
        "wikimedia",
        "missing",
        "--fixture-dir",
        str(fixtures),
        cwd=tmp_path,
    )

    assert result.returncode != 0
    assert "no search results" in result.stderr.lower()
