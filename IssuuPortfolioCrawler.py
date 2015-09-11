# -*- coding: utf-8 -*-
import urllib,re,os,csv
import Queue, errno

def parsePage(url):
    content = urllib.urlopen(url).read()
    return content

def getPageTitle(content):
    title = re.findall(r'<title>.*</title>',content)
    title = re.split('[><]',title[0])[2] 
    title = re.sub('[/\\\:\*\!\"|<>]', ' ', title)
    return title

def getPageDocumentId(content):
    documentid = re.findall(r'documentId=.*\"', content)
    documentid = re.split('[="]', documentid[0])[1]
    return documentid

def getPageCount(content):
    pageCount = re.findall(r'\"pageCount\":[0-9]*', content)
    pageCount = re.split('[:]', pageCount[0])[1]
    return pageCount

def savePageImages(title, documentid, pageCount, dir = 'C:\Users\Yidong\Desktop\\test\\'):
    directoryname = dir + title + ' portfolio'
    try:
        os.mkdir(directoryname)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(directoryname):
            pass
        else: raise
    for id in xrange(1, int(pageCount)+1):
        imgurl = "http://image.issuu.com/" + documentid + "/jpg/page_" + str(id) + ".jpg"
        name = directoryname + "\\" + str(id) + ".jpg"
        print imgurl
        img = urllib.urlopen(imgurl) 
        f = open(name,'wb')  
        f.write(img.read())  
        f.close() 



def downloadIssuuPub(url, dir = 'C:\Users\Yidong\Desktop\\test\\'):
    #url = "http://issuu.com/hanastaroova/docs/140119_portfolio_eng"  
    content = parsePage(url)     
    title = getPageTitle(content)
    documentid = getPageDocumentId(content)
    pageCount = getPageCount(content)
    savePageImages(title,documentid, pageCount)
    return

def parseRelatedPubs(publicationId, revisionId, ownerUsername):
    relatedRequestUrl = 'http://issuu.com/call/stream/api/related/3/2/initial?publicationId=' + publicationId + '&revisionId=' + revisionId + '&ownerUsername=' + ownerUsername + '&seed=1000&pageSize=50&format=json'
    try:
        relatedRequestContent = urllib.urlopen(relatedRequestUrl).read()
    except IOError:
        return []  
    return relatedRequestContent

def getPagePublicationId(content):
    publicationId = re.findall(r'\"publicationId\":\"\w*\"',content)
    publicationId = re.split('["]', publicationId[0])[3]
    return publicationId
    
def getPageRevisionId(content):
    revisionId = re.findall(r'\"revisionId\":\"\w*\"',content)
    revisionId = re.split('["]', revisionId[0])[3]
    return revisionId

def getPageOwnerUsername(content):
    ownerUsername = re.findall(r'\"username":\"[^"]*\"',content)
    ownerUsername = re.split('["]', ownerUsername[1])[3]
    return ownerUsername
    
def getRelatedOwnerUsernames(relatedRequestContent):
    relatedOwnerUsername =  re.findall(r'\"ownerUsername": \"[a-zA-Z0-9\.\-\_]*\"',relatedRequestContent)
    for index in xrange(len(relatedOwnerUsername)):
        thisName = re.split('["]', relatedOwnerUsername[index])[3]
        relatedOwnerUsername[index] = thisName 
    return relatedOwnerUsername

def getRelatedPublicationNames(relatedRequestContent):
    relatedPublicationName =  re.findall(r'\"publicationName": \"[a-zA-Z0-9\.\-\_]*\"',relatedRequestContent)
    for index in xrange(len(relatedPublicationName)):
        thisName = re.split('["]', relatedPublicationName[index])[3]
        relatedPublicationName[index] = thisName 
    return relatedPublicationName
    
def getPageDescription(content):
    description = re.findall(r'\"description":\"[^"]*\"',content)
    if description != []:
        description = re.split('["]', description[0])[3]
        return description
    else:
        return 'None'

def getRelatedUrl(url = "http://issuu.com/hanastaroova/docs/140119_portfolio_eng" ):
    try:
        content = parsePage(url)
    except IOError:
        return []
    publicationId = getPagePublicationId(content)
    revisionId = getPageRevisionId(content)
    ownerUsername = getPageOwnerUsername(content)
    relatedRequestContent = parseRelatedPubs(publicationId, revisionId, ownerUsername)
    if relatedRequestContent == []:
        return []
    relatedOwnerUsername =  getRelatedOwnerUsernames(relatedRequestContent)
    relatedPublicationName =  getRelatedPublicationNames(relatedRequestContent)
    relatedDescription = re.findall(r'\"description": \"[^"]*\"',relatedRequestContent)
    relatedUrl = []
    dic = ['portfolio', 'work', 'project', 'sample', 'architect', 'architecture', 'exhibition']
    for index in xrange(len(relatedOwnerUsername)):
        for keyword in dic:
            if keyword in relatedDescription[index] or keyword in relatedPublicationName[index]:
                thisUrl = 'http://issuu.com/' + relatedOwnerUsername[index] + '/docs/' + relatedPublicationName[index]
                relatedUrl.append( thisUrl)
                break
    #print relatedUrl
    #print len(relatedUrl)      
    return relatedUrl

def getPageLikes(content):
    likes = re.findall(r'\"likes":[0-9]*',content)
    likes = re.split('[:]', likes[0])[1]
    return int(likes)

#urlSource = "http://issuu.com/jamesleng/docs/jamesleng_portfolio2013"
'''urlSource = "http://issuu.com/krisc16/docs/kristopher_chan_portfolio_012014"
#downloadIssuuPub(urlSource)
rel = getRelatedUrl(urlSource)
content = parsePage(urlSource)
like = getPageLikes(content)
print like
print rel'''

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

while count < 10000:
    if myqueue.qsize() == 0:
        break
    thisurl = myqueue.get()
    try:
        thisContent = parsePage(thisurl)
    except IOError:
        continue
    if dictPub.has_key(thisurl):
        continue
    title = getPageTitle(thisContent)
    likes = getPageLikes(thisContent)
    description = getPageDescription(thisContent)
    dictPub[thisurl] = [title, str(likes), description]
    count += 1
    print str(count) + " : " + title + " HAS LIKES : " + str(likes) 
    print "Queue current size "+ str(myqueue.qsize())
    relatedUrl = getRelatedUrl(thisurl)
    for index in xrange(len(relatedUrl)):
        if myqueue.qsize() < 30000 and dictQueue.has_key(relatedUrl[index]) == 0:
            myqueue.put(relatedUrl[index])
            dictQueue[relatedUrl[index]] = 0
           
with open('C:\Users\walter\Desktop\stat.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect = 'excel')
    for url, info in dictPub.items():
        title, like, descrip = info
        spamwriter.writerow([url, title, like, descrip])
        
with open('C:\Users\walter\Desktop\statQueue.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect = 'excel')
    while myqueue.qsize() > 0:
        url = myqueue.get()
        spamwriter.writerow([url])
