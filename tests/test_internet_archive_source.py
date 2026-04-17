from wudcutt.sources.internet_archive import InternetArchiveSource


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

    def get(self, url, params=None, timeout=None):
        for needle, payload in self.responses.items():
            if needle in url:
                return DummyResponse(payload)
        raise AssertionError(f"Unexpected URL: {url}")


def test_internet_archive_source_normalizes_results():
    session = DummySession({
        "advancedsearch": {
            "response": {
                "docs": [
                    {
                        "identifier": "durerhorsemen",
                        "title": "The Four Horsemen",
                        "creator": "Albrecht Durer",
                        "year": "1498",
                        "mediatype": "image",
                        "rights": "Public domain",
                        "subject": ["woodcut", "apocalypse"],
                    }
                ]
            }
        },
        "metadata/durerhorsemen": {
            "files": [
                {"name": "four-horsemen.jpg", "format": "JPEG"}
            ]
        },
    })
    source = InternetArchiveSource(session=session)

    candidates = source.search("horsemen")

    assert len(candidates) == 1
    assert candidates[0].provider == "internet_archive"
    assert "archive.org" in candidates[0].source_page_url
    assert candidates[0].source_file_url.endswith("four-horsemen.jpg")
