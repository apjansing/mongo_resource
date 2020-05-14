#!/usr/local/bin/python
import json
import sys
import os
from os.path import join
import pymongo as pm
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from common import get_or_default, msg, get_payload_data

def update_record(filee, collection):
  with open(filee, 'r') as f:
    try:
      record = json.load(f)
      if '_id' in record.keys() and len(list(collection.find({'_id': ObjectId(record['_id'])}))) > 0:
        id = record['_id']
        del record['_id']
        msg('''record {}''', record)
        collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': record}, upsert=True)  ##pymongo.errors.WriteError: After applying the update, the (immutable) field '_id' was found to have been altered to _id: "5e76a3617be93507462b81b9"
      else: 
        collection.insert_one(record)
    except:
      raise Exception

def updated_records(path, collection):
  for filee in os.listdir(path):
    update_record(join(path,filee), collection)

def _out(instream, src='.'):
  payload = json.load(instream)
  msg('''OUT
  Payload: {}
  ls: {}''', payload, os.listdir(src))
  source, uri = get_payload_data(payload)

  connection = pm.MongoClient(uri)
  msg('Connection {}', connection)
  try:
    # The ismaster command is cheap and does not require auth.
    connection.admin.command('ismaster')
  except ConnectionFailure:
    msg("Server not available")
                                   
  db = connection[source['db']]
  collection = db[source['collection']]
  path = join(src, payload['params']['path'])
  if os.path.isdir(path):
    updated_records(path, collection)
    files = os.listdir(path)
    if len(files) == 1:
      msg('{}', files)
      return {"version": {"version": files[0].split('.')[0]}}
    msg('123 {}', files)
    return {"version": {"version": [f.split('.')[0] for f in os.listdir(path)]}}
  elif os.path.isfile(path):
    update_record(path, collection)
    return {"version": {"version": path.split('.')[0]}}
  elif not os.path.exists(path):
    msg('File {} not found! Please evaluated your *path* parameter.', path)
    raise Exception
  else:
    msg('File {} found, but could not be inserted into Mongo Databse.', path)
    raise Exception

if __name__ == "__main__":
  print(json.dumps(_out(sys.stdin, sys.argv[1])))
