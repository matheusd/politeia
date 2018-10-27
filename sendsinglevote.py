#!/usr/bin/env python3

import sys
import urllib.request
import urllib.error

DEBUG = False 

def main(votefile, piwww):
    # debug my current ip
    if DEBUG:
        res = urllib.request.urlopen("https://wtfismyip.com/text")
        print("My ip: ", res.read())

    processor = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(processor)

    # acquire csrf
    res = opener.open("%s" % piwww)
    #print(res.info(), res.read())
    csrf = res.info().get("X-Csrf-Token")

    opener.addheaders = [("X-Csrf-Token", csrf)]
    
    # send vote
    with open(votefile, mode="rb") as f:
        data = f.read()

    try:
        url = "%s/v1/proposals/castvotes" % piwww
        res = opener.open(url, data)
        print(res.read())
    except urllib.error.HTTPError as httpErr:
        print(httpErr.info(), httpErr.read())
        sys.exit(1)
    except e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s votefile politeia-www-url" % sys.argv[0])
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
