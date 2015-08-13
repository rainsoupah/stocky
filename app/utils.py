import HTMLParser
html_parser = HTMLParser.HTMLParser()

def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return html_parser.unescape(html).rstrip()

def toNum(s):
	try: 
		return float(s.replace(',', ''))
	except:
		if s == '-': return 0		# if it doesn't exist, then assume 0.
		return s