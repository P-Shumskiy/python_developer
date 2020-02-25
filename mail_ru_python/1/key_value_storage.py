import argparse
import json
import os
import tempfile


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="take key of storage", type=str)
parser.add_argument("--val", help="take value of current key", type=str)
args = parser.parse_args()

mode = 'r+' if os.path.exists(storage_path) else 'w+'

with open(storage_path, mode=mode) as f:
    try:
        storage_data = json.load(f)
    except json.decoder.JSONDecodeError:
        storage_data = dict()

if args.key:
    if args.val:
        if storage_data.get(args.key):
            storage_data[args.key].append(args.val)
        else:
            storage_data[args.key] = [args.val]
    else:
        if storage_data.get(args.key):
            print(", ".join(map(str, storage_data[args.key])))
        else:
            print('None')

with open(storage_path, 'r+') as f:
    json.dump(storage_data, f)
