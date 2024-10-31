# title of the page
def title(soup):
    title = soup.title.string
    return title

# all headings of the page
def headings(soup):
    headings = [heading.get_text() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    return headings

# all texts of the page (filtered for cookie-related texts)
def texts(soup):
    footer = soup.body.find('footer')
    if footer:
        footer.extract()

    texts = [text.get_text() for text in soup.find_all('p')]

    filtered_texts = filter_texts(texts)
    return filtered_texts

# alt text of all images of the page
def images(soup):
    img_tags = soup.find_all('img')
    image_list = []
    for img in img_tags:
        alt_text = img.get('alt', '')
        image_list.append(alt_text)
    return image_list

# all text within span tags of the page
def span_texts(soup):
    spans_with_text = [span.get_text() for span in soup.find_all('span') if span.string]
    return spans_with_text

# all links on the page
def links(soup):
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links

# filters out cookie-related texts
def filter_texts(texts):
    # Define keywords to filter out cookie-related texts
    cookie_keywords = ["decline", "accept", "consent", "preference", "tracking", "analytics"]
    # Filter texts to remove cookie-related messages
    filtered_texts = [text for text in texts if not (
        ('cookie' in text.lower() or 'cookies' in text.lower()) and
        any(keyword in text.lower() for keyword in cookie_keywords)
    )]
    return filtered_texts