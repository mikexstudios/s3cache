from flask import Flask, request
import boto

import os, urllib
import hmac, hashlib #for creating S3 signature

app = Flask(__name__)

if os.environ.get('MODE') == 'dev':
    app.debug = True

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/<path:key>')
def cache(key):
    # reconstruct original S3 path:
    full_path = '%s?%s' % (urllib.quote(key), request.query_string)
    generated_signature = get_s3_signature(key, request.args.get('Expires'))
    request_signature = urllib.quote_plus(request.args.get('Signature'))
    assert generated_signature == request_signature

    return '%s\n%s' % (full_path, generated_signature)


# Adapted from https://github.com/nzoschke/s3/blob/master/s3.py
def get_s3_signature(key, expires):
    http_verb = 'GET'
    bucket = os.environ['S3_BUCKET']
    key = urllib.quote(key) #don't quote slashes
    canonical_string = '/%s/%s' % (bucket, key)
    canonical_string = canonical_string.rstrip('/') #when key = ''
    secret_access_key = os.environ['S3_SECRET_ACCESS_KEY']

    if bucket == '' or secret_access_key == '':
        raise Exception('No S3_BUCKET or S3_SECRET_ACCESS_KEY defined!')

    string_to_sign = '%s\n\n\n%s\n%s' % (http_verb, str(expires), canonical_string)
    string_to_sign = unicode(string_to_sign, 'utf-8')
    signature = hmac.new(secret_access_key, string_to_sign, hashlib.sha1)
    signature = urllib.quote_plus(signature.digest().encode('base64').rstrip('\n'))
    return signature
