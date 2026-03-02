import re

BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

store = {}
counter = 0

REGEX = re.compile(
    r'^(https?:\/\/)'                 # http:// or https://
    r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'  # domain.tld (tld length 2+)
    r'(:\d+)?'                        # optional port
    r'(\/[^\s]*)?$'                   # optional path, no spaces
)

def is_valid_url(url):
    return re.match(REGEX, url) is not None

def encode_url(num):
    if num == 0:
        return BASE62[0]
    result = ""
    while num > 0:
        result = BASE62[num % 62] + result
        num //= 62
    return result

def create_short_id():
    global counter
    short_id = encode_url(counter)
    counter += 1
    return short_id