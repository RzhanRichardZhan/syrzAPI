from flask import Flask,request,url_for,redirect,render_template
import json, urllib, urllib2, math, statistics
app=Flask(__name__)



def query(s):
	return s.replace(" ", "%20")
def totupledictionary(d):
	result = [(x,d[x]) for x in d.keys()]
	return sorted(result,key=lambda count: count[1],reverse=True)
def expense(L):
	stuff=[float(x) for x in L]
	return (max(stuff),statistics.median(stuff),min(stuff),statistics.stdev(stuff))

@app.route("/", methods=["GET"])
def index():
	if request.method == "GET" and request.args.get("submit",None)=="yes":
		return redirect("/t/%s"%request.args.get("q",None))
	return render_template("home.html",error="")


@app.route("/t")
@app.route("/t/<tag>")
def t(tag):
	if request.args.get("submit",None)=="yes":
		return redirect("/t/%s"%request.args.get("q",None))
	elif (request.args.get("original_query") == None):
		tag_url = urllib.quote(tag)
		url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=RichardZ-f87b-4d7d-a4c3-966a1890f59e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=%s"
		url = url%(tag_url)
		d = json.load(urllib2.urlopen(url))
		if d["findItemsByKeywordsResponse"][0]["searchResult"][0]["@count"]=="0":
			return render_template("home.html",error="No Search Results")
		page = ""
		items = []
		prices = []
		attributes = {}
		for r in d["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
			if r["country"][0] == 'US' and r["listingInfo"][0]["listingType"][0] != "Auction":
				items.append([r["title"][0], r["sellingStatus"][0]["currentPrice"][0]["__value__"], r["shippingInfo"][0]["shippingServiceCost"][0]["__value__"] if "shippingServiceCost" in r["shippingInfo"][0] else "", r["viewItemURL"][0]])
				prices.append(r["sellingStatus"][0]["currentPrice"][0]["__value__"])
				item_attributes = r["title"][0].split(" ")
				for attribute in item_attributes:
					attribute = attribute.lower()
					if attribute not in tag.lower():
						if attribute not in attributes:
							attributes[attribute]=1
						else:
							attributes[attribute]=attributes[attribute]+1
					
			
		return render_template("tag.html", attributes = totupledictionary(attributes),prices=expense(prices), page = items)
	else:
		if (request.args.get("original_query") == "True"):
			return redirect("/t/" + tag + " " + " ".join(request.args.getlist("attributes")))
		else:
			return redirect("/t/" + " ".join(request.args.getlist("attributes")))

if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0",port=8000)


#http://open.api.ebay.com/shopping?appid=RichardZ-f87b-4d7d-a4c3-966a1890f59e &version=517 &siteid=0 &callname=FindItems &QueryKeywords=ipod &responseencoding=JSON &callback=true
#http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=RichardZ-f87b-4d7d-a4c3-966a1890f59e&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=harry%20potter%20phoenix
