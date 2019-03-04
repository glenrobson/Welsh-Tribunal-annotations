#!/usr/bin/python
import sys
import datetime
import sqlite3
import json
import os
from bottle import route, run, template,debug, get, static_file
reasons = {}
reasons['A'] = 'Habitual work is of national interest'
reasons['B'] = 'Wishes to work in a position which is of national interest'
reasons['C'] = 'Underaking education or trainnig for national interest work'
reasons['D'] = 'Hardship'
reasons['E'] = 'Ill Health'
reasons['F'] = 'Conscientious objector'
reasons['G'] = 'Listed as a protected ocupation'
reasons[''] = 'Missing grounds'
keyOrders = {
    'grounds': ['A', 'B', 'C', 'D', 'E', 'F', 'G', ''],
    'year': ['1916', '1917', '1918', '']
}

def printIfAvliable(key, dictonary):
    if key in dictonary:
        return dictonary[key]
    return ''    

def getGroundsPerYear():
    conn = sqlite3.connect('db/tribunal.db')
    results = {}
    for row in conn.execute('select date, grounds, original from grounds'):
        if len(row[0]) > 4:
            year = row[0][0:4]
        else:
            year = ''

        if year not in results:
            results[year] = {}
            for ground in 'A B C D E F G'.split(' '):
                key = ground.strip()
                if key not in results[year]:
                    results[year][key] = 0
            results[year][''] = 0        

        if len(row[1]) == 0:
            results[year][''] += 1
        else:    
            for ground in row[1].split(' '):
                results[year][ground.strip()] += 1

    return results

def getPeopleForGrounds(grounds):
    conn = sqlite3.connect('db/tribunal.db')
    results = {}
    sqlResults = None
    if grounds == 'missing_grounds':
        sqlResults = conn.execute("select * from grounds where grounds = '';")
    else:
        sqlResults = conn.execute("select * from grounds where grounds like ?;",('%{}%'.format(grounds),))
    for row in sqlResults:
        result = {} 
        form_id = row[0]
        date = row[1]
        if len(date) > 4:
            year = date[0:4]
        else:
            year = ''
        result['id'] = form_id
        result['type'] = row[2]
        result['ground'] = row[3]
        metadata = {}
        for fields in conn.execute("select * from form where id = ?;",(form_id,)):
            metadata[fields[2]] = fields[3]

        result['metadata'] = metadata
        
        manifestData = conn.execute("select * from form_canvas where form_id = ? order by type asc limit 1;", (form_id,)).fetchone()

        result['images'] = {
            'manifest': manifestData[3],
            'canvas': manifestData[2]
        }
        if year not in results:
            results[year] = []
        results[year].append(result)


    return results        
        
@route('/index.html')
@route('/')
def showIndex():
    data = getGroundsPerYear()

    print(json.dumps(data, indent=4))
    output = template('templates/grounds.tpl', data=data, reasons=reasons, keyOrders=keyOrders)
    return output

@route('/<grounds>.html')
def showDetails(grounds):    
    data = getPeopleForGrounds(grounds)
    print(json.dumps(data, indent=4))
    output = template('templates/year_grounds.tpl', data=data, grounds=grounds, reasons=reasons, keyOrders=keyOrders)
    return output

if __name__ == "__main__":
    debug(True)
    run(host='localhost', port=9000)
