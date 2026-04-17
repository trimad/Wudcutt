# Asset Schema

Each sourced artwork should get its own slug directory and metadata record.

Required metadata fields:
- slug
- title
- artist
- year
- medium
- source_institution
- source_page_url
- source_file_url
- license_label
- license_reason

Optional fields:
- preview_url
- downloaded_at
- dimensions
- notes
- tags
- provider
- quality_score
- quality_grade
- quality_reasons

Recommended layout:

```text
assets/
  raw/<slug>/source_original.ext
  processed/<slug>/
  copy/<slug>/listing.md
  metadata/<slug>/metadata.json
  logs/
```

The metadata JSON is the durable record of provenance.
The listing markdown stores the human-facing product copy.
Processed assets should contain threshold variants, transparent PNG exports, and any final storefront-ready image files.
