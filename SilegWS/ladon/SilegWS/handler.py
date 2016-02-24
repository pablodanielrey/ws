# -*- coding: utf-8 -*-

from ladon.server.wsgi import LadonWSGIApplication
from os.path import abspath, dirname

application = LadonWSGIApplication(['SilegWS'],
  [dirname(abspath(__file__))],
  catalog_name='Catalogo del webservice del sileg',
  catalog_desc='Raiz del catálogo del webservice del sileg')
