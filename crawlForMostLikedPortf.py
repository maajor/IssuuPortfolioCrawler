#crawlForMostLikedPortf.py
'''an application to crawl for most liked publication and save them, using issuuPagePub class
@version0.4.151001
@author:maajor{<mailto:hello_myd@126.com>} 
'''

import Queue, issuuPagePub, csv
import queueMethod as qm

dictPub = {}
dictQueue = {}
myqueue = Queue.Queue()
myqueue.put("http://issuu.com/jamesleng/docs/jamesleng_portfolio2013")
myqueue.put("http://issuu.com/studiowangfei/docs/fei-jpg")
myqueue.put("http://issuu.com/wangzigeng/docs/narrator_wang_zigeng_1500dpi")
myqueue.put("http://issuu.com/sogkarimi/docs/karimiarchportfolio")
myqueue.put("http://issuu.com/b.a.maranda/docs/portfolio_2015")
myqueue.put("http://issuu.com/justinoh/docs/20150102_portfolio__compiled_")
myqueue.put("http://issuu.com/maithamalmubarak/docs/portfolio2014")
myqueue.put("http://issuu.com/yutianwang/docs/portfolio_of_yutian_wang_harvard_ma")
myqueue.put("http://issuu.com/lixiangyu/docs/portfolio_b5-")
myqueue.put("http://issuu.com/archdekk/docs/portfolio2013")

count = 0

while count < 2000:
    if myqueue.qsize() == 0:
        break
    thisurl = myqueue.get()
    thisPage = issuuPagePub.issuuPagePub(thisurl)
    if dictPub.has_key(thisurl):
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
        
qm.saveQueue(myqueue)
qm.saveDict(dictPub, 'dictPub.csv')
qm.saveDict(dictQueue, 'dictQueue.csv')