from wudcutt.sources.wellcome import WellcomeSource


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


def test_wellcome_source_normalizes_results():
    payload = {
        "results": [
            {
                "id": "xyz",
                "title": "A monstrous beast",
                "contributors": [{"agent": {"label": "Unknown engraver"}}],
                "production": [{"date": "1650"}],
                "genres": [{"label": "Woodcuts"}],
                "images": [{"locations": [{"url": "https://iiif.wellcomecollection.org/image.jpg"}]}],
                "type": "Visual materials",
                "source": {"url": "https://wellcomecollection.org/works/xyz"},
                "license": {"label": "Public Domain Mark"},
            }
        ]
    }
    source = WellcomeSource(session=DummySession(payload))

    candidates = source.search("beast")

    assert len(candidates) == 1
    assert candidates[0].provider == "wellcome"
    assert candidates[0].license_label == "public domain"
