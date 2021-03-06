import sys
import os
import os.path
import requests
import lxml.html
from multiprocessing import Pool
from multiprocessing import Process

def main(url):
  if not url.startswith('http'):
    print('url is invalid')
    sys.exit(1)

  img_dir = 'img/%s' % url.split('//')[-1].split('/')[0]
  content = requests.get(url).content

  xhtml = lxml.html.document_fromstring(content)
  img_urls = xhtml.xpath('//img/@src')
  img_set = set()
  for img in img_urls:
    img_set.add(img)

  if not os.path.isdir(img_dir):
    os.makedirs(img_dir)

  for img in img_set:
    if not img.startswith('http'):
      img = '%s/%s' % (url, img)
    filename = img.split('/')[-1]
    with open('%s/%s' % (img_dir, filename), 'wb') as f:
      f.write(requests.get(img).content)

def multi_download(urllist):
  urls = open(urllist, 'r').readlines()
  p = Pool(10)
  p.map(main, urls)

urllist = 'urllist.txt'
multi_download(urllist)
