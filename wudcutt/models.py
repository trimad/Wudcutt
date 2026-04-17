from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import re
import unicodedata
from typing import Any


def slugify(*parts: str) -> str:
    bits = []
    for part in parts:
        if not part:
            continue
        normalized = unicodedata.normalize("NFKD", part).encode("ascii", "ignore").decode("ascii")
        cleaned = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
        if cleaned:
            bits.append(cleaned)
    return "-".join(bits)


@dataclass(slots=True)
class AssetMetadata:
    title: str
    artist: str
    year: str
    medium: str
    source_institution: str
    source_page_url: str
    source_file_url: str
    license_label: str
    license_reason: str
    preview_url: str | None = None
    slug: str | None = None
    downloaded_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    dimensions: str | None = None
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    provider: str | None = None
    quality_score: int | None = None
    quality_grade: str | None = None
    quality_reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        required = {
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "medium": self.medium,
            "source_institution": self.source_institution,
            "source_page_url": self.source_page_url,
            "source_file_url": self.source_file_url,
            "license_label": self.license_label,
            "license_reason": self.license_reason,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError(f"Missing required metadata fields: {', '.join(missing)}")
        if not self.slug:
            artist_parts = self.artist.split()
            artist_key = artist_parts[-1] if artist_parts else self.artist
            self.slug = slugify(artist_key, self.title, self.year)
        self.tags = [tag.strip().lower() for tag in self.tags if tag and tag.strip()]

    def to_dict(self) -> dict[str, Any]:
        return {
            "slug": self.slug,
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "medium": self.medium,
            "source_institution": self.source_institution,
            "source_page_url": self.source_page_url,
            "source_file_url": self.source_file_url,
            "preview_url": self.preview_url,
            "license_label": self.license_label,
            "license_reason": self.license_reason,
            "downloaded_at": self.downloaded_at,
            "dimensions": self.dimensions,
            "notes": self.notes,
            "tags": self.tags,
            "provider": self.provider,
            "quality_score": self.quality_score,
            "quality_grade": self.quality_grade,
            "quality_reasons": self.quality_reasons,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AssetMetadata":
        return cls(**payload)


@dataclass(slots=True)
class SearchCandidate:
    provider: str
    title: str
    artist: str
    year: str
    medium: str
    source_institution: str
    source_page_url: str
    source_file_url: str
    preview_url: str | None
    license_label: str
    license_reason: str
    width: int | None = None
    height: int | None = None
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    quality_score: int | None = None
    quality_grade: str | None = None
    quality_reasons: list[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        artist_parts = self.artist.split()
        artist_key = artist_parts[-1] if artist_parts else self.artist
        return slugify(artist_key, self.title, self.year)

    def to_metadata(self) -> AssetMetadata:
        dimensions = None
        if self.width and self.height:
            dimensions = f"{self.width}x{self.height}"
        return AssetMetadata(
            slug=self.slug,
            title=self.title,
            artist=self.artist,
            year=self.year,
            medium=self.medium,
            source_institution=self.source_institution,
            source_page_url=self.source_page_url,
            source_file_url=self.source_file_url,
            preview_url=self.preview_url,
            license_label=self.license_label,
            license_reason=self.license_reason,
            dimensions=dimensions,
            notes=self.notes,
            tags=self.tags,
            provider=self.provider,
            quality_score=self.quality_score,
            quality_grade=self.quality_grade,
            quality_reasons=self.quality_reasons,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "medium": self.medium,
            "source_institution": self.source_institution,
            "source_page_url": self.source_page_url,
            "source_file_url": self.source_file_url,
            "preview_url": self.preview_url,
            "license_label": self.license_label,
            "license_reason": self.license_reason,
            "width": self.width,
            "height": self.height,
            "tags": self.tags,
            "notes": self.notes,
            "quality_score": self.quality_score,
            "quality_grade": self.quality_grade,
            "quality_reasons": self.quality_reasons,
            "slug": self.slug,
        }
