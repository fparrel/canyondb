#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

def time2sec(tps):
    print tps.encode('utf8')
    if tps=='5/10min':
        return 600
    elif tps=='10/15min':
        return 15*60
    elif tps=='15/20min':
        return 1200
    elif tps=='10min/30mi':
        return 20*60
    elif tps=='...' or tps=='??':
        return None
    elif tps.endswith('ant'):
        return 0
    elif tps.encode('utf8')=='2 à 3 h':
        return 3600*2.5
    elif tps.encode('utf8')=='6 à 8 h':
        return 3600*7
    elif tps=='30min/1h45':
        return 3600+45*60
    elif tps=='4h/5h' or tps=='4-5h':
        return 3600*4.5
    elif tps=='4/6h':
        return 3600*5
    elif tps=='45m':
        return 45*60
    if tps.endswith('.'):
        tps=tps[:-1]
    s = tps.split('h')
    if len(s)==1:
        if s[0].endswith('min'):
            h=0
            min=int(s[0][:-3])
        else:
            h=int(s[0])
            min=0
    elif len(s)==2:
        h=int(s[0])
        if s[1].endswith('min'):
            min=int(s[1][:-3])
        else:
            if len(s[1].strip())>0:
                min=int(s[1])
            else:
                min = 0
    print h,min
    return h*3600+min*60

if __name__=='__main__':
    f = open('canyons.json','r')
    data = json.load(f)
    f.close()

    for canyon in data:
        if not canyon.has_key('tpstotal'):
            print canyon['title'].encode('utf8')
            try:
                tpstotal = canyon['aller']+canyon['descente']+canyon['ret']+2*canyon['localisation']['distance']
                print tpstotal
                canyon['tpstotal']=tpstotal
            except:
                pass

    for canyon in data:
        if isinstance(canyon['corde'],basestring):
            if canyon['corde'].endswith('m'):
                print canyon['title'].encode('utf8'),int(canyon['corde'][:-1])
                canyon['corde']=int(canyon['corde'][:-1])

    for canyon in data:
        if isinstance(canyon['aller'],basestring):
            print canyon['title'].encode('utf8')
            aller= time2sec(canyon['aller'])
            ret= time2sec(canyon['ret'])
            descente= time2sec(canyon['descente'])
            #if canyon['corde'].endswith('m'):
            #    print canyon['title'].encode('utf8'),int(canyon['corde'][:-1])
            canyon['aller']=aller
            canyon['ret']=ret
            canyon['descente']=descente

    json.dump(data,open('canyons.json','w'))
