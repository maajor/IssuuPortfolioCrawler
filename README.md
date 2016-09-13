# IssuuPortfolioCrawler
Find architecture portfolios on Issuu
  
Issuu爬虫  
*查找最赞的建筑作品集  
*利用Issuu页面自动加载的推荐文件爬  
*有下载功能  
  
使用库：  urllib + re    

folder 4000: results after crawling for 4000 portfolios and sorted by likes  
folder 10000: results after crawling for 10000 portfolios and sorted by likes, ran for 6 hours on my laptop  

# To Use this crawler  
### 1. Start Crawler.
1. change directory to this project
2. open `crawlForMostLikedPortf.py`
2. change your starting portfolios. I add some urls to `myqueue`, you can add your favorite portfolios into this queue.
3. change your saving directory on line 45
4. change portfolios number on line 26
5. run the script.

### 2. Restart Crawler.
If you have finished last crawl, the script should have saved two files `dictPub.csv` and `dictQueue.csv`
1. change directory to this project
2. open `LoadAndContinueCrawl.py`
3. change your saving directory on line 40
4. change portfolios number on line 20
5. run the script.

### 3. Save a Portfolio
1. change directory to this project
2. open `downloadPublications.py`
2. change your saving directory on line 12
3. change the portfolio url you want to download on line 9
4. run the script.
