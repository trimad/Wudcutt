import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


def run_cli(*args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "wudcutt.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_cli_process_threshold_and_transparent(tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (4, 4), color=(255, 255, 255)).save(source)
    output = tmp_path / "transparent.png"

    result = run_cli("process", str(source), "--threshold", "128", "--transparent", "--output", str(output), cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    assert output.exists()


def test_cli_generate_copy_outputs_json(tmp_path):
    metadata = tmp_path / "metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "title": "The Rhinoceros",
                "artist": "Albrecht Durer",
                "year": "1515",
                "medium": "woodcut",
                "source_institution": "Wikimedia Commons",
                "source_page_url": "https://example.com/page",
                "source_file_url": "https://example.com/file.jpg",
                "license_label": "public domain",
                "license_reason": "published before 1929",
                "notes": "Armored silhouette and antique linework",
                "tags": ["animal", "woodcut"],
            }
        )
    )

    result = run_cli("copy", str(metadata), cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "title" in payload
    assert "short_description" in payload


def test_cli_process_auto_threshold(tmp_path):
    source = tmp_path / "source.png"
    img = Image.new("L", (8, 8))
    pixels = [20] * 32 + [220] * 32
    img.putdata(pixels)
    img.save(source)
    output = tmp_path / "auto-threshold.png"

    result = run_cli("process", str(source), "--auto-threshold", "--output", str(output), cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    assert output.exists()
