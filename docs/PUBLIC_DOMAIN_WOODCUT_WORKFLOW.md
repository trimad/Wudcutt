# Public-Domain Woodcut T-Shirt Workflow Plan

Date: 2026-04-17
Repo: `/home/tristan/Desktop/Wudcutt`

## Goal

Extend Wudcutt from a manual image-thresholding utility into a repeatable workflow for:
- finding high-resolution public-domain woodcut / engraving illustrations
- saving them locally with provenance
- documenting each asset cleanly
- producing transparent t-shirt-ready outputs
- generating short storefront descriptions for Redbubble and Society6

## Trusted image sources to prioritize

These are the best first-pass sources because they frequently expose public-domain historical scans at high resolution and usually provide provenance metadata.

### Tier 1: strongest starting points
- Wikimedia Commons
- The Metropolitan Museum of Art Open Access
- Rijksmuseum
- Library of Congress
- Internet Archive
- New York Public Library Digital Collections
- Wellcome Collection
- Rawpixel Public Domain

### Tier 2: useful depending on subject matter
- British Museum collection pages
- Gallica / BnF
- Artvee
- Europeana
- Harvard Art Museums
- Cleveland Museum of Art Open Access

## Search heuristics for profitable candidates

Focus on subjects that tend to work on shirts:
- animals with strong silhouette
- skeletons / death iconography / danse macabre
- demons, saints, angels, apocalypse scenes
- medieval combat / horsemen / hunters / mythic beasts
- botanical / occult / alchemical imagery
- heraldic and emblematic compositions
- strange historical creatures

High-conversion visual traits:
- centered or easily center-croppable composition
- high contrast linework
- limited background clutter
- iconic silhouette at a distance
- enough detail to feel premium when printed large

Avoid or deprioritize:
- low-resolution scans
- muddy gray reproductions with weak linework
- sources with unclear copyright language
- images whose appeal depends on color rather than line art
- compositions that become unreadable when thresholded

## Recommended local folder structure

```text
assets/
  raw/
    <slug>/
      source_original.ext
      source_preview.ext
  processed/
    <slug>/
      threshold_*.png
      transparent.png
  copy/
    <slug>/
      listing.md
  metadata/
    <slug>/
      metadata.json
  logs/
```

Example slug:
- `durer-rhinoceros-1515`
- `holbein-death-lansquenet`

## Metadata schema per artwork

Every saved artwork should record:

```json
{
  "slug": "durer-rhinoceros-1515",
  "title": "The Rhinoceros",
  "artist": "Albrecht Durer",
  "year": "1515",
  "medium": "woodcut",
  "source_institution": "Wikimedia Commons",
  "source_page_url": "...",
  "source_file_url": "...",
  "license_label": "public domain",
  "license_reason": "published before 1929 / museum public-domain mark",
  "downloaded_at": "2026-04-17T00:00:00Z",
  "dimensions": "4096x3203",
  "notes": "Strong silhouette, high print appeal, text may be removable for cleaner shirt design",
  "tags": ["rhinoceros", "renaissance", "woodcut", "animal", "historical illustration"]
}
```

## Proposed end-to-end workflow

### Step 1: source discovery
For each search session:
- search trusted public-domain archives first
- open candidate result pages
- verify public-domain status explicitly
- prefer original scan download links over derivative thumbnails
- reject low-res or unclear-license results immediately

### Step 2: save locally
For each accepted image:
- create slug folder under `assets/raw/<slug>/`
- save original file as `source_original.<ext>`
- optionally save a preview image as `source_preview.<ext>`
- write metadata to `assets/metadata/<slug>/metadata.json`

### Step 3: assess print suitability
Before processing, score the image for:
- silhouette clarity
- line density
- background clutter
- crop flexibility
- likely market theme

Simple rating system:
- `A` = strong t-shirt candidate
- `B` = workable with cleanup
- `C` = archive only

### Step 4: process through Wudcutt
Use Wudcutt to:
- generate threshold variants
- select best threshold for apparel contrast
- produce transparent PNG
- export high-resolution print-ready version

### Step 5: document the finished design
Create a markdown file in `assets/copy/<slug>/listing.md` containing:
- artwork title
- historical attribution
- source and provenance summary
- design notes
- short Redbubble description
- short Society6 description
- keyword/tag ideas

## Product description template

### Redbubble / Society6 short description template

`A restored public-domain woodcut featuring <subject>. This design preserves the bold linework and antique character of the original historical illustration, cleaned for strong contrast and wearable impact on modern apparel.`

### Optional longer variant

`A high-contrast adaptation of a public-domain historical woodcut, refined for apparel printing. The original illustration's engraved textures and dramatic silhouette give this design a timeless graphic feel that works especially well on dark shirts and other minimalist products.`

## Example product descriptions

### Durer rhinoceros
`A restored public-domain woodcut of Albrecht Durer's famous rhinoceros, refined for bold contrast and strong shirt printing. The antique linework and armored silhouette give it a timeless graphic look with real historical character.`

### Death and the Lansquenet
`A dramatic public-domain woodcut showing Death confronting a landsknecht, cleaned for sharp contrast and wearable impact. The dense linework and dark historical mood make it a striking design for fans of medieval and memento mori imagery.`

### Four Horsemen
`A restored public-domain apocalypse woodcut featuring the Four Horsemen, prepared for high-contrast apparel printing. The chaotic composition and historic engraved detail give it a dark, iconic presence on a shirt.`

## Suggested repo additions

Recommended files to add next:
- `README.md`
- `requirements.txt`
- `assets/` directory layout
- `docs/public_domain_sourcing.md`
- `scripts/search_public_domain.py`
- `scripts/download_asset.py`
- `scripts/write_description.py`
- `schemas/asset_metadata.schema.json`

## Suggested automation features

### 1. Search helper
A script should:
- query known public-domain sources
- return title, artist, year, resolution, source URL, license note
- rank likely shirt candidates

### 2. Download + manifest helper
A script should:
- create the slug folder
- download the source image
- write metadata JSON
- optionally write a starter markdown description file

### 3. Description generator
A script should generate:
- 1 short product description
- 1 longer product description
- 10-20 tags
- 3-5 possible product titles

### 4. Wudcutt CLI mode
Wudcutt should support:
- batch threshold generation from command line
- transparent export from command line
- optional auto-save into `assets/processed/<slug>/`

## Practical search phrases to reuse

Use combinations like:
- `site:commons.wikimedia.org woodcut rhinoceros public domain`
- `site:loc.gov woodcut skeleton public domain`
- `site:metmuseum.org woodcut horseman open access`
- `site:rijksmuseum.nl engraving demon public domain`
- `site:archive.org albrecht durer woodcut`
- `site:rawpixel.com public domain woodcut animal`

## Decision rule for downloading

Download only if all are true:
- explicit public-domain or open-access status
- sufficiently high resolution for print workflow
- visually strong enough to survive thresholding
- commercially interesting subject or silhouette

## Bottom line

Wudcutt already covers a useful processing step, but the profitable repeatable system is really:
- search
- verify rights
- download
- document
- process
- write copy
- publish

That is the skillset to build next.
