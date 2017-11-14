import logging
from tdp_core import db

_log = logging.getLogger(__name__)

def _find_engine(db_connector):
 """
 find the registered SQLAlchemy engine given a registered db connector name
 :param db_connector: name of the db connector
 :return: SQLAlchemy engine instance
 """
 _, engine = db.configs.get(db_connector)
 return engine

class MyMappingTable(object):
 def __init__(self):
  self.from_idtype = 'MyIDType'
  self.to_idtype = 'MyOtherIDType'

 def __call__(self, ids):
  """
  maps the given ids to the output id type
  :param ids: the list of input id strings
  :return: a list of string lists one for each id, empty array indicate that for this specified id no mapping was found
  """
  return [[id] for id in ids]


class MyDBMappingTable(object):
 def __init__(self):
  self.from_idtype = 'MyIDType'
  self.to_idtype = 'IDTypeB'
  self._engine = _find_engine('mydb')

 def __call__(self, ids):
  from itertools import groupby

  # use the TDP db module session factor to create a session that is automatically closed afterwards
  with db.session(self._engine) as session:
   mapping = session.execute('SELECT my_id as f, b_id as t FROM myid2idtypeb WHERE my_id in :ids ORDER BY my_id', ids=ids)

  result = {}
  for id, rows in groupby(mapping, lambda row: row['f']):
   bs = [row['t'] for row in rows]
   result[id] = bs
   
  return [result.get(id, []) for id in ids]


class MyMappingProvider(object):
 """
 a mapping provider extension can implement multiple mapping tables at once, i.e. register multiple mappings for different types
 """

 def __init__(self):
   self.mapper = [MyMappingTable(), MyDBMappingTable()]

 def __iter__(self):
   """
   returns an iterable of all available mapper of this mapping provider
   :return: iterator that returns a tuple like (from_idtype, to_idtype, function doing the mapping)
   """
   return iter(((f.from_idtype, f.to_idtype, f) for f in self.mapper))


def create():
 return MyMappingProvider()