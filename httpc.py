import json
import re
import socket
import argparse
import sys
from httplib import HTTPResponse

from request import request

def run_client(new_request):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = new_request.getHost()
    port = 80
    requestURL = new_request.toString().encode("utf-8")

    try:
        conn.connect((host, port))
        sys.stdout.write(requestURL + new_request.getFile())
        conn.sendall(requestURL)
        response = conn.recv(1024, socket.MSG_WAITALL)
        if(new_request.getVerbosity() is not None):
             sys.stdout.write(response.decode("utf-8"))
        else:
            sys.stdout.write("Replied: " + re.search("({[\S\s]*})", response.decode("utf-8")).group(1))
    finally:
        conn.close()

def create_request():
    r = request(args.URL, args.request_type)

    if args.v:
        r.setVerbosity(True)
    if args.header:
        for h in args.header:
            search = re.search("(\w+-\w+):(\w+\/\w+)", h)
            if(search is None):
                r.addHeader(h)
            else:
                r.addHeader(search.group(1) + ":" + search.group(2))
    if args.d:
        r.setInlineData(args.d)
    if args.j:
        r.setInlineData(args.j)
    if args.f:
        r.setFile(args.f)

    return r



parser = argparse.ArgumentParser(description='Socket based HTTP Client')

# positional arguments
parser.add_argument('request_type', help="type of request, GET or POST", choices=['GET', 'get', 'post', 'POST'])

# optional arguments
parser.add_argument("-v", help="enable verbosity", action='store_true')
parser.add_argument("--header", help="HTTP headers of format \"key:value\"", action='append')
parser.add_argument("-j", help="add inline json data", type=json.loads)
parser.add_argument("-d", help="add inline data", type=str)
parser.add_argument("-f", help="add file", type=str)

# positional arguments
parser.add_argument("URL", help="URL to send request to")

args = parser.parse_args()
new_request = create_request()
run_client(new_request)
