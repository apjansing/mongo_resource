#!/usr/local/bin/python
import json
import sys
import os
import pymongo as pm
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from pprint import pprint
from bson import ObjectId

def get_or_default(dictionary, key, default=''):
  try:
    return dictionary[key]
  except:
    return default

def msg(msg, *args, **kwargs):
  if isinstance(msg, dict):
    pprint(msg, stream=sys.stderr)
  else:
    print(msg.format(*args, **kwargs), file=sys.stderr)

def get_versions(version):
  if os.path.exists('versions.json'):
    with open('versions.json', 'r') as f:
      versions = json.load(f)
  else:
    versions = {'versions': []}
  return versions

def update_versions(id, versions):
  versions['versions'] += [id]
  with open('versions.json', 'w') as f:
    json.dump(versions, f)

def _check(instream):
  payload = json.load(instream)
  source = payload["source"]
  try:
    versions = get_versions(payload['version'])
  except:
    versions = {'versions': []}
  msg('''Payload {}
  Source {}
  Versions {}
  ''', payload, source, versions)
  # if len(versions['versions']) > 2:
  #   raise Exception

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
  find = dict(source['find'])
  if len(versions['versions']) > 0:
    find = {**find, **{'_id': {'$nin': versions['versions']}}}
  cursor = list(collection.find(find))

  for c in cursor:
    id = str(c['_id'])
    if id not in versions['versions']:
      update_versions(id, versions)
      return [{"version" : id}]
  

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))