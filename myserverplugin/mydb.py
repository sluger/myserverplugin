from tdp_core.dbview import DBViewBuilder, DBConnector, add_common_queries, inject_where, DBMapping

# idtype of our rows
idtype = 'MyIDType'
# columns of our mytable, it is used to verify dynamic parameters
columns = ['name', 'cat', 'value']

mappings = [
 DBMapping('MyIDType', 'IDTypeB', """SELECT my_id as f, b_id as t FROM myid2idtypeb WHERE my_id in :ids""")
]

# main dictionary containing all views registered for this plugin
views = dict()

# register a view that computes a score for each item based on a given my_id
views['mytable_single_score'] = DBViewBuilder().idtype('IDTypeA') \
.query("""
  SELECT a_id as id, value AS score
  FROM mytable_scores e
  WHERE e.my_id = :my_id""") \
.arg('my_id') \
.call(inject_where) \
.build()

# register the view for getting the mytable itself
views['mytable'] = DBViewBuilder().idtype(idtype).table('mytable') \
 .query("""SELECT my_id as id, * FROM mytable""") \
 .derive_columns() \
 .column('cat', type='categorical') \
 .assign_ids() \
 .call(inject_where) \
 .build()

# create a set of common queries
add_common_queries(views, 'mytable', idtype, 'my_id as id', columns)

# register a view that computes a score for each item based on a given my_id
views['mytable_single_score'] = DBViewBuilder().idtype('IDTypeA') \
 .query("""
  SELECT a_id as id, value AS score
  FROM mytable_scores e
  WHERE e.my_id = :my_id""") \
 .arg('my_id') \
 .call(inject_where) \
 .build()

def custom_callback(engine, arguments, filter):
 """
 custom query implementation
 :param engine: the SQLAlchemy engine
 :param arguments: a dictionary of valid arguments
 :param filter: a dictionary of valid filter key:value[] entries
 :return: an array of dictionaries
 """
 import pandas as pd
 data = pd.read_sql("""SELECT cat, value FROM mytable""", engine)
 grouped = data.groupby('cat').sum()
 return grouped.to_dict('records')

views['callback'] = DBViewBuilder() \
 .callback(custom_callback) \
 .build()

def create():
 """
 factory method to build this extension
 :return:
 """
 connector = DBConnector(views, mappings=mappings)
 connector.description = 'sample connector to the mydb.sqlite database'
 return connector