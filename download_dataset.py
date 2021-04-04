from zipfile import ZipFile
from math import ceil
import requests
import time
import sys
import os

MB = 1024 * 1024
downloads_path = ''
url_list = sys.argv[1:]
downloads = []

def print_progress(percentage):
    print('\r%{:.2f} '.format(percentage) + '[' + '=' * int(percentage * 3 / 10) + ' ' * (30 - int(percentage * 3 / 10)) + ']', end=' ')

for url in url_list:
    print('---------------------------------')
    filename = url.split('/')[-1].split('.')[0] # assumes downloading w/ .zip extension
    path = os.path.join(downloads_path, filename)
    downloads.append(filename)
    start = time.time()

    r = requests.get(url, stream=True)
    size = int(r.headers.get('content-length')) / MB

    if os.path.exists(path):
        print('Dataset {} already exists @ {}'.format(filename, path))
        continue

    print('Downloading {}'.format(filename + '.zip'))
    print('File Size: (approx) {} MB'.format(ceil(size)))
    chunk_size = 4096
    with open(path + '.zip', 'wb') as fd:
        downloaded = 0
        print_progress(downloaded * 100 / size)
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
            downloaded += chunk_size / MB
            downloaded = min(downloaded, size)
            print_progress(downloaded * 100 / size)
        fd.close()

    print('\nUnzipping...')
    
    with ZipFile(path + '.zip', 'r') as myzip:
        myzip.extractall(downloads_path)
        myzip.close()
    
    print('Deleting archive...')

    os.remove(path + '.zip')
    
    total_time = time.time() - start
    print('Done!\nTime elapsed: {} minutes\nAvg download speed: {} mbps'.format(total_time // 60, size // total_time))
