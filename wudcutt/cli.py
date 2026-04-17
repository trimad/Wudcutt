from __future__ import annotations

import argparse
import json
from pathlib import Path

from .copywriting import generate_listing_copy
from .downloads import save_candidate_asset
from .models import AssetMetadata
from .processing import apply_threshold, create_transparent_image, load_image_grayscale, suggest_threshold
from .sources.internet_archive import InternetArchiveSource
from .sources.loc import LibraryOfCongressSource
from .sources.metmuseum import MetMuseumSource
from .sources.nypl import NYPLSource
from .sources.rijksmuseum import RijksmuseumSource
from .sources.wellcome import WellcomeSource
from .sources.wikimedia import WikimediaSource
from .marketplace import export_curation_csv, export_marketplace_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wudcutt")
    subparsers = parser.add_subparsers(dest="command", required=True)

    process_parser = subparsers.add_parser("process")
    process_parser.add_argument("source")
    process_parser.add_argument("--threshold", type=int, default=140)
    process_parser.add_argument("--auto-threshold", action="store_true")
    process_parser.add_argument("--transparent", action="store_true")
    process_parser.add_argument("--output", required=True)

    copy_parser = subparsers.add_parser("copy")
    copy_parser.add_argument("metadata")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("provider", choices=["wikimedia", "metmuseum", "loc", "rijksmuseum", "nypl", "wellcome", "internet_archive"])
    search_parser.add_argument("query")
    search_parser.add_argument("--fixture-dir")

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("provider", choices=["wikimedia", "metmuseum", "loc", "rijksmuseum", "nypl", "wellcome", "internet_archive"])
    ingest_parser.add_argument("query")
    ingest_parser.add_argument("--root", default="assets")
    ingest_parser.add_argument("--fixture-dir")
    ingest_parser.add_argument("--index", type=int, default=0)
    ingest_parser.add_argument("--save-preview", action="store_true")
    ingest_parser.add_argument("--auto-process", action="store_true")
    ingest_parser.add_argument("--threshold", type=int, default=140)

    export_parser = subparsers.add_parser("export-marketplace")
    export_parser.add_argument("assets_root")
    export_parser.add_argument("--output", required=True)

    curation_parser = subparsers.add_parser("export-curation")
    curation_parser.add_argument("assets_root")
    curation_parser.add_argument("--output", required=True)

    return parser


def _source(provider: str, fixture_dir: str | None = None):
    if provider == "wikimedia":
        return WikimediaSource(fixture_dir=fixture_dir)
    if provider == "metmuseum":
        return MetMuseumSource(fixture_dir=fixture_dir)
    if provider == "loc":
        return LibraryOfCongressSource(fixture_dir=fixture_dir)
    if provider == "rijksmuseum":
        return RijksmuseumSource(fixture_dir=fixture_dir)
    if provider == "nypl":
        return NYPLSource(fixture_dir=fixture_dir)
    if provider == "wellcome":
        return WellcomeSource(fixture_dir=fixture_dir)
    if provider == "internet_archive":
        return InternetArchiveSource(fixture_dir=fixture_dir)
    raise ValueError(f"Unsupported provider: {provider}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "process":
        img = load_image_grayscale(args.source)
        threshold = suggest_threshold(img) if args.auto_threshold else args.threshold
        img = apply_threshold(img, threshold)
        if args.transparent:
            img = create_transparent_image(img)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        img.save(args.output)
        return 0

    if args.command == "copy":
        payload = json.loads(Path(args.metadata).read_text())
        metadata = AssetMetadata.from_dict(payload)
        listing = generate_listing_copy(metadata)
        print(json.dumps(listing.to_dict()))
        return 0

    if args.command == "search":
        candidates = _source(args.provider, args.fixture_dir).search(args.query)
        print(json.dumps([candidate.to_dict() for candidate in candidates]))
        return 0

    if args.command == "ingest":
        candidates = _source(args.provider, args.fixture_dir).search(args.query)
        if not candidates:
            parser.exit(status=1, message="No search results found for ingest.\n")
        if args.index < 0 or args.index >= len(candidates):
            parser.exit(status=1, message=f"Requested index {args.index} is out of range for {len(candidates)} results.\n")
        selected = candidates[args.index]
        saved = save_candidate_asset(
            selected,
            args.root,
            save_preview=args.save_preview,
            auto_process=args.auto_process,
            threshold=args.threshold,
        )
        print(json.dumps({
            "source_path": str(saved.source_path),
            "metadata_path": str(saved.metadata_path),
            "copy_path": str(saved.copy_path),
            "preview_path": str(saved.preview_path) if saved.preview_path else "",
            "threshold_path": str(saved.threshold_path) if saved.threshold_path else "",
            "transparent_path": str(saved.transparent_path) if saved.transparent_path else "",
        }))
        return 0

    if args.command == "export-marketplace":
        output_path = export_marketplace_csv(args.assets_root, args.output)
        print(json.dumps({"output": str(output_path)}))
        return 0

    if args.command == "export-curation":
        output_path = export_curation_csv(args.assets_root, args.output)
        print(json.dumps({"output": str(output_path)}))
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
