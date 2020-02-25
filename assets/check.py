import json
import sys
import gdelt

def msg(msg, *args, **kwargs):
    print(msg.format(*args, **kwargs), file=sys.stderr)

def _check(instream, destpath = None):
    payload = json.load(instream)
    msg('Payload {}', payload)
    source = payload['source']
    gd = gdelt.gdelt(version = source['version'])
    gd.schema('events')
    return gd.Search(source['date_start'], source['date_end'], output='json' ,table='events', coverage=True, translation=False)[0]

if __name__ == "__main__":
    try:
        destpath = sys.argv[1] or None
        print(_check(sys.stdin, destpath))
    except:
        with open('secret.json', 'rb') as f:
            print(_check(f))