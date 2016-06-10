#!/usr/bin/python

import scrapy
import urlparse
import urllib2
from xml.dom.minidom import parseString
from config import place_to_scrap

class BlogSpider(scrapy.Spider):
    name = 'canyonspider'
    start_urls = ['http://www.descente-canyon.com/canyoning/lieu/%s'%place_to_scrap]

    def parse(self, response):
        for href in response.css('#table-1 > tbody > tr > td a::attr(href)'):
            full_url = urlparse.urljoin(response.url, href.extract())
            if full_url.startswith('http://www.descente-canyon.com/boutique/') or full_url.startswith('http://www.descente-canyon.com/canyoning/topoguide/'):
                continue
            cid = href.extract().split('/')[3]
            #geo = scrapy.Request('http://www.descente-canyon.com/canyoning/localized-point-search?t=xml2&idc='+cid[1:], callback=self.parse_geo)
            infos = scrapy.Request(full_url, callback=self.parse_canyon, meta={'cid':cid})
            yield infos
            #yield geo

    def parse_canyon(self, response):
        #print 'cid ',response.meta['cid']
        #print 'geourl ','http://www.descente-canyon.com/canyoning/localized-point-search?t=xml2&idc='+response.meta['cid'][1:]
        #print 'geoxml ',urllib2.urlopen('http://www.descente-canyon.com/canyoning/localized-point-search?t=xml2&idc='+response.meta['cid'][1:]).read()

        location={}
        title = response.css('h1::text')[0].extract()
        try:
            interet = float(filter(lambda x:not(x.startswith("Attention")),response.css('.fichetechnique strong::text').extract())[0])
        except:
            interet = -1
        #cotation = response.css('table.fichetechnique td.valeur > a::text').extract()[0]
        #valeurs = response.css('table.fichetechnique td.valeur::text').extract()
        valeurs = []
        for valeur in response.css('table.fichetechnique td.valeur'):
            #print 'valeur ',valeur
            for a in valeur.css('a::text'):
                valeurs.append(a.extract())
            for t in valeur.css('td::text'):
                valeurs.append(t.extract())
        #print 'valeurs ',valeurs
        if len(valeurs)!=10:
            print 'error valeurs ',response.url
        altdep,cotation,aller,deniv,longcorde,descente,longueur,retour,cascade,navette=valeurs

        geodoc = parseString(urllib2.urlopen('http://www.descente-canyon.com/canyoning/localized-point-search?t=xml2&idc='+response.meta['cid'][1:]).read())
        for marker in geodoc.getElementsByTagName('marker'):
            lat = marker.getAttributeNode('lat').nodeValue
            lon = marker.getAttributeNode('lng').nodeValue
            label = marker.getAttributeNode('label').nodeValue
            if label.startswith('parking'):
                location={'lat':lat,'lon':lon,'nature':'parking'}
                break
            if label.startswith('depart'):
                location={'lat':lat,'lon':lon,'nature':'depart'}
            if label.startswith('arrivee'):
                location={'lat':lat,'lon':lon,'nature':'arrivee'}

        return {'localisation':location,'title':title,'interet':interet,'alt':altdep,'cot':cotation,'aller':aller,'deniv':deniv,'corde':longcorde,'descente':descente,'lg':longueur,'ret':retour,'cascade':cascade,'navette':navette}
