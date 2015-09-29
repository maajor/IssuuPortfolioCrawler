#LoadAndContinueCrawl.py
'''load saved queue and restart crawl
@version0.3.150928
@author:maajor{<mailto:hello_myd@126.com>} 
'''

import Queue, issuuPagePub, csv
import queueMethod as qm

dictPub = {}
dictPubSaved = {}
dictQueue = {}
myqueue = Queue.Queue()
qm.loadQueue(myqueue)
qm.loadDict(dictPubSaved, 'dictPub.csv')
qm.loadDict(dictQueue, 'dictQueue.csv')

count = 0

while count < 2000 and myqueue.qsize() > 0:
    if myqueue.qsize() == 0:
        break
    thisurl = myqueue.get()
    thisPage = issuuPagePub.issuuPagePub(thisurl)
    if dictPubSaved.has_key(thisurl) or dictPub.has_key(thisurl):
        continue
    dictPub[thisurl] = thisPage.getInformation()
    count += 1
    print str(count) + " : " + str(thisPage) 
    print "Queue current size "+ str(myqueue.qsize())
    thisPage.setKeywordDict(['portfolio', 'work', 'project', 'sample', 'architect', 'architecture'])
    thisPage.initRelatedInformation()
    relatedUrl = thisPage.getRelatedUrl()
    for index in xrange(len(relatedUrl)):
        if myqueue.qsize() < 30000 and dictQueue.has_key(relatedUrl[index]) == 0:
            myqueue.put(relatedUrl[index])
            dictQueue[relatedUrl[index]] = 0
           
with open('C:\Users\walter\Desktop\stat.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect = 'excel')
    for url, info in dictPub.items():
        title, like, descrip, city, country, date, count, width, height = info
        spamwriter.writerow([url, title, like, descrip, city, country, date, count, width, height])
        dictPubSaved[url] = 0
        

qm.saveDict(dictPubSaved, 'dictPub.csv')
qm.saveDict(dictQueue, 'dictQueue.csv')