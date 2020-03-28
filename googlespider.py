import urllib.error, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import sqlite3
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

datahandle=sqlite3.connect('spiderdb.sqlite')
cur=datahandle.cursor()

cur.execute('DROP TABLE IF EXISTS Pages')
cur.execute('DROP TABLE IF EXISTS Links')
cur.execute('CREATE TABLE Pages ( id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT, old_rank FLOAT, new_rank FLOAT )')
cur.execute('CREATE TABLE Links ( from_id INTEGER, to_id INTEGER, UNIQUE (from_id,to_id))')

start_url=input("Enter a website: ")
cur.execute('INSERT INTO Pages (url, html, new_rank) VALUES (?, NULL, 1.0)',(start_url,))
datahandle.commit()

number=input('How many pages to spider: ')
count=int(number)

for i in range(count):
    cur.execute('SELECT id,url FROM Pages WHERE html is NULL ORDER BY RANDOM() LIMIT 1')
    row=cur.fetchone()
    if row is None:
        print(i+1,"End of connected links, Restart the process with new start point")
        break

    url = row[1]
    from_id = row[0]

    try:
        retdata=urllib.request.urlopen(url, context=ctx)
    except:
        print(i+1,url,'URL Page not available')
        cur.execute('DELETE FROM Pages WHERE url=?',(url,))
        datahandle.commit()
        continue

    #ignore non text/html files
    if 'text/html' != retdata.info().get_content_type():
        print(i+1,url,"Ignoring non text/html files")
        cur.execute('DELETE FROM Pages WHERE url=?',(url,))
        datahandle.commit()
        continue

    try:
        html=retdata.read()
    except:
        print(i+1,url,"Error in reading data using .read function")
        cur.execute('DELETE FROM Pages WHERE url=?',(url,))
        datahandle.commit()
        continue

    try:
        soup=BeautifulSoup(html,'html.parser')
        tags=soup('a')
    except:
        print(i+1,url,"Error in parsing the file with BeautifulSoup")
        cur.execute('DELETE FROM Pages WHERE url=?',(url,))
        datahandle.commit()
        continue

    cur.execute('UPDATE Pages SET html=? WHERE url=?',(memoryview(html),url))
    inlinks=0

    for tag in tags:
        try:
            href = tag.get('href', None)
            if ( href is None ) :
                continue
            # Resolve relative references like href="/contact"
            up = urllib.parse.urlparse(href)
            if ( len(up.scheme) < 1 ) :
                href = urllib.parse.urljoin(url, href)
            ipos = href.find('#')
            if ( ipos > 1 ) : href = href[:ipos]
            if ( href.endswith('/') ) : href = href[:-1]
            # print href
            if ( len(href) < 1 ) : continue
            if href.endswith('doc') or href.endswith('docx'):
                continue
            if not href.startswith(start_url):
                continue
        except:
            print('Error in forming url')
            continue
        cur.execute('INSERT OR IGNORE INTO Pages(url,html,new_rank) VALUES ( ?, NULL, 1.0)',(href,))
        inlinks=inlinks+1
        datahandle.commit()
        cur.execute('SELECT id FROM Pages WHERE url=? ',(href,))
        to_id=cur.fetchone()[0]

        cur.execute('INSERT OR REPLACE INTO Links(from_id, to_id) VALUES (?,?)',(from_id, to_id))

    print(i,url,inlinks)
datahandle.commit()
cur.close()
