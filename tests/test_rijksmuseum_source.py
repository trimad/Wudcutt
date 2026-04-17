from wudcutt.sources.rijksmuseum import RijksmuseumSource


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


def test_rijksmuseum_source_normalizes_results(tmp_path):
    payload = {
        "artObjects": [
            {
                "title": "The Four Horsemen of the Apocalypse",
                "principalOrFirstMaker": "Albrecht Durer",
                "dating": {"presentingDate": "1498"},
                "webImage": {"url": "https://rijksmuseum.nl/original.jpg", "width": 4500, "height": 3200},
                "links": {"web": "https://rijksmuseum.nl/object/1"},
                "objectTypes": ["print"],
            }
        ]
    }
    (tmp_path / "rijksmuseum.json").write_text(__import__("json").dumps(payload))
    source = RijksmuseumSource(fixture_dir=tmp_path)

    candidates = source.search("horsemen")

    assert len(candidates) == 1
    assert candidates[0].provider == "rijksmuseum"
    assert candidates[0].source_file_url.endswith("original.jpg")
