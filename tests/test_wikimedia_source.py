from wudcutt.sources.wikimedia import WikimediaSource


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
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return DummyResponse(self.payload)


def test_wikimedia_source_normalizes_search_results():
    payload = {
        "query": {
            "pages": {
                "1": {
                    "title": "File:Albrecht Dürer - The Rhinoceros (NGA 1964.8.697).jpg",
                    "imageinfo": [{
                        "url": "https://upload.wikimedia.org/file.jpg",
                        "width": 4096,
                        "height": 3203,
                        "extmetadata": {"LicenseShortName": {"value": "Public domain"}},
                    }],
                    "categories": [{"title": "Category:1515 woodcuts"}],
                },
                "2": {
                    "title": "File:Unknown licensed item.jpg",
                    "imageinfo": [{
                        "url": "https://upload.wikimedia.org/file2.jpg",
                        "width": 1000,
                        "height": 1000,
                        "extmetadata": {},
                    }],
                    "categories": [{"title": "Category:misc"}],
                },
            }
        }
    }
    session = DummySession(payload)
    source = WikimediaSource(session=session)

    candidates = source.search("durer rhinoceros")

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.provider == "wikimedia"
    assert candidate.title == "The Rhinoceros"
    assert candidate.artist == "Albrecht Dürer"
    assert candidate.year == "1515"
    assert candidate.slug == "durer-the-rhinoceros-1515"
    assert candidate.width == 4096
    assert candidate.license_label == "public domain"
    assert candidate.source_file_url == "https://upload.wikimedia.org/file.jpg"
