from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import requests
import os
import shutil


def isDirectory(url):
    if(url.endswith('/')):
        return True
    else:
        return False

#def download_file(url: str, dest_folder: str):
#    if not os.path.exists(dest_folder):
#        os.makedirs(dest_folder)  # create folder if it does not exist
#
#    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
#    file_path = os.path.join(dest_folder, filename)
#
#    r = requests.get(url, stream=True)
#    if r.ok:
#        print("saving to", os.path.abspath(file_path))
#        with open(file_path, 'wb') as f:
#            for chunk in r.iter_content(chunk_size=1024 * 8):
#                if chunk:
#                    f.write(chunk)
#                    f.flush()
#                    os.fsync(f.fileno())
#    else:  # HTTP status code 4XX/5XX
#        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

def download_file(url, folder_name):
    local_filename = url.split('/')[-1]
    path = os.path.join("{}{}".format(folder_name, local_filename))
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename

def findLinks(url, ospath):
    # print(ospath)
    if not os.path.exists(ospath):
        os.makedirs(ospath)
    page = requests.get(url).content
    bsObj = BeautifulSoup(page, 'html.parser')
    maybe_directories = bsObj.findAll('a', href=True)
    for link in maybe_directories:
        # print(link['href'])
        # print(isDirectory(link['href']))
        if(link['href'] != "../"):
            if(isDirectory(link['href'])):
                newUrl = url + link['href']
                newosPath = ospath + link['href']
                findLinks(newUrl, newosPath) #recursion happening here
            else:
                if(link['href'].endswith('.mp4') or link['href'].endswith('.mkv')):
                    newUrl = url + link['href']
                    # print(newUrl)
                    # print(link['href'])
                    # print(ospath)
                    # print(url) #now safe and download
                    download_file(newUrl, ospath)


startUrl = "https://dl3.3rver.org/cdn2/03/series/1994/Friends/"
startPath = "D:/Friends/1994/"
findLinks(startUrl, startPath)
