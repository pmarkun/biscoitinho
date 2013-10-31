import urllib2

def urlopen(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    xml = urllib2.urlopen(req)
    return xml