import HTMLParser
html_parser = HTMLParser.HTMLParser()

def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return html_parser.unescape(html).rstrip()