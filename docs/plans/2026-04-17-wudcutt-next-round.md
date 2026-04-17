# Wudcutt Next-Round Enhancements Plan

Goal: Expand Wudcutt with more public-domain providers, candidate quality scoring, richer ingest behavior, and marketplace export helpers.

## Scope
- Add adapters for Library of Congress, Rijksmuseum, NYPL, Wellcome, Internet Archive
- Add a reusable scoring system for candidate print suitability
- Save preview images on ingest
- Optionally auto-process ingested assets into thresholded and transparent outputs
- Add batch export helpers for marketplace listing data

## Tasks

1. Add tests for normalized candidate scoring and new provider adapters.
2. Extend metadata models to carry quality score fields.
3. Implement provider adapters with fixture-backed tests first.
4. Add scoring logic and integrate it into all providers.
5. Extend download/ingest flow to save previews and optional processed outputs.
6. Add marketplace export module and CLI command.
7. Update docs and verify with full tests and review.
