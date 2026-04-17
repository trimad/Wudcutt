from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .models import AssetMetadata


@dataclass(slots=True)
class AssetPaths:
    slug: str
    raw_dir: Path
    processed_dir: Path
    copy_dir: Path
    metadata_dir: Path


class AssetCatalog:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.raw_root = self.root / "raw"
        self.processed_root = self.root / "processed"
        self.copy_root = self.root / "copy"
        self.logs_root = self.root / "logs"
        self.metadata_root = self.root / "metadata"
        for path in [self.raw_root, self.processed_root, self.copy_root, self.logs_root, self.metadata_root]:
            path.mkdir(parents=True, exist_ok=True)

    def ensure_asset_dirs(self, slug: str) -> AssetPaths:
        raw_dir = self.raw_root / slug
        processed_dir = self.processed_root / slug
        copy_dir = self.copy_root / slug
        metadata_dir = self.metadata_root / slug
        for path in [raw_dir, processed_dir, copy_dir, metadata_dir]:
            path.mkdir(parents=True, exist_ok=True)
        return AssetPaths(slug=slug, raw_dir=raw_dir, processed_dir=processed_dir, copy_dir=copy_dir, metadata_dir=metadata_dir)

    def write_metadata(self, metadata: AssetMetadata) -> Path:
        paths = self.ensure_asset_dirs(metadata.slug)
        target = paths.metadata_dir / "metadata.json"
        target.write_text(json.dumps(metadata.to_dict(), indent=2, sort_keys=True))
        return target

    def write_copy_markdown(self, metadata: AssetMetadata, description: str) -> Path:
        paths = self.ensure_asset_dirs(metadata.slug)
        target = paths.copy_dir / "listing.md"
        tag_line = ", ".join(metadata.tags) if metadata.tags else ""
        body = (
            f"# {metadata.title}\n\n"
            f"Artist: {metadata.artist}\n"
            f"Year: {metadata.year}\n"
            f"Medium: {metadata.medium}\n"
            f"Source: {metadata.source_institution}\n"
            f"Source Page: {metadata.source_page_url}\n"
            f"License: {metadata.license_label}\n"
            f"License Reason: {metadata.license_reason}\n"
            f"Dimensions: {metadata.dimensions or 'unknown'}\n\n"
            f"## Description\n\n{description}\n\n"
            f"## Design Notes\n\n{metadata.notes or 'No notes yet.'}\n\n"
            f"## Tags\n\n{tag_line or 'No tags yet.'}\n"
        )
        target.write_text(body)
        return target
