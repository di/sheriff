#!/usr/bin/python

import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template
from curlers import curlers

app=Flask(__name__)

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)

    def decorate(func):
        lastTimeCalled = [0.0]

        def rateLimitedFunction(*args, **kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

def in_zip(a2, z):
    return a2.split(' ')[-1].split("-")[0] == z

class Property():

    def __init__(self, a1, a2, brt, bid, status, neighbors):
        self.a1 = a1
        self.a2 = a2
        self.brt = brt
        self.bid = bid
        self.status = status
        self.neighbors = neighbors

class Listing():

    def __init__(self, name, date, properties):
        self.name = name
        self.date = date
        self.properties = properties


@RateLimited(0.5)
def get_assessment(url):
    return requests.get(url)

def has_lot(a1):
    api_url = "http://api.phila.gov/opa/v1.0/address/%s/?format=json"
    spl = a1.split(' ')
    if "-" in spl[0]:
        return "---", "---"
    left = ' '.join([str(int(spl[0])-2)] + spl[1:])
    right = ' '.join([str(int(spl[0])+2)] + spl[1:])
    r_left = get_assessment(api_url % left)
    try :
        r_left_desc = r_left.json()["data"]["properties"][0]["characteristics"]["description"]
    except:
        r_left_desc = "May not exist"
    r_right = get_assessment(api_url % right)
    try:
        r_right_desc = r_right.json()["data"]["properties"][0]["characteristics"]["description"]
    except:
        r_right_desc = "May not exist"
    return "%s (%s)" % (left, r_left_desc), "%s (%s)" % (right, r_right_desc)

@app.route("/")
def index():
    url = "http://144.202.209.2/sheriff.salelisting/frameview.aspx"
    listings = []
    for r in curlers:
        properties = []
        bs = BeautifulSoup(r.text)
        for prop in bs.find("table", id="dgSaleListing").find_all("tr")[1:]:
            col = prop.find_all("td")
            a1 = col[3].contents[0]
            a2 = col[3].contents[1].contents[0]
            brt = col[3].contents[1].contents[1].contents[0].split(' ')[-1]
            bid = col[4].text
            status = col[5].text
            if in_zip(a2, '19104'):
                left, right = has_lot(a1)
                properties.append(Property(a1, a2, brt, bid, status, [left, right]))
        listing_name = bs.find("select", id="ddlSaleCategory").find("option", selected=True).text
        listing_date = bs.find("select", id="ddlSaleDates").find("option", selected=True).text
        listings.append(Listing(listing_name, listing_date, properties))
    return render_template("view.html", listings=listings)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_debugger=True, use_reloader=True)
