import parsing.html_parser as html_parser
from models.website_content import WebsiteContent

# Parses content from HTML and initializes WebsiteContent
def parse_website_content(soup, url):
    website_content = WebsiteContent(
        url=url,
        title=html_parser.title(soup),
        headings=html_parser.headings(soup),
        main_texts=html_parser.texts(soup),
        other_texts=html_parser.span_texts(soup),
        images=html_parser.images(soup),
        links=html_parser.links(soup),
    )
    return website_content.to_dict()