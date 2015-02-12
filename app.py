from flask import Flask, request, redirect, abort, make_response

import os, shutil, urllib
from urlparse import urlparse
import hmac, hashlib #for creating S3 signature
import time
import multiprocessing, fcntl

app = Flask(__name__)
if os.environ.get('MODE') == 'dev':
    app.debug = True

# Have bucket name be subdomain and not as a folder or else `save_file` will
# not determine the 'key'/filename properly.
BASE_S3_URL = 'http://%s.s3.amazonaws.com' % os.environ['S3_BUCKET']
CACHE_ROOT = '/usr/src/app/cache' #no trailing /

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/<path:key>')
def cache(key):
    key = urllib.quote(key)

    # reconstruct original S3 path:
    full_path = '%s?%s' % (key, request.query_string)
    full_url = '%s/%s' % (BASE_S3_URL, full_path)

    # verify expires
    expires = int(request.args.get('Expires'))
    now = int(time.time())
    if expires <= now:
        abort(401)

    # verify signature
    # NOTE: at the moment, we assume that all requests come with Signature and
    # Expires fields.
    try:
        request_signature = urllib.quote_plus(request.args.get('Signature'))
        generated_signature = get_s3_signature(key, expires)
    except TypeError:
        abort(401)
    if generated_signature != request_signature:
        abort(401)

    # check if file has been cached, if not cache it
    if is_url_cached(full_url):
        key_filename = key_to_filename(key)
        response = make_response()
        #TODO: Implement partial downloads?
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % key
        # X-Accel-Redirect unquotes whatever is passed to it, so we need to
        # double quote it.
        response.headers['X-Accel-Redirect'] = '/cache/%s' % urllib.quote(key_filename)
        return response

    # save file in non-blocking process
    # TODO: Use file locking
    p = multiprocessing.Process(target = save_file, args = (full_url, ))
    p.start()

    return redirect(full_url)
    #return '%s\n%s' % (full_path, generated_signature)


# Adapted from https://github.com/nzoschke/s3/blob/master/s3.py
# NOTE: key must be urllib.quote
def get_s3_signature(key, expires):
    http_verb = 'GET'
    expires = str(expires)
    bucket = os.environ['S3_BUCKET']
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

def key_to_filename(key):
    key = urllib.unquote(key)
    key = urllib.quote_plus(key) #convert slashes
    return key

def save_file(url):
    key = urlparse(url).path.lstrip('/')
    key = key_to_filename(key)
    target = os.path.join(CACHE_ROOT, key)
    # NOTE: To get a lock we need to open the file, but before saving
    # the URL retrieved file, we need to unlock.
    f = open(target, 'w') 

    # Lock file to prevent multiple downloads of same file. If lock exists,
    # skip getting file.
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return #lock exists

    try:
        temp = urllib.urlretrieve(url)[0]
    except urllib.ContentTooShortError:
        return #failed to get URL
    finally:
        # unlock file
        fcntl.lockf(f, fcntl.LOCK_UN)
        f.close()
    # We use move over os.rename since rename does not handle moving files
    # across different partitions (important sine we mount target as local
    # volume in docker while temp is inside the VM).
    shutil.move(temp, target)
    os.chmod(target, 0666)

def is_url_cached(url):
    key = urlparse(url).path.lstrip('/')
    key = key_to_filename(key)
    try:
        # also checks if file exists
        if os.path.getsize(os.path.join(CACHE_ROOT, key)) > 0:
            return True
    except OSError:
        pass #file does not exist
    return False
