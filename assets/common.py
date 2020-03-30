import sys
from pprint import pprint
from urllib.parse import quote_plus

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

def get_payload_data(payload):
  source = payload["source"]
  username = get_or_default(source, "username", "admin")
  password = get_or_default(source, "password", "admin")
  host = f'{source["url"]}:{source["port"]}'
  uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
  return source, uri