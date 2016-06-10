#!/usr/bin/python

import urllib2
import json
from config import googleapi_maps_key, home

def get_distance(destinations):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?key=%(apikey)s&origins=%(home)s&destinations=%(destinations)s' % {'apikey':googleapi_maps_key,'home':home,'destinations':'+'.join(map(lambda ll:','.join(ll),destinations))}
    data=urllib2.urlopen(url).read()
    try:
        return json.loads(data)['rows'][0]['elements'][0]['duration']['value']
    except:
        print 'data=',data
        return None

if __name__=='__main__':
    f = open('canyons.json','r')
    data = json.load(f)
    f.close()
    for canyon in data:
        if not canyon.has_key('localisation') or not canyon['localisation'].has_key('distance'):
            print canyon['title'].encode('utf8')
            if canyon['localisation'].has_key('lat'):
                ll = (canyon['localisation']['lat'],canyon['localisation']['lon'])
                distance = get_distance([ll])
                print distance
                if distance!=None:
                    canyon['localisation']['distance']=distance

    json.dump(data,open('canyons.json','w'))
