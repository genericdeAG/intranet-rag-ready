class WebsiteContent:
    def __init__(self, url="", title="", headings="", main_texts=None, other_texts=None, images=None, links=None):
        self.url = url
        self.title = title
        self.headings = headings
        self.main_texts = main_texts if main_texts is not None else []
        self.other_texts = other_texts if other_texts is not None else []
        self.images = images if images is not None else []
        self.links = links if links is not None else []
        
    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "headings": self.headings,
            "main_texts": self.main_texts,
            "other_texts": self.other_texts,
            "images": self.images,
            "links": self.links
        }