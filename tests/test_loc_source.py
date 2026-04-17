from wudcutt.sources.loc import LibraryOfCongressSource


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class DummySession:
    def __init__(self, payload):
        self.payload = payload

    def get(self, url, params=None, timeout=None):
        return DummyResponse(self.payload)


def test_loc_source_normalizes_results():
    payload = {
        "results": [
            {
                "title": "The rhinoceros",
                "contributor_names": ["Durer, Albrecht"],
                "date": "1515",
                "image_url": ["https://loc.gov/original.jpg"],
                "url": "https://loc.gov/item/123",
                "item": {"rights": "No known restrictions"},
                "subject": ["Woodcuts", "Animals"],
            }
        ]
    }
    source = LibraryOfCongressSource(session=DummySession(payload))

    candidates = source.search("rhinoceros")

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.provider == "loc"
    assert candidate.artist == "Durer, Albrecht"
    assert candidate.license_label == "public domain"
