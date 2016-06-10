#!/usr/bin/python

from flask import Flask
import pymongo
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/search/<int:corde>/<int:tpstotal>")
def search(corde,tpstotal):
    out=[]
    cur = client['canyons']['canyons'].find({'tpstotal':{'$lte':3600*int(tpstotal)},'corde':{'$lte':int(corde)/2}},{"_id":0}).sort('interet',-1)
    for itm in cur:
        out.append(itm)
    print str(out)
    return json.dumps(out)

if __name__ == "__main__":
    client = pymongo.MongoClient()
    app.run(debug=True,port=30000)
