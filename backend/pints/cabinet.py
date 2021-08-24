import os
from cloudstorage.drivers.amazon import S3Driver

AWS_ACCESS_KEY_ID = os.environ.get('PAPER_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('PAPER_AWS_SECRET_ACCESS_KEY')
PAPER_STORAGE_CONTAINER = os.environ.get('PAPER_STORAGE_CONTAINER', 'paper-metrics')

if AWS_ACCESS_KEY_ID:
    storage = S3Driver(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)

def file(filename):
    container = storage.get_container('paper-metrics')
    blob = container.upload_blob(filename, acl='public-read')
    url = blob.generate_download_url()
    if '?' in url:
        url = url.split('?')[0]
    return url
