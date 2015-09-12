#downloadPublications.py
'''an application to download publication using issuuPagePub class
@version0.2.150912
@author:maajor{<mailto:hello_myd@126.com>} 
'''

import issuuPagePub

aPage = issuuPagePub.issuuPagePub('http://issuu.com/elena_ardighieri/docs/portfolio_2014_3rd_print_opt')
#change to the publication url you want
print aPage
aPage.savePageImages('D:/test//')
#change to your own directory
