# Wudcutt Repo Inspection

Date: 2026-04-17

## Executive summary

Wudcutt is currently a small desktop utility for preparing historical illustration images for apparel use.

Its present strength is manual image cleanup:
- load a source image
- convert it to grayscale
- preview a thresholded black/white version
- export either one thresholded image or a whole batch of threshold variants

This aligns well with your stated t-shirt workflow, but only covers the back half of the pipeline.

Right now the repo does not yet handle:
- sourcing public-domain woodcut images from the web
- recording provenance/license metadata
- storing asset notes in a reusable catalog
- generating product descriptions for Redbubble or Society6
- packaging a repeatable end-to-end workflow

## Repository shape

Top-level contents:
- `Wüdcutt.py` — the main and only application code
- sample art folders:
  - `The Rhino/`
  - `The Four Horsemen/`
  - `Death and the Lansquenet/`
- `.gitignore`
- `test` — currently empty

Git history is minimal:
- `78c58b9` first commit
- `aa2f786` test

There is no README, requirements file, packaging metadata, or test suite.

## What the app currently does

The single Python file builds a Tkinter GUI with three tabs:

### 1. Threshold Adjuster
Purpose:
- manually tune a black/white threshold using a slider

Behavior:
- loads an image
- applies EXIF transpose
- converts to grayscale
- applies a binary threshold with NumPy
- previews the result
- saves the processed output

### 2. Transparency Converter
Current state:
- the tab exists in the UI
- but it does not actually perform transparency conversion yet
- it currently just loads and saves the current image state

This is the biggest mismatch between the repo name/purpose and the current implementation.

### 3. Macro
Purpose:
- export a full sweep of threshold variants in steps of 5 from 0 to 250

Behavior:
- writes files named like `threshold_0.png`, `threshold_5.png`, etc.
- useful for quickly reviewing which threshold works best for print

## Important implementation details

### Strengths
- Simple and easy to understand
- Uses Pillow + NumPy only
- Good for fast manual experimentation
- Already proven against sample art in the repo

### Weaknesses / technical debt
- Hardcoded Windows default save path in the Macro tab
- No CLI mode for batch processing outside the GUI
- No metadata or provenance tracking
- No automation for sourcing images
- No tests
- No documentation
- No actual transparency-removal logic in the "Transparency Converter" tab
- Uses one shared `self.original_img` / `self.thresholded_img` state across tabs, which could become fragile as features grow

## Sample assets already in repo

Observed examples suggest the workflow is:
1. start from a historical source image
2. create multiple threshold variants
3. clean/select a preferred output
4. create a transparent PNG for storefront upload

Examples:
- `The Rhino/source.jpg` — 4096x3203
- `The Rhino/140-cleaned-transparent.png` — 5100x3988 RGBA
- `The Four Horsemen/0.jpg` — 2798x3801
- `Death and the Lansquenet/0.jpg` — 2586x3695

The transparent rhino output contains real alpha data and is likely apparel-ready as an asset, even though some viewers render transparent black artwork against a black background.

## Fit for your business goal

The repo is a good nucleus for the image-processing stage of a vintage woodcut t-shirt pipeline.

A strong end-to-end pipeline would be:
1. find public-domain woodcut/engraving source art
2. save the source locally with provenance
3. document artist/date/source/license
4. create thresholded and transparent apparel variants
5. generate marketplace-ready copy
6. export organized folders for Redbubble / Society6 / archive

Wudcutt currently covers step 4 only, and even there it is only partially complete.

## Best next improvements

Recommended repo evolution:

### Priority 1 — make the current tool reliable
- add README
- add `requirements.txt`
- replace hardcoded paths with a folder picker
- implement real transparency conversion
- add a CLI mode so the same processing can run non-interactively

### Priority 2 — add asset management
- create an `assets/` layout such as:
  - `assets/raw/`
  - `assets/processed/`
  - `assets/metadata/`
  - `assets/descriptions/`
- define a metadata schema per artwork:
  - title
  - artist
  - year
  - source URL
  - institution
  - rights/public-domain status
  - local filenames
  - threshold used
  - notes

### Priority 3 — add sourcing workflow
- define trusted public-domain sources
- add a downloader/search script
- log provenance automatically
- optionally rank images by print suitability

### Priority 4 — add listing copy generation
- generate short title ideas
- generate Redbubble/Society6 product descriptions
- generate tags/keywords
- keep all copy tied to the exact source asset metadata

## Conclusion

Wudcutt is not yet a full woodcut t-shirt production system, but it is pointed in the right direction.

Today it is best described as:
- a prototype desktop thresholding tool
- with sample historical artwork
- and the beginnings of an apparel-prep workflow

To support a repeatable profitable business workflow, the missing pieces are:
- sourcing
- provenance tracking
- cataloging
- description generation
- and a cleaner export pipeline
