#!/usr/bin/python

import urllib2
import pymongo
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
    client = pymongo.MongoClient()
    for canyon in client['canyons']['canyons'].find({'localisation.distance':{'$exists':False}}):
        print canyon['title'].encode('utf8')
        if canyon['localisation'].has_key('lat'):
            ll = (canyon['localisation']['lat'],canyon['localisation']['lon'])
            distance = get_distance([ll])
            print distance
            if distance!=None:
                client['canyons']['canyons'].update({'_id': canyon['_id']},{'$set': {'localisation.distance': distance}}, upsert=False, multi=False)
