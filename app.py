from flask import Flask,request,url_for,redirect,render_template
import json, urllib2
app=Flask(__name__)

def query(s):
    return s.replace(" ", "%20")
@app.route("/")
def index():
    return "hello"


@app.route("/t")
@app.route("/t/<tag>")
def t(tag="Harry%20Potter"):
    url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=RichardZ-f87b-4d7d-a4c3-966a1890f59e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=%s"
    url = url%(tag)
    request = urllib2.urlopen(url)
    result = request.read()
    d = json.loads(result)
    page = ""
    for r in d["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
        print r["listingInfo"][0]["listingType"][0]
        if r["country"][0] == 'US' and r["listingInfo"][0]["listingType"][0] != "Auction":
            page = page + r["title"][0] + "<br>Price: $" + r["sellingStatus"][0]["currentPrice"][0]["__value__"]# + " + Shipping: $" + r["shippingInfo"][0]["shippingServiceCost"][0]["__value__"]
            page = page + "<hr>"
        #break
    return page



if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8000)


#http://open.api.ebay.com/shopping?appid=RichardZ-f87b-4d7d-a4c3-966a1890f59e &version=517 &siteid=0 &callname=FindItems &QueryKeywords=ipod &responseencoding=JSON &callback=true
#http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=RichardZ-f87b-4d7d-a4c3-966a1890f59e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=harry%20potter%20phoenix
