from wudcutt.sources.metmuseum import MetMuseumSource


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class DummySession:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        for needle, payload in self.responses.items():
            if needle in url:
                return DummyResponse(payload)
        raise AssertionError(f"Unexpected URL: {url}")


def test_metmuseum_source_normalizes_search_results():
    session = DummySession(
        {
            "/search": {"objectIDs": [123, 456]},
            "/objects/123": {
                "title": "The Four Horsemen of the Apocalypse",
                "artistDisplayName": "Albrecht Durer",
                "objectDate": "ca. 1498",
                "medium": "Woodcut",
                "primaryImage": "https://images.metmuseum.org/123/original.jpg",
                "primaryImageSmall": "https://images.metmuseum.org/123/small.jpg",
                "objectURL": "https://metmuseum.org/art/collection/search/123",
                "isPublicDomain": True,
                "dimensions": "image: 39.0 x 28.5 cm",
                "tags": [{"term": "Horsemen"}, {"term": "Apocalypse"}],
                "repository": "The Metropolitan Museum of Art",
            },
            "/objects/456": {
                "title": "Missing Image Record",
                "artistDisplayName": "Unknown",
                "objectDate": "1500",
                "medium": "Woodcut",
                "primaryImage": "",
                "primaryImageSmall": "",
                "objectURL": "https://metmuseum.org/art/collection/search/456",
                "isPublicDomain": True,
                "dimensions": "",
                "tags": [],
                "repository": "The Metropolitan Museum of Art",
            },
        }
    )
    source = MetMuseumSource(session=session)

    candidates = source.search("four horsemen")

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.provider == "metmuseum"
    assert candidate.artist == "Albrecht Durer"
    assert candidate.license_label == "public domain"
    assert candidate.source_file_url.endswith("original.jpg")
