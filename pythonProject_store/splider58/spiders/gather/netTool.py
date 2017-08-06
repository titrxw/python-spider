import gzip
from StringIO import StringIO
# import zlib

class NetTool:
    @classmethod
    def getDoMain(cls,url):
        reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
        m = re.match(reg, url)
        uri = m.groups()[0] if m else ''
        return uri
    @classmethod
    def uzip(data):
        buf = StringIO(data)
        f = gzip.GzipFile(fileobj=buf)
        return f.read()