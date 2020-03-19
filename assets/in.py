#!/usr/local/bin/python
import json
import sys
import os
from os.path import join
import pymongo as pm
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from bson.objectid import ObjectId

def get_or_default(dictionary, key, default=''):
  try:
    return dictionary[key]
  except:
    return default

def msg(msg, *args, **kwargs):
  print(msg.format(*args, **kwargs), file=sys.stderr)

def _in(instream, dest='.'):
  payload = json.load(instream)

  msg('''IN
  Payload: {}
  ls: {}''', payload, os.listdir(dest))
  source = payload["source"]
  username=get_or_default(source, "username", "admin")
  password=get_or_default(source, "password", "admin")
  host=f'{source["url"]}:{source["port"]}'
  uri = "mongodb://%s:%s@%s" % (quote_plus(username), 
                                      quote_plus(password), host)

  connection = pm.MongoClient(uri)
  msg('Connection {}', connection)
  try:
    # The ismaster command is cheap and does not require auth.
    connection.admin.command('ismaster')
  except ConnectionFailure:
    msg("Server not available")                                        
  db = connection[source['db']]

  collection = db[source['collection']]

  concourse_input = payload['version']
  find = {'_id': ObjectId(concourse_input['version'])}  ### ERROR HERE ObjectId is not JSON serializable... try bson?
  cursor = collection.find(find)
  return {"version": cursor.next()}


if __name__ == "__main__":
    print(json.dumps(_in(sys.stdin)))