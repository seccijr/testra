import sys
import re
import mechanize
import urllib
import urllib2
import urlparse
import pprint
from bs4 import BeautifulSoup

if len(sys.argv) == 1:
    param = ''
else:
    param = sys.argv[1]

url = ["https", "sedeapl.dgt.gob.es", None, None, None, None]
consultaResource = "/WEB_TTRA_CONSULTA/Todos.faces"
visualizacionResource = "/WEB_TTRA_CONSULTA/ServletVisualizacion"

br = mechanize.Browser()
url[2] = consultaResource
url[4] = urllib.urlencode({"idioma": "es"})
br.open(urlparse.urlunparse(url))
assert br.viewing_html()
print br.title()
br.select_form(name="dato")
br["dato:BusInput"] = param
response = br.submit()
html = response.read()
href_str = re.findall(r'/WEB_TTRA_CONSULTA/VisualizacionEdicto\.faces\?params=.*?"', html)[0].replace('"', '')
href = urlparse.urlparse(href_str)

if href is not None:
    params = {"formato": "HTML"}
    query = dict(urlparse.parse_qsl(href[4]))
    query.update(params)
    url[2] = visualizacionResource
    url[4] = urllib.urlencode(query)
    html = urllib2.urlopen(urlparse.urlunparse(url))
    soup2 = BeautifulSoup(html)
    try:
        info = soup2.findAll('span', {
                                      'style': 'font-family: Verdana; color: #000000; font-size: 9px;'
        })
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
else:
    result = None

pprint.pprint(result)
