from urllib.parse import urljoin, urlparse
from flask import request

def checkIfSafeURL(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc