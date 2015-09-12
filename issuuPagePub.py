#issuuPagePub.py
'''main crawler class
@version0.2.150912
@author:maajor{<mailto:hello_myd@126.com>} 
'''

import urllib, re, errno, os

class issuuPagePub:
    def __init__(self, Url):
        self._url = Url
        self._content = self.__parsePage()
        self._title = self.__setPageTitle()
        self._description = self.__setPageDescription()
        self._likes = self.__setPageLikes()
        self._city = self.__setPageCity()
        self._country = self.__setPageCountry()
        self._documentId = ''
        self._pageCount = -1
        self._publicationId = ''
        self._revisionId = ''
        self._ownerUsername = ''
        self._keywordDict = []
        self._relatedContent = ''
        self._relatedOwnerUsernames = []
        self._relatedPublicationNames = []
        self._relatedDescriptions = []
        self._relatedUrls = []
    def __initBasicInformation(self):
        self._documentId = self.__setPageDocumentId()
        self._pageCount = self.__setPageCount()
    def __initAdvInformation(self):
        self._publicationId = self.__setPagePublicationId()
        self._revisionId = self.__setPageRevisionId()
        self._ownerUsername = self.__setPageOwnerUsername()
    def initRelatedInformation(self):
        self.__initAdvInformation()
        self._relatedContent = self.__parseRelatedPubs()
        self._relatedOwnerUsernames = self.__setRelatedOwnerUsernames()
        self._relatedPublicationNames = self.__setRelatedPublicationNames()
        self._relatedDescriptions = self.__setRelatedDescriptions()
        self._relatedUrls = self.__setRelatedUrl()
    def __parsePage(self):
        try:
            content = urllib.urlopen(self._url).read()
            return content
        except:
            raise
            return 
    
    def __setPageLikes(self):
        try:
            likes = re.findall(r'\"likes":[0-9]*',self._content)
            likes = re.split('[:]', likes[0])[1]
            return int(likes)
        except:
            return -1
    def __setPageTitle(self):
        try:
            title = re.findall(r'<title>.*</title>',self._content)
            title = re.split('[><]',title[0])[2] 
            title = re.sub('[/\\\:\*\!\"|<>]', ' ', title)
            return title
        except:
            return ''
    def __setPageCity(self):
        try:
            city = re.findall(r'\"city":\"[^"]*\"',self._content)
            city = re.split('["]', city[0])[3]
            return city
        except:
            return ''
    def __setPageCountry(self):
        try:
            country = re.findall(r'\"country":\"[^"]*\"',self._content)
            country = re.split('["]', country[0])[3]
            return country
        except:
            return ''      
    def __setPageDocumentId(self):
        try:
            documentid = re.findall(r'documentId=.*\"', self._content)
            documentid = re.split('[="]', documentid[0])[1]
            return documentid
        except:
            return ''
    def __setPageCount(self):
        try:
            pageCount = re.findall(r'\"pageCount\":[0-9]*', self._content)
            pageCount = re.split('[:]', pageCount[0])[1]
            return pageCount
        except:
            return 0
    def savePageImages(self, dir = 'D:/test//'):
        self.__initBasicInformation()
        directoryname = dir + self._title + ' download'
        try:
            os.mkdir(directoryname)
        except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(directoryname):
                pass
            else: raise
        for id in xrange(1, int(self._pageCount)+1):
            imgurl = "http://image.issuu.com/" + self._documentId + "/jpg/page_" + str(id) + ".jpg"
            name = directoryname + "//" + str(id) + ".jpg"
            print imgurl
            img = urllib.urlopen(imgurl) 
            f = open(name,'wb')  
            f.write(img.read())  
            f.close() 
    def __setPagePublicationId(self):
        try:
            publicationId = re.findall(r'\"publicationId\":\"\w*\"',self._content)
            publicationId = re.split('["]', publicationId[0])[3]
            return publicationId
        except:
            return ''
    def __setPageRevisionId(self):
        try:
            revisionId = re.findall(r'\"revisionId\":\"\w*\"',self._content)
            revisionId = re.split('["]', revisionId[0])[3]
            return revisionId
        except:
            return ''
    def __setPageOwnerUsername(self):
        try:
            ownerUsername = re.findall(r'\"username":\"[^"]*\"',self._content)
            ownerUsername = re.split('["]', ownerUsername[1])[3]
            return ownerUsername
        except:
            return ''
    def __setPageDescription(self):
        description = re.findall(r'\"description":\"[^"]*\"',self._content)
        if description != []:
            description = re.split('["]', description[0])[3]
            return description
        else:
            return 'None'
    def getInformation(self):
        return [self._title, str(self._likes), self._description, self._city, self._country]
    def __str__(self):
        return self._title + " HAS LIKES : " + str(self._likes) + " published at " + self._city + ", " + self._country
    def __parseRelatedPubs(self):
        relatedRequestUrl = 'http://issuu.com/call/stream/api/related/3/2/initial?publicationId=' + self._publicationId + '&revisionId=' + self._revisionId + '&ownerUsername=' + self._ownerUsername + '&seed=1000&pageSize=50&format=json'
        try:
            relatedRequestContent = urllib.urlopen(relatedRequestUrl).read()
        except IOError:
            return []  
        return relatedRequestContent            
    def __setRelatedOwnerUsernames(self):
        relatedOwnerUsername =  re.findall(r'\"ownerUsername": \"[a-zA-Z0-9\.\-\_]*\"',self._relatedContent)
        for index in xrange(len(relatedOwnerUsername)):
            thisName = re.split('["]', relatedOwnerUsername[index])[3]
            relatedOwnerUsername[index] = thisName 
        return relatedOwnerUsername
    def __setRelatedPublicationNames(self):
        relatedPublicationName =  re.findall(r'\"publicationName": \"[a-zA-Z0-9\.\-\_]*\"',self._relatedContent)
        for index in xrange(len(relatedPublicationName)):
            thisName = re.split('["]', relatedPublicationName[index])[3]
            relatedPublicationName[index] = thisName 
        return relatedPublicationName
    def __setRelatedDescriptions(self):
        relatedDescriptions = re.findall(r'\"description": \"[^"]*\"',self._relatedContent)
        return relatedDescriptions
    def __setRelatedUrl(self):
        if self._relatedContent == []:
            return []
        relatedUrl = [] 
        for index in xrange(len(self._relatedOwnerUsernames)):
            for keyword in self._keywordDict:
                if keyword in self._relatedDescriptions[index] or keyword in self._relatedPublicationNames[index]:
                    thisUrl = 'http://issuu.com/' + self._relatedOwnerUsernames[index] + '/docs/' + self._relatedPublicationNames[index]
                    relatedUrl.append( thisUrl)
                    break
        return relatedUrl
    def getRelatedUrl(self):
        return self._relatedUrls
    def setKeywordDict(self, dic):
        self._keywordDict = dic
        return