#queueMethod.py
'''some queue I/O method for crawler
@version0.2.150912
@author:maajor{<mailto:hello_myd@126.com>} 
'''

import Queue, csv

def saveQueue(queue, directo = 'C:\Users\walter\Desktop\statQueue.csv'):
    with open(directo, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect = 'excel')
        while queue.qsize() > 0:
            url = queue.get()
            spamwriter.writerow([url])
    return
def loadQueue(queue, directo = 'C:\Users\walter\Desktop\statQueue.csv'):
    csvfile = file(directo, 'rb')
    spamreader = csv.reader(csvfile, dialect = 'excel')
    for line in spamreader:
        queue.put(line)
    csvfile.close()
    return