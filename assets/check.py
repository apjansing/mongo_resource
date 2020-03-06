import json
import sys
import pymongo as pm
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus

def msg(msg, *args, **kwargs):
    print(msg.format(*args, **kwargs), file=sys.stderr)

def _check(instream, destpath = None, username="admin", 
                    password="admin"):
    payload = json.load(instream)
    msg('Payload {}', payload)
    source = payload["source"]
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
    # print(connection.test.trigger.find().next())
    db = connection[source['db']]

    collection = db[source['collection']]
    find = source['find']
    cursor = collection.find(dict(find))
    for _ in range(cursor.count()):
        print(cursor.next())
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # print(_check(sys.stdin, sys.argv[1]))
        _check(sys.stdin, sys.argv[1])
    else:
        with open('secret.json', 'rb') as f:
            # print(_check(f))
            _check(f)