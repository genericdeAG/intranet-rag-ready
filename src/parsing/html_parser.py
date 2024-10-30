
def language(soup):
    lang = soup.html.get('lang')
    print(f'Language of the page: {lang}\n')
    return lang

def title(soup):
    title = soup.title.string
    print(f'Title of the page: {title}\n')
    return title

def headings(soup):
    headings = [heading.get_text() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    print(f'Headings of the page: {headings}\n')
    return headings

def texts(soup):
    footer = soup.body.find('footer')
    if footer:
        footer.extract()

    texts = [text.get_text() for text in soup.find_all('p')]

    filtered_texts = filter_texts(texts)
    print(f'Texts of the page after filtering: {filtered_texts}\n')
    return filtered_texts

def images(soup):
    img_tags = soup.find_all('img')
    image_list = []
    for img in img_tags:
        alt_text = img.get('alt', '')
        image_list.append(alt_text)
    print(f'Images of the page (alt text): {image_list}\n')
    return image_list

    
def span_texts(soup):
    spans_with_text = [span.get_text() for span in soup.find_all('span') if span.string]
    print(f'Spans with text: {spans_with_text}\n')
    return spans_with_text

def links(soup):
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    print(f'Links of the page: {links}\n')
    return links

def filter_texts(texts):
    # Define keywords to filter out cookie-related texts
    cookie_keywords = ["decline", "accept", "consent", "preference", "tracking", "analytics"]
    # Filter texts to remove cookie-related messages
    filtered_texts = [text for text in texts if not (
        ('cookie' in text.lower() or 'cookies' in text.lower()) and
        any(keyword in text.lower() for keyword in cookie_keywords)
    )]
    return filtered_texts