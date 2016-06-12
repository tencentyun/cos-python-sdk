#!/usr/bin/env python
# coding=utf-8

import random
import time
import urllib
import hmac
import hashlib
import binascii
import base64
import cos_cred

class Auth(object):
    def __init__(self, cred):
        self.cred = cred

    def app_sign(self, bucket, cos_path, expired):
        appid      = self.cred.get_appid()
        bucket     = bucket.encode('utf8')
        secret_id  = self.cred.get_secret_id().encode('utf8')
        now        = int(time.time())
        rdm        = random.randint(0, 999999999)
        cos_path   = urllib.quote(cos_path.encode('utf8'), '~/')
        fileid     = '/%s/%s%s' % (appid, bucket, cos_path)
        sign_tuple = (appid, secret_id, expired, now, rdm, fileid, bucket)

        plain_text  = 'a=%s&k=%s&e=%d&t=%d&r=%d&f=%s&b=%s' % sign_tuple
        secret_key  = self.cred.get_secret_key().encode('utf8')
        sha1_hmac   = hmac.new(secret_key, plain_text, hashlib.sha1)
        hmac_digest = sha1_hmac.hexdigest()
        hmac_digest = binascii.unhexlify(hmac_digest)
        sign_hex    = hmac_digest + plain_text
        sign_base64 = base64.b64encode(sign_hex)
        return sign_base64

    def sign_once(self, bucket, cos_path):
        return self.app_sign(bucket, cos_path, 0)

    def sign_more(self, bucket, cos_path, expired):
        return self.app_sign(bucket, cos_path, expired)
