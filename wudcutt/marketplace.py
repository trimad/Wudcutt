from __future__ import annotations

import csv
import json
from pathlib import Path

from .copywriting import generate_listing_copy
from .models import AssetMetadata


def _load_metadata_rows(assets_root: str | Path) -> list[AssetMetadata]:
    assets_root = Path(assets_root)
    metadata_files = sorted((assets_root / "metadata").glob("*/metadata.json"))
    return [AssetMetadata.from_dict(json.loads(metadata_file.read_text())) for metadata_file in metadata_files]


def export_marketplace_csv(assets_root: str | Path, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    rows = []
    for metadata in _load_metadata_rows(assets_root):
        listing = generate_listing_copy(metadata)
        rows.append(
            {
                "slug": metadata.slug,
                "title": listing.title,
                "short_description": listing.short_description,
                "long_description": listing.long_description,
                "tags": ", ".join(listing.tags),
                "artist": metadata.artist,
                "year": metadata.year,
                "provider": metadata.provider or "",
                "source_institution": metadata.source_institution,
                "quality_score": metadata.quality_score or "",
                "quality_grade": metadata.quality_grade or "",
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["slug", "title", "short_description", "long_description", "tags", "artist", "year", "provider", "source_institution", "quality_score", "quality_grade"]
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def export_curation_csv(assets_root: str | Path, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    rows = []
    for metadata in sorted(_load_metadata_rows(assets_root), key=lambda item: (item.quality_score or 0), reverse=True):
        rows.append(
            {
                "slug": metadata.slug,
                "title": metadata.title,
                "artist": metadata.artist,
                "year": metadata.year,
                "provider": metadata.provider or "",
                "quality_score": metadata.quality_score or "",
                "quality_grade": metadata.quality_grade or "",
                "quality_reasons": " | ".join(metadata.quality_reasons),
                "source_institution": metadata.source_institution,
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["slug", "title", "artist", "year", "provider", "quality_score", "quality_grade", "quality_reasons", "source_institution"]
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path
