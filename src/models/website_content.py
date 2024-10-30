class WebsiteContent:
    def __init__(self, url="", language="", title="", headings="", texts=None, spans=None, images=None, links=None):
        self.url = url
        self.language = language
        self.title = title
        self.headings = headings
        self.texts = texts if texts is not None else []
        self.spans = spans if spans is not None else []
        self.images = images if images is not None else []
        self.links = links if links is not None else []
        
    def to_dict(self):
        return {
            "url": self.url,
            "language": self.language,
            "title": self.title,
            "headings": self.headings,
            "texts": self.texts,
            "spans": self.spans,
            "images": self.images,
            "links": self.links
        }