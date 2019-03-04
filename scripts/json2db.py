#!/usr/bin/python

import json
import sys
import sqlite3
import addGrounds

def string2json(line):
    data = {}
    for field in line.split('<p>'):
       # print (field)
        name, value = field.split(':')[0], ':'.join(field.split(':')[1:])
       # print("Name: {}, value: {}".format(name,value))
        data[name] = value.strip()

    return data    

def createDB(conn):
    conn.execute("drop table if exists form")
    conn.execute("create table if not exists form(id varchar(150), type varchar(150), key varchar(150), value varchar(256))") # id should be date+amount

    conn.execute("drop table if exists form_canvas")
    conn.execute("create table if not exists form_canvas (form_id varchar(150),type varchar(150), canvas_id varchar(150), manifest_id varchar(150))") # id should be date+amount
    
def createId(anno1, anno2=None):
    if anno2 is None:
        return "{}".format(shortId(anno1["on"])) 
    else:
        return "{}-{}".format(shortId(anno1["on"]),shortId(anno2["on"])) 

def shortId(canvas_uri):
    splitURI = canvas_uri.split('#')[0].split('/')
    return "{}-{}".format(splitURI[5],splitURI[7].split('.json')[0])

def anno2ImageLink(anno):
    canvasId = anno["on"].split('#')[0].split('/')
    return "{}/image/{}/full/1200,/0/default.jpg".format("/".join(canvasId[0:5]), canvasId[7].split('.json')[0]) 

def anno2manifest(anno):
    canvasId = anno["on"].split('#')[0].split('/')
    return "https://damsssl.llgc.org.uk/iiif/2.0/{}/manifest.json".format(canvasId[5]) 

def runFixes(anno, pageData):
    runFixOnLis(anno,pageData, ['4003411'], 'Blue R52/53, page 1') 
    runFixOnLis(anno,pageData, ['4003442'], 'Blue R52/53, page 2') 
    runFixOnLis(anno,pageData, ['4003762', '4004474','4004492'], 'Beige R41/42: Page 1') 
    runFixOnLis(anno,pageData, ['4004475'], 'Beige R41/42: Page 2') 
    runFixOnLis(anno,pageData, [] , 'Unknown document type') 

def runFixOnLis(anno,pageData, ids, doc_type):
    for ident in ids:
        if ident in anno['on']:
            pageData['Tag'] = doc_type


def addMissingPage(anno):
    if '4004069' in anno['on']:
        # 4004068 is missing transcription so add it here...
        page1Anno = {}
        page1Anno['on'] = 'https://damsssl.llgc.org.uk/iiif/2.0/4003356/canvas/4004068.json#xywh=0,0,3484,5528'
        page1Anno['resource'] = {
            "@type": "cnt:ContentAsText",
            'chars': 'Name of Local Tribunal: Cardiganshire Appeal<p>Name: Richard John Williams<p>Age: 20<p><p>Married or single: Single<p>Address: 12, Prospect Street, Aberystwyth<p>Occupation, profession or business: Chemists Apprentice<p>Grounds: See below<p>Nature of application: Application is made for the variation or withdrawal of the Certificate in this case on the ground that it is no longer in the national interest that he shall be allowed to remain in civil occupation<p>Tag: Beige R41/42: Page 1',
            'format': 'text/plain'
        }
        return page1Anno
    if '4004071' in anno['on']:
        # 4004070 is missing transcription so add it here...
        page1Anno = {}
        page1Anno['on'] = 'https://damsssl.llgc.org.uk/iiif/2.0/4003356/canvas/4004070.json#xywh=0,0,3612,5400'
        page1Anno['resource'] = {
            "@type": "cnt:ContentAsText",
            'chars': 'Name of Local Tribunal: Cardiganshire Appeal<p>Number of Case: 157<p>Name: William Griffith Edwards<p>Age: 19<p>Married or single: Single<p>Address: 15, Rummers St, Aberystwyth<p>Number of group: 2<p>Number on group card: 15<p>Occupation, profession or business: Boot and shoe salesman<p>Grounds: See below<p>Nature of application: Application is made for the variation or withdrawal of the Certificate in this case on the ground that it is no longer in the national interest that he shall be allowed to remain in civil occupation<p>Tag: Blue R52/53, page 1',
            'format': 'text/plain'
        }
        return page1Anno
    return None     

with open(sys.argv[1]) as f:
    annolist = json.load(f)

    conn = sqlite3.connect('db/tribunal.db')
    createDB(conn)
    
    page1 = None 
    page2 = None
    entries = []
    for anno in annolist["resources"]:
        pageData = string2json(anno["resource"]["chars"])
        # fixes
        runFixes(anno, pageData)
        tag = pageData['Tag']
        if 'age 1' in tag:
            page1 = anno
        elif 'age 2' in tag:
            if page1 is None:
                page1 = addMissingPage(anno)
                if page1 is None:
                    print ('Failed to find first page for anno.')
                    print (json.dumps(anno, indent=4))
                    print ('Image URL {}'.format(anno2ImageLink(anno)))
            page1Data = string2json(page1["resource"]["chars"])

            if 'Grounds' not in page1Data:
                page1Data['Grounds'] = ''
            runFixes(page1, page1Data)

            page2 = anno 
            page2Data =  pageData
            identifier = createId(page1, page2)
           
            if ',' in  tag:
                shortTag = tag.split(',')[0]
            elif ':' in tag:
                shortTag = tag.split(':')[0]
            
            manifest = anno2manifest(anno)
            conn.execute('INSERT INTO form_canvas VALUES (?, ?, ?, ?)', [identifier, page1Data['Tag'], page1["on"].split('#')[0], manifest])
            conn.execute('INSERT INTO form_canvas VALUES (?, ?, ?, ?)', [identifier, page2Data['Tag'], page2["on"].split('#')[0], manifest])
     
            entry = page1Data
            entry.update(page2Data)
            for key in entry:
                # need to move Tag to a field in db
                conn.execute('INSERT INTO form VALUES (?, ?, ?, ?)', [identifier, shortTag, key, entry[key]])
                
            #print (json.dumps(entry,indent=4))
            #entries.append(entry);
            page1 = None 
            page2 = None
        elif 'Unknown document type' == tag:
            if page1 is not None:
                print('Got lost somewhere with {}. page1 contains data where it should be empty'.format(anno['@id']))
            identifier = createId(anno)     
            for key in pageData:
                # need to move Tag to a field in db
                conn.execute('INSERT INTO form VALUES (?, ?, ?, ?)', [identifier, tag, key, pageData[key]])
            manifest = anno2manifest(anno)
            conn.execute('INSERT INTO form_canvas VALUES (?, ?, ?, ?)', [identifier, tag, anno["on"].split('#')[0], manifest])
        else:
            # page not tagged with a type
            print ('Page not tagged with a type {}\n'.format(anno['resource']['chars'].encode('utf-8')))
            print ('Image URL {}'.format(anno2ImageLink(anno)))
            #print (pageData)

    conn.commit()
    addGrounds.runGroundsCount(conn)
    conn.close()

#print (entries)
