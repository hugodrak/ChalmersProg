import urllib.request

def get_web_text(url):
    resp = urllib.request.urlopen(url)
