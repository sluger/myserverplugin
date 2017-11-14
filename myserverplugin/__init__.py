###############################################################################
# Caleydo - Visualization for Molecular Biology - http://caleydo.org
# Copyright (c) The Caleydo Team. All rights reserved.
# Licensed under the new BSD license, available at http://caleydo.org/license
###############################################################################


def phovea(registry):
  """
  register extension points
  :param registry:
  """
  # generator-phovea:begin
  registry.append('namespace', 'hello_world', 'myserverplugin.hello_world', {
   'namespace': '/api/hello_world'
  })


  registry.append('tdp-sql-database-definition', 'mydb', 'myserverplugin.mydb', {
   'configKey': 'myserverplugin'
  })


  registry.append('mapping_provider', 'my_mapping_provider', 'myserverplugin.mymappingprovider', {})


  registry.append('namespace', 'hello-rest', 'myserverplugin.hello_rest', {
   'namespace': '/api/hello_rest'
  })
  # generator-phovea:end
  pass


def phovea_config():
  """
  :return: file pointer to config file
  """
  from os import path
  here = path.abspath(path.dirname(__file__))
  config_file = path.join(here, 'config.json')
  return config_file if path.exists(config_file) else None
