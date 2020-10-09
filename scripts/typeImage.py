#!/usr/bin/python3

import json
import sys
import requests
from pathlib import Path

def string2json(line):
    data = {}
    for field in line.split('<p>'):
       # print (field)
        name, value = field.split(':')[0], ':'.join(field.split(':')[1:])
       # print("Name: {}, value: {}".format(name,value))
        data[name] = value.strip()

    return data    

with open(sys.argv[1]) as f:
    annolist = json.load(f)
    print ('Looking at {}'.format(sys.argv[1]))
    outputDir = Path(sys.argv[2])

    for anno in annolist["resources"]:
        pageData = string2json(anno["resource"]["chars"])
        imageId = anno["on"].split('/')[7].split('.')[0]
        subDir = pageData['Tag'].replace(" ","_").replace(":","").replace("/","-").replace(",","")
        imageUrl = 'http://dams.llgc.org.uk/iiif/2.0/image/{}/full/256,/0/default.jpg'.format(imageId)

        response = requests.get(imageUrl)

        imageDir = outputDir.joinpath(subDir)
        imageDir.mkdir(parents=True, exist_ok=True)

        print ('Downloading {} to {}'.format(imageUrl, imageDir.joinpath("{}.jpg".format(imageId))))
        with open(imageDir.joinpath("{}.jpg".format(imageId)), "wb") as imgfile:
            imgfile.write(response.content)
            imgfile.close()



