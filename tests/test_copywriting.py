from wudcutt.copywriting import generate_listing_copy
from wudcutt.models import AssetMetadata


def test_generate_listing_copy_contains_title_descriptions_and_tags():
    metadata = AssetMetadata(
        title="The Rhinoceros",
        artist="Albrecht Durer",
        year="1515",
        medium="woodcut",
        source_institution="Wikimedia Commons",
        source_page_url="https://example.com/page",
        source_file_url="https://example.com/file.jpg",
        license_label="public domain",
        license_reason="published before 1929",
        notes="Armored silhouette and antique linework",
        tags=["animal", "renaissance", "woodcut"],
    )

    listing = generate_listing_copy(metadata)

    assert "Rhinoceros" in listing.title
    assert "public-domain" in listing.short_description.lower()
    assert "Albrecht Durer" in listing.long_description
    assert len(listing.tags) >= 5
    assert "woodcut" in listing.tags
