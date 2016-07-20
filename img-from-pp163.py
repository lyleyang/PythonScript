import os
import time

__author__ = 'lyle'


import requests
import re
from selenium import webdriver

index = 0

def downAllImage(url):
    r = requests.get(url)
    p = re.compile(r'data-lazyload-src="(.+?\.jpg)"')

    base_path = os.path.join(os.path.expanduser('~'), "Documents/pp")
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    m = p.findall(r.text)
    global index
    for url in m:
        print(url)
        r = requests.get(url, stream=True)
        filename = os.path.join(base_path, str(index)+".jpg")
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)
        index += 1

def downAllHref(web):
    try:
        es = web.find_elements_by_css_selector("a.img.js-anchor.etag.noul")
        for e in es:
            url = e.get_attribute("href")
            downAllImage(url)

    except():
        print("error ")

def closeAD(web):
    ad = web.find_element_by_css_selector("a.ztag.btn-close")
    ad.click()

def nextPage(web):
    next = web.find_element_by_css_selector("span.pgi.pgb.pgbright.iblock")
    next.click()

def start():
    web = webdriver.Chrome(os.path.join(os.path.expanduser('~'), "Documents/chromedriver"))
    web.get("http://pp.163.com/pp/#p=10&c=-1&m=3&page=1")
    time.sleep(3)
    closeAD(web)
    time.sleep(3)
    while True:
        downAllHref(web)
        nextPage(web)
        time.sleep(3)
    web.quit()


if __name__ == "__main__":
    start()
