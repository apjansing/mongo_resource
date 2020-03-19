#!/usr/local/bin/python
import json
import sys
import pymongo as pm
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus

def get_or_default(dictionary, key, default=''):
  try:
    return dictionary[key]
  except:
    return default

def msg(msg, *args, **kwargs):
    print(msg.format(*args, **kwargs), file=sys.stderr)

def _check(instream):
    payload = json.load(instream)
    msg('Payload {}', payload)
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
    find = source['find']
    cursor = collection.find(dict(find))
    for _ in range(cursor.count()):
        current = cursor.next()
        return [{"version" : str(current["_id"])}]
    

if __name__ == "__main__":
    print(json.dumps(_check(sys.stdin)))