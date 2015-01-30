#!/usr/bin/python

import sys
import re
import mechanize
import urllib
import urllib2
import urlparse
import pprint
from bs4 import BeautifulSoup

class Testra:
    url = ["https", "sedeapl.dgt.gob.es", None, None, None, None]
    consultaResource = "/WEB_TTRA_CONSULTA/Todos.faces"
    visualizacionResource = "/WEB_TTRA_CONSULTA/ServletVisualizacion"
    
    def parseEdicto(self, html):
        soup = BeautifulSoup(html)
        try:
            info = soup.findAll('span', { 'style': ('font-family:'
                                                     ' Verdana;'
                                                     ' color: #000000;'
                                                     ' font-size: 9px;') })
            result = dict({
                           'expediente': info[0].text, 
                           'titular': info[1].text, 
                           'nif': info[2].text, 
                           'localidad': info[3].text, 
                           'fecha': info[4].text, 
                           'matricula': info[5].text, 
                           'cantidad': info[6].text, 
                           'precepto': info[7].text
                           })
        except IndexError:
            result = None
            
        return result

    def getConsulta(self, href):
        url = self.url
        params = {"formato": "HTML"}
        query = dict(urlparse.parse_qsl(href[4]))
        query.update(params)
        url[2] = self.visualizacionResource
        url[4] = urllib.urlencode(query)
        html = urllib2.urlopen(urlparse.urlunparse(url))
        result = self.parseEdicto(html)
        
        return result
    
    def searchEdictos(self, param):
        url = self.url
        br = mechanize.Browser()
        url[2] = self.consultaResource
        url[4] = urllib.urlencode({"idioma": "es"})
        br.open(urlparse.urlunparse(url))
        assert br.viewing_html()
        br.select_form(name="dato")
        br["dato:BusInput"] = param
        response = br.submit()
        html = response.read()
        
        return html
    
    def getEdictosUrl(self, html):
        reg = re.compile(('/WEB_TTRA_CONSULTA'
                          '/VisualizacionEdicto'
                          '\.faces\?params=.*?"'))
        href_str = reg.findall(html)[0].replace('"', '')
        href = urlparse.urlparse(href_str)
        
        return href
        
    
    def main(self, param):
        edictos = self.searchEdictos(param)
        href = self.getEdictosUrl(edictos)
        if href is not None:
            result = self.getConsulta(href)
        else:
            result = None
            
        pprint.pprint(result)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage: testra.py [pattern]'
        exit(1)
    else:
        param = sys.argv[1]
        testra = Testra()
        testra.main(param)
        exit(0)

