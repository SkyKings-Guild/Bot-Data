import json
import os

for _dir in [f.path.replace('\\', '/') for f in os.scandir("extensions") if f.is_dir()]:  # type: ignore
    for file in os.listdir(_dir):
        with open(_dir + '/' + file, 'r', encoding='utf-8') as f:
            json.load(f)