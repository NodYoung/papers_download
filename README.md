# papers_download
download papers' pdf from http://sci-hub.cc/ automatically


## 任务描述
papers.xlsx中存储有需要下载的论文详细，从[sci-hub](http://sci-hub.cc/) 下载论文对应的pdf文件到本地。


## 部分细节介绍
- 写了自己用的小工具，本项目使用selenium库实现爬虫功能
- transfer.py负责提取到papers.xlsx中的paper id和title到papers.txt当中
- crawler.py负责从papers.txt中读取paper title，爬取相应pdf文件后以paper id命名，并保存到download文件夹。
其中，对于可以下载到的论文记录其信息到download.txt，无法下载到的论文记录其信息到notdownload.txt
- crawler.py中对于验证码的处理方法是当检查到网页中出现验证码时，声音警报提醒用户手动输入 
- 针对爬虫速度慢的问题，下一步改进可以从多线程多进程入手。 

