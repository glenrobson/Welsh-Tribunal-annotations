#!/usr/bin/python
import sys
import datetime
import sqlite3
import os
from bottle import route, run, template,debug, get, static_file

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
        

@route('/index.html')
@route('/')
def showIndex():
    data = getGroundsPerYear()

    output = template('templates/grounds.tpl', data=data)
    return output

if __name__ == "__main__":
    debug(True)
    run(host='localhost', port=9000)
