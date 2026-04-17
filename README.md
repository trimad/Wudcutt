# Wudcutt

Wudcutt is a Python workflow for turning public-domain woodcuts and engravings into apparel-ready graphics.

It now supports four parts of the pipeline:
- discovering public-domain candidates from supported archives
- saving source files locally with provenance metadata
- generating thresholded and transparent print-ready variants
- generating listing copy for marketplaces like Redbubble and Society6

The repository also keeps the original Tkinter GUI for hands-on threshold tuning.

## Features

- Threshold processing for grayscale historical artwork
- Transparent PNG export for dark-shirt friendly graphics
- Batch threshold export in 5-step increments
- Structured asset catalog layout under `assets/`
- Metadata manifests for provenance and rights notes
- Listing title / short description / long description / tags generation
- Initial source adapters for:
  - Wikimedia Commons
  - Metropolitan Museum of Art Open Access
  - Library of Congress
  - Rijksmuseum
  - New York Public Library Digital Collections
  - Wellcome Collection
  - Internet Archive
- Candidate quality scoring for print suitability
- Marketplace CSV export from saved metadata

## Install

```bash
python -m pip install -r requirements.txt
```

Optional editable install:

```bash
python -m pip install -e .[dev]
```

## Asset layout

```text
assets/
  raw/<slug>/source_original.ext
  processed/<slug>/
  copy/<slug>/listing.md
  metadata/<slug>/metadata.json
  logs/
```

See `docs/ASSET_SCHEMA.md` for details.

## CLI usage

### Process an image into a transparent PNG

```bash
python -m wudcutt.cli process input.jpg --threshold 140 --transparent --output output.png
```

### Generate listing copy from saved metadata

```bash
python -m wudcutt.cli copy assets/metadata/durer-the-rhinoceros-1515/metadata.json
```

### Search Wikimedia Commons

```bash
python -m wudcutt.cli search wikimedia "durer rhinoceros"
```

### Search the Met Museum

```bash
python -m wudcutt.cli search metmuseum "four horsemen"
```

### Search other archives

```bash
python -m wudcutt.cli search loc "woodcut beast"
python -m wudcutt.cli search rijksmuseum "apocalypse"
python -m wudcutt.cli search nypl "dance of death"
python -m wudcutt.cli search wellcome "monster"
python -m wudcutt.cli search internet_archive "durer horsemen"
```

Notes:
- `rijksmuseum` live queries require `RIJKSMUSEUM_API_KEY`
- `nypl` live queries require `NYPL_TOKEN`

### Ingest the first search result into the local asset catalog

```bash
python -m wudcutt.cli ingest wikimedia "durer rhinoceros" --root assets --save-preview --auto-process --threshold 140
```

That command can now:
- download the original file
- save a preview image
- write `metadata.json`
- create a starter `listing.md`
- optionally create processed threshold and transparent outputs

### Export marketplace CSV from saved metadata

```bash
python -m wudcutt.cli export-marketplace assets --output exports/marketplace.csv
```

## GUI usage

Run the desktop app:

```bash
python Wüdcutt.py
```

Tabs:
- Threshold Adjuster: load an image, adjust threshold, save thresholded output
- Transparency Converter: preview and save a transparent PNG
- Macro: export many threshold variants to a chosen folder

## Source strategy

Recommended priorities for profitable historical shirt designs:
- animals with strong silhouette
- apocalypse / death / danse macabre imagery
- demons, saints, angels, occult or mythic scenes
- medieval warfare, riders, hunters, heraldic emblems

Recommended archives to expand next:
- Library of Congress
- Rijksmuseum
- NYPL Digital Collections
- Wellcome Collection
- Internet Archive

## Development

Run tests:

```bash
python -m pytest tests -q
```

## Status

Wudcutt has moved beyond a single-file GUI prototype, but there is still room to grow.
Useful next steps could include:
- more source adapters
- better quality scoring for search results
- print-preview composition helpers
- automatic processed asset export into `assets/processed/<slug>/`
- storefront CSV/export helpers
