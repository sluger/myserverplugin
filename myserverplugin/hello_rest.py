###############################################################################
# Caleydo - Visualization for Molecular Biology - http://caleydo.org
# Copyright (c) The Caleydo Team. All rights reserved.
# Licensed under the new BSD license, available at http://caleydo.org/license
###############################################################################

from phovea_server.ns import Namespace, request, abort
from phovea_server.util import jsonify
import logging

app = Namespace(__name__)
_log = logging.getLogger(__name__)


@app.route('/')
def _hello():
  return jsonify({
    'message': 'Hello World'
  })

@app.route('/greet/<path:name>')
def _greet(name):
  lang = request.values.get('lang', 'en')
  template = ''
  if lang == 'en':
    template = 'Hello {name}'
  elif lang == 'de':
    template = 'Hallo {name}'
  elif lang == 'es':
    template = 'Hola {name}'
  else:
    abort(400, 'invalid language: ' + lang)

  return jsonify({
    'message': template.format(name=name)
  })


def create():
  return app
