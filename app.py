from flask import Flask, request

import os, urllib

app = Flask(__name__)

if os.environ.get('MODE') == 'dev':
    app.debug = True

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/<path:key>')
def cache(key):
    # reconstruct original S3 path:
    query_str = urllib.urlencode(request.args.lists(), doseq=True)
    full_path = '%s?%s' % (key, query_str)

    return '%s' % full_path
