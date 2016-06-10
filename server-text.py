#!/usr/bin/python

from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/search/<int:corde>/<int:tpstotal>")
def search(corde,tpstotal):
    out=[]
    print 'lendata',len(data)
    for itm in data:
        #print itm['corde']
        if itm.has_key('tpstotal'):
            print itm['tpstotal']
        if itm.has_key('tpstotal') and itm['tpstotal']<=3600*int(tpstotal) and itm['corde']<=int(corde)/2:
            out.append(itm)
    out.sort(key=lambda itm:itm['interet'],reverse=True)
    #cur = client['canyons']['canyons'].find({'tpstotal':{'$lte':3600*int(tpstotal)},'corde':{'$lte':int(corde)/2}},{"_id":0}).sort('interet',-1)
    #for itm in cur:
    #    out.append(itm)
    print str(out)
    return json.dumps(out)

if __name__ == "__main__":
    f = open('canyons.json','r')
    data = json.load(f)
    f.close()
    app.run(host='localhost',port=30000,debug=True)
