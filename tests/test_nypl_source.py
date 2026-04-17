from wudcutt.sources.nypl import NYPLSource


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

    def get(self, url, params=None, timeout=None, headers=None):
        return DummyResponse(self.payload)


def test_nypl_source_normalizes_results(tmp_path):
    payload = {
        "response": {
            "docs": [
                {
                    "title": "Dance of Death",
                    "creatorLiteral": "Hans Holbein",
                    "date": "1526",
                    "imageID": "12345",
                    "uuid": "abcde",
                    "typeOfResource": "still image",
                    "genre": ["woodcuts"],
                }
            ]
        }
    }
    (tmp_path / "nypl.json").write_text(__import__("json").dumps(payload))
    source = NYPLSource(fixture_dir=tmp_path)

    candidates = source.search("death")

    assert len(candidates) == 1
    assert candidates[0].provider == "nypl"
    assert candidates[0].preview_url.endswith("12345/full/1000,/0/default.jpg")
