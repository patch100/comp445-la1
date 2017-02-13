import re

import sys

CRLF = "\r\n\r\n"

class request:

    def __init__(self, url, request_type):
        self.url = url
        self.request_type = request_type.upper()

        search = re.search("[a-z]+:\/\/(www\.)?([a-z.]*)(\/.*)?", url)
        self.query = search.group(3)
        self.host = "www."+search.group(2)
        self.addHeader("Host: " + self.host)

    def getURL(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getQuery(self):
        return self.query

    def setQuery(self, query):
        self.query = query

    def setHost(self, host):
        self.host = host

    def getHost(self):
        return self.host

    def getType(self):
        return self.request_type

    def setType(self, request_type):
        self.request_type = request_type

    def setVerbosity(self, v):
        self.verbosity = v

    def getVerbosity(self):
        return getattr(self, 'verbosity', None)

    def addHeader(self, header):
        if hasattr(self, 'headers'):
            self.headers.append(header)
        else:
            self.headers = [header]

    def getHeaders(self):
        if hasattr(self, 'headers'):
            header_string = ""
            for h in self.headers[:-1]:
                header_string += h + "\r\n"
            header_string += self.headers[-1]
            return header_string
        else:
            return ""

    def setInlineData(self, data):
        self.data = data

    def getInlineData(self):
        if hasattr(self, 'data'):
            return self.data
        else:
            return ""

    def setContentLength(self):
        size = 0
        if hasattr(self, 'data'):
            size = len(str(self.data))
        if hasattr(self, 'file'):
            file = open(self.file, 'rb').read()
            size = len(str(file))
        if(self.request_type == 'POST'):
            self.headers.append("Content-Length: %i" % size)

    def setFile(self, file):
        self.file = file

    def getFile(self):
        if hasattr(self, 'file'):
            return self.file
        else:
            return ""

    def getData(self):
        if hasattr(self, 'data'):
            return self.data

        if hasattr(self, 'file'):
            return open(self.file, 'rb').read()

        return ""


    def toString(self):
        self.setContentLength()
        return self.request_type + " " + self.query + " HTTP/1.0\r\n" + self.getHeaders() + "\r\nConnection: close\r\n\r\n" + self.getData()

