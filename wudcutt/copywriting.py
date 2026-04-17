from __future__ import annotations

from dataclasses import dataclass

from .models import AssetMetadata


@dataclass(slots=True)
class ListingCopy:
    title: str
    short_description: str
    long_description: str
    tags: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "tags": self.tags,
        }


def generate_listing_copy(metadata: AssetMetadata) -> ListingCopy:
    subject = metadata.title
    title = f"{subject} Woodcut by {metadata.artist}"
    short_description = (
        f"A restored public-domain {metadata.medium} featuring {subject}, "
        "refined for strong contrast and wearable impact on apparel."
    )
    long_description = (
        f"{subject} is adapted from a public-domain {metadata.medium} by {metadata.artist} "
        f"({metadata.year}). The original historical linework is preserved while being prepared "
        "for bold, high-contrast printing on shirts and other products."
    )
    seed_tags = metadata.tags + [
        metadata.medium,
        metadata.artist.lower(),
        metadata.year,
        metadata.source_institution.lower(),
        "public domain",
    ]
    tags: list[str] = []
    subject_tag = subject.lower()
    if subject_tag not in tags:
        tags.append(subject_tag)
    for tag in seed_tags:
        normalized = tag.strip().lower()
        if normalized and normalized not in tags:
            tags.append(normalized)
    return ListingCopy(title=title, short_description=short_description, long_description=long_description, tags=tags[:15])
