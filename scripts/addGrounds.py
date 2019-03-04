#!/usr/bin/python

import json
import sys
import sqlite3
import re

def createDB(conn):
    conn.execute("drop table if exists grounds")
    conn.execute("create table if not exists grounds(form_id varchar(150), date text, type varchar(150), grounds varchar(150), original varchar(256))") # id should be date+amount


def runGroundsCount(conn):
    createDB(conn)
    counts = {}
    for row in conn.execute("select id, type, value from form where type = 'Beige R41/42' and key = 'Grounds'"):
        groundsOriginal = re.sub(r"\(([a-gA-G]) & ([a-gA-G])\)", "(\\1) (\\2)", re.sub(r"^([a-gA-G]) & ([a-gA-G])$", "(\\1) (\\2)", row[2]))
        if groundsOriginal != row[2]:    
            print ("{} to {}".format(row[2], groundsOriginal))
        grounds = ''
        if '(a)' in groundsOriginal.lower():
            grounds += ' A'
        if '(b)' in groundsOriginal.lower():
            grounds += ' B'
        if '(c)' in groundsOriginal.lower() or 'c -' in groundsOriginal.lower():
            grounds += ' C'
        if '(d)' in groundsOriginal.lower():
            grounds += ' D'
        if '(e)' in groundsOriginal.lower():
            grounds += ' E'
        if '(f)' in groundsOriginal.lower() or 'f -' in groundsOriginal.lower():
            grounds += ' F'
        if '(g)' in groundsOriginal.lower():
            grounds += ' G'
        if len(groundsOriginal.lower().strip()) == 1:
            grounds = groundsOriginal.upper()
        if groundsOriginal.lower() == 'a, d & e':
            grounds = 'A D E'
        if groundsOriginal.lower() == 'A + E':
            grounds = 'A E'
        if groundsOriginal.lower() == 'A, D, E and G':
            grounds = 'A D E'
        if groundsOriginal.lower() == 'd e':
            grounds = 'D E'
        if groundsOriginal.lower() == 'A + G +d':
            grounds = 'A D'
        if groundsOriginal.lower() == 'a d e g':
            grounds = 'A D E'
        if groundsOriginal.lower() == 'a - b - d':
            grounds = 'A B D'
        if groundsOriginal.lower() == 'a + b':
            grounds = 'A B'

        result = conn.execute("select value from form where id = ? and key = 'Date of application'", [row[0]])    
        date = ''
        for dateRow in result:
            date = dateRow[0]

        conn.execute('INSERT INTO grounds VALUES(?, ?, ?, ?, ?)',[row[0], date, row[1], grounds.strip(), row[2]])
        for ground in grounds.split(' '):
            key = ground.strip()
            if key not in counts:
                counts[key] = 1
            else:
                counts[key] += 1

    conn.commit()
    conn.close()
    return counts

if __name__ == "__main__":
    conn = sqlite3.connect('db/tribunal.db')
    counts = runGroundsCount(conn)
    print ('Habitual national interest work: {}\nWishes national interest work: {}\nUnderaking education or trainig: {}\nHardship: {}\nIll Health: {}\nConscientious objector: {}\nListed as a protected ocupation: {}\nMissing: {}'.format(counts['A'], counts['B'], counts['C'], counts['D'], counts['E'], counts['F'], counts['G'], counts['']))
