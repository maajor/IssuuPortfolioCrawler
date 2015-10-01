import Queue, csv
import queueMethod as qm

dictPub = {}
dictPubSaved = {}
dictQueue = {}
myqueue = Queue.Queue()
qm.loadQueue(myqueue)

qm.loadDict(dictPubSaved, 'dictPub.csv')

namedictPubSaved = 'dictPub.csv'
namedictQueue = 'dictQueue.csv'

directo = 'C:\Users\walter\Desktop\\'
csvfile = file(directo + namedictPubSaved, 'rb')
spamreader = csv.reader(csvfile, dialect = 'excel')
for line in spamreader:
    dictPubSaved[line[0]] = 0
csvfile.close()

directo = 'C:\Users\walter\Desktop\\'
csvfile = file(directo + namedictQueue, 'rb')
spamreader = csv.reader(csvfile, dialect = 'excel')
for line in spamreader:
    dictQueue[line[0]] = 0
csvfile.close()
