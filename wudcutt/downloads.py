from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from urllib.parse import urlparse

import requests

from .catalog import AssetCatalog
from .copywriting import generate_listing_copy
from .models import SearchCandidate
from .processing import apply_threshold, create_transparent_image, load_image_grayscale


@dataclass(slots=True)
class SavedAsset:
    source_path: Path
    metadata_path: Path
    copy_path: Path
    preview_path: Path | None = None
    threshold_path: Path | None = None
    transparent_path: Path | None = None


def _extension_from_url(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    return suffix or ".bin"


def save_candidate_asset(
    candidate: SearchCandidate,
    root: str | Path,
    session=None,
    save_preview: bool = False,
    auto_process: bool = False,
    threshold: int = 140,
) -> SavedAsset:
    catalog = AssetCatalog(root)
    paths = catalog.ensure_asset_dirs(candidate.slug)
    session = session or requests.Session()
    if hasattr(session, "headers"):
        session.headers["User-Agent"] = os.getenv("WUDCUTT_USER_AGENT", "Wudcutt/0.1 (+https://github.com/trimad/Wudcutt)")
    response = session.get(candidate.source_file_url, timeout=60)
    response.raise_for_status()
    source_path = paths.raw_dir / f"source_original{_extension_from_url(candidate.source_file_url)}"
    source_path.write_bytes(response.content)

    preview_path = None
    if save_preview and candidate.preview_url:
        preview_response = session.get(candidate.preview_url, timeout=60)
        preview_response.raise_for_status()
        preview_path = paths.raw_dir / f"source_preview{_extension_from_url(candidate.preview_url)}"
        preview_path.write_bytes(preview_response.content)

    metadata = candidate.to_metadata()
    metadata_path = catalog.write_metadata(metadata)
    listing = generate_listing_copy(metadata)
    description = f"{listing.short_description}\n\n{listing.long_description}\n\nSuggested tags: {', '.join(listing.tags)}"
    copy_path = catalog.write_copy_markdown(metadata, description)

    threshold_path = None
    transparent_path = None
    if auto_process:
        base_image = load_image_grayscale(source_path)
        threshold_image = apply_threshold(base_image, threshold)
        threshold_path = paths.processed_dir / f"threshold_{threshold}.png"
        threshold_image.save(threshold_path)
        transparent_image = create_transparent_image(threshold_image)
        transparent_path = paths.processed_dir / "transparent.png"
        transparent_image.save(transparent_path)

    return SavedAsset(
        source_path=source_path,
        metadata_path=metadata_path,
        copy_path=copy_path,
        preview_path=preview_path,
        threshold_path=threshold_path,
        transparent_path=transparent_path,
    )
