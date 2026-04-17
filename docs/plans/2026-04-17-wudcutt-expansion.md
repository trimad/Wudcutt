# Wudcutt Expansion Implementation Plan

> For Hermes: execute this plan task-by-task using strict TDD. Write failing tests first for each new behavior.

Goal: Turn Wudcutt from a single-file thresholding GUI into a reusable toolkit for discovering public-domain woodcut assets, saving provenance-rich metadata, producing apparel-ready transparent exports, and generating marketplace-ready product copy.

Architecture: Split the current monolithic GUI into a small Python package with focused modules for image processing, asset metadata/catalog management, source adapters, and copy generation. Keep a thin Tkinter GUI wrapper for interactive use, but make the important behaviors available from a CLI and tested library code so the workflow is repeatable and scriptable.

Tech stack: Python 3, Pillow, NumPy, requests, tkinter, pytest.

---

## Task 1: Add project scaffolding and dependency manifests

Objective: Create a maintainable project structure and basic project docs.

Files:
- Create: `README.md`
- Create: `requirements.txt`
- Create: `wudcutt/__init__.py`
- Create: `tests/__init__.py`

Verification:
- `python -m pytest tests -q` runs and discovers tests (even if none yet)
- `python -c "import wudcutt; print('ok')"` prints `ok`

## Task 2: Define metadata models and asset directory helpers

Objective: Add structured models for artwork metadata and helpers for local storage layout.

Files:
- Create: `wudcutt/models.py`
- Create: `wudcutt/catalog.py`
- Create: `tests/test_models.py`
- Create: `tests/test_catalog.py`

Verification:
- tests cover slug generation, serialization, required fields, and path creation

## Task 3: Extract reusable image processing functions from the GUI

Objective: Move thresholding and transparency logic into a library module.

Files:
- Create: `wudcutt/processing.py`
- Create: `tests/test_processing.py`
- Modify: `Wüdcutt.py`

Verification:
- tests cover thresholding, macro threshold generation, and transparent export
- GUI imports library functions instead of embedding all logic inline

## Task 4: Add a command-line interface for processing assets

Objective: Support non-interactive thresholding/transparency operations from the shell.

Files:
- Create: `wudcutt/cli.py`
- Create: `tests/test_cli.py`
- Modify: `README.md`

Verification:
- CLI supports threshold export and transparent export
- tests invoke the CLI module and verify output files exist

## Task 5: Add copywriting helpers for titles, descriptions, and tags

Objective: Generate marketplace-ready copy from metadata and design notes.

Files:
- Create: `wudcutt/copywriting.py`
- Create: `tests/test_copywriting.py`

Verification:
- tests validate generated title, short description, long description, and tag lists

## Task 6: Add source adapter framework and Wikimedia Commons search adapter

Objective: Provide a repeatable way to search public-domain archives.

Files:
- Create: `wudcutt/sources/__init__.py`
- Create: `wudcutt/sources/base.py`
- Create: `wudcutt/sources/wikimedia.py`
- Create: `tests/test_wikimedia_source.py`

Verification:
- tests validate parsing of mocked Wikimedia API responses
- adapter returns normalized candidate records

## Task 7: Add a second source adapter for a museum/open-access source

Objective: Prove the source framework works across more than one provider.

Files:
- Create: `wudcutt/sources/metmuseum.py`
- Create: `tests/test_metmuseum_source.py`

Verification:
- tests validate parsing of mocked Met API responses
- adapter normalizes provenance, title, and file URLs

## Task 8: Add download/manifest workflow

Objective: Save chosen candidates locally with metadata and starter copy docs.

Files:
- Create: `wudcutt/downloads.py`
- Create: `tests/test_downloads.py`
- Modify: `wudcutt/catalog.py`

Verification:
- tests validate folder creation, metadata JSON writing, preview path generation, and safe filenames

## Task 9: Add CLI commands for search and ingest

Objective: Make search/download usable from the terminal.

Files:
- Modify: `wudcutt/cli.py`
- Create: `tests/test_cli_search.py`
- Modify: `README.md`

Verification:
- CLI can search providers with a query
- CLI can ingest a mocked candidate into the asset layout

## Task 10: Rebuild the GUI as a thin front-end over the library

Objective: Keep the desktop workflow, but backed by reusable code.

Files:
- Modify: `Wüdcutt.py`

Verification:
- GUI still launches
- thresholding and transparency use the shared library functions
- hardcoded Windows path is removed

## Task 11: Add example asset templates and docs

Objective: Make the workflow self-explanatory for future use.

Files:
- Modify: `README.md`
- Create: `docs/ASSET_SCHEMA.md`
- Create: `assets/.gitkeep`
- Create: `assets/raw/.gitkeep`
- Create: `assets/processed/.gitkeep`
- Create: `assets/copy/.gitkeep`
- Create: `assets/logs/.gitkeep`

Verification:
- README documents end-to-end usage with examples

## Task 12: Final verification

Objective: Confirm the expanded repo works as a coherent system.

Files:
- Modify as needed based on fixes from verification

Verification:
- `python -m pytest tests -q`
- spot-check CLI help and one mocked search command
- run independent review over git diff before presenting results
