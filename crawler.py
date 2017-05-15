# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import requests
import re
import winsound

# 分别记录能下载到的论文和不能下载到的论文
download_file = 'download.txt'
notdownload_file = 'notdownload.txt'
# 论文下载网址
base_url = 'http://sci-hub.cc/'

# 获取所有paper的ID和title，下载后的论文以ID命名
def get_paper(papers_file):
    papers = []
    with open(papers_file, 'r') as f:
        for line in f.readlines():
            paper = line.strip().split(',')
            papers.append(paper)
    return papers


def init(papers_file, load_timeout=60):
    papers = get_paper(papers_file)  # 获得paper列表
    open(download_file, 'w').close()  # 清空文件夹
    open(notdownload_file, 'w').close()
    browser = webdriver.Chrome()  # 初始化浏览器
    browser.set_page_load_timeout(load_timeout)    #set the amount of time to wait for a page load to complete before throwing an error.
    return papers, browser


# 下载一篇论文
def download(browser, paper):
    browser.get(base_url)
    browser.find_element_by_xpath('//*[@id="input"]/form/input[2]').send_keys(paper[1])  # 输入论文title
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="open"]').click()  # 点击搜索按钮
    time.sleep(1)
    cur_url = browser.current_url  # 获得跳转后的网址
    allow_domain = r'.*sci\-hub\.cc.*'  # 网址域名匹配模式
    if re.match(allow_domain, cur_url):  # 跳转后依然在本域名内
        try:
            pdf_src = browser.find_element_by_xpath('//iframe[@id="pdf"]').get_attribute('src') # paper's pdf源地址
            # 切换到iframe当中
            browser.switch_to_frame(browser.find_element_by_xpath('//iframe[@id="pdf"]'))
            try:
                # 遇到有验证码，声音报警，并等待30秒钟以方便手动输入验证码
                browser.find_element_by_xpath('/html/body/div/table/tbody/tr/td/form/input')
                winsound.PlaySound('alert', winsound.SND_ASYNC)
                time.sleep(30)
            except:
                pass
            finally:
                with open(download_file, 'a') as f:  # 记录已经下载的论文id
                    f.write("%s\n" % paper[0])
                with open('download/'+paper[0]+'.pdf', 'wb') as f:  # 下载论文
                    f.write(requests.get(pdf_src).content)
        except:
            with open(notdownload_file, 'a') as f:  # 找不到论文，记录一下
                f.write("%s\n" % paper[0])
    else:  # 本网页内没有这篇论文，但链接到了论文的源头，记录其源头
        with open(notdownload_file, 'a') as f:
            f.write("%s,%s\n" % (paper[0], cur_url))


def main(papers_file):
    papers, browser = init(papers_file)
    for paper in papers:
        download(browser, paper)


if __name__ == '__main__':
    main('papers.txt')