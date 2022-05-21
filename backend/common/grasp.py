# -*- coding = utf-8 -*-
# @Time: 2022/4/15 22:13
# @Auther: Topher
# @File: grasp.py
# @Software: PyCharm

import time
from datetime import datetime
import schedule
from html import unescape
import selenium.webdriver.chrome.service
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则库，文字匹配
import urllib  # 指定url，获取网页数据
from urllib import request
from urllib import response
from urllib import error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlwt  # 进行excel操作
import pymysql
from http import cookiejar

from module.game import Game


def job():
    now = datetime.now()
    print(f"Time now:{now}")
    datalist = []
    baseurlLuogu = "https://www.luogu.com.cn/contest/list"
    baseurlNewCoder = "https://ac.nowcoder.com/acm/contest/vip-index"
    baseurlLeetCode = "https://leetcode-cn.com/contest/"
    baseurlAtCoder = "https://atcoder.jp/contests/"
    baseurlCodeForces = "https://codeforces.com/contests"
    print("Start collecting event data...")
    # 1.爬取
    print("Start collecting Luogu...")
    datalist += getDataLuogu(baseurlLuogu)
    print("Start collecting newcoder...")
    datalist += getDataNewCoder(baseurlNewCoder)
    print("Start collecting leetcode...")
    datalist += getDataLeetCode(baseurlLeetCode)
    print("Start collecting atcoder...")
    datalist += getDataAtCoder(baseurlAtCoder)
    print("Start collecting codeforces...")
    datalist += getDataCodeForces(baseurlCodeForces)
    print("Data collection completed.")

    newList=[]
    for i in datalist:
        try:
            game = Game(game_name=i[0], game_start_time=i[1], game_end_time=i[2], duration=i[3], checked=1,
                         website=i[5], game_type=i[6], level_=i[7], platform=i[8])
            game.add()
            print(i)

        except:
            print('already-exist')
        else:
            print('add-success')
            newList.append(i)
    return newList
    # savepath = ".\\初步收集赛事信息.xls"
    # saveData(savepath, datalist)




# 2.解析数据，通常需要边爬边解，所以在getData中就做掉了
# 3.保存数据到excel，这里要改成存到数据库


# 还没写好的接数据库的模块
# db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='abcdefg123456', db='letscode', charset='utf8')
# cursor = db.cursor()
# sql = "select * from game where game_name="


def getDataLuogu(baseurl):
    datalist = []
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    s = selenium.webdriver.chrome.service.Service(driver_path)
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get(baseurl)
    locator = (By.TAG_NAME, 'a')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located(locator))

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    info = soup.find_all('div', class_="row")
    for item in info:
        item = str(item).replace('\n', '')
        # print(item)
        getStatus = re.compile(r'<span class="status".*?>(.*?)</span>')
        status = re.findall(getStatus, item)[0].strip()
        if status == "已结束":
            break
        data = []
        # findLink = re.compile(r'<a.*href="(.*?)" target="_blank">.*?</a>')
        # link = "https://www.luogu.com.cn" + re.findall(findLink, item)[0]
        findName = re.compile(r'<a.*target="_blank">(.*?)</a>')
        name = re.findall(findName, item)[0].strip()
        name = unescape(name)

        findDate = re.compile(r'<time>(.*?) ..:..</time>')
        findTime = re.compile(r'<time>(.*?)</time>')
        date = "2022-" + re.findall(findDate, item)[0]
        times = re.findall(findTime, item)
        start = "2022-" + times[0]
        end = date + " " + times[1]
        if re.findall('Div.\d', name):
            diff = re.findall('Div.\d', name)[0]
        elif re.findall('普及组', name):
            diff = '普及组'
        else:
            diff = ''
        # 模拟点击获取链接
        element = browser.find_element(by=By.LINK_TEXT, value=name)
        ActionChains(browser).move_to_element(element).perform()
        element.click()
        time.sleep(0.1)
        browser.switch_to.window(browser.window_handles[1])
        link = browser.current_url
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        data.append(name)
        data.append(start)
        data.append(end)
        data.append('')
        data.append(1)
        data.append(link)
        data.append(diff)
        data.append('')
        data.append('洛谷')
        datalist.append(data)

    browser.quit()
    return datalist


def getDataNewCoder(baseurl):
    datalist = []
    html = askUrl(baseurl)
    soup = BeautifulSoup(html, features="html.parser")
    for item in soup.find_all('div', class_="platform-item js-item"):
        data = []
        item = str(item)
        findLink = re.compile(r'<a href="(.*?)" target="_blank">.*</a>')
        findName = re.compile(r'<a href="/acm/contest/.*" target="_blank">(.*?)</a>')
        findStart = re.compile(r'<li class="match-time-icon">比赛时间：    (.*?)\n')
        findEnd = re.compile(r'至     (.*?)\n.*</li>')
        findLength = re.compile(r'\(时长:(.*?)\)</li>')
        findDiff = re.compile(r'<li class="icon-nc-flash2">(.*?)</li>')
        name = re.findall(findName, item)
        link = re.findall(findLink, item)
        trueLink = []
        for singleLink in link:
            trueLink.append("https://ac.nowcoder.com" + singleLink)
        start = re.findall(findStart, item)
        end = re.findall(findEnd, item)
        trueEnd = []
        for i in range(0, len(end)):
            if i % 2 == 1:
                trueEnd.append(end[i])
        # length = re.findall(findLength, item)
        # minutelabel = length.find("分钟")
        # hourlabel = length.find("小时")
        # if minutelabel != -1:
        #     length = length[0:hourlabel] + ":" + length[hourlabel+4:minutelabel]
        diff = re.findall(findDiff, item)
        data.append(name[0])
        data.append(start[0])
        if len(trueEnd) == 0:
            data.append('')
        else:
            data.append(trueEnd[0])
        # if len(length) == 0:
        #     data.append('')
        # else:
        #     data.append(length[0])
        data.append('')
        data.append(1)
        data.append(trueLink[0])
        if len(diff) == 0:
            data.append('')
        else:
            data.append(diff[0])
        data.append('')
        data.append('牛客网')
        datalist.append(data)
    # print(datalist)
    return datalist


def getDataLeetCode(baseurl):
    datalist = []
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    s = selenium.webdriver.chrome.service.Service(driver_path)
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get(baseurl)
    html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html, features="html.parser")
    info = str(soup.find_all('div', class_="contest-card-base col-sm-7 col-xs-6")[0])
    findLink = re.compile(r'a href="/contest/(.*?)"')
    link = re.findall(findLink, info)[0]
    # findHour = re.compile(r'参加这场 (.*?) 小时 .*? 分 的竞赛')
    # findMinute = re.compile(r'参加这场 .*? 小时 (.*?) 分 的竞赛')
    # length = re.findall(findHour, info)[0] + ":" + re.findall(findMinute, info)[0]
    findName = re.compile(r'<div class="card-title .*>(.*?赛)</div>')
    name = re.findall(findName, info)[0]
    findDate = re.compile(r'<div class="time">中国时间：(.*?)：.*')
    findStartTime = re.compile(r'<div class="time">中国时间：.*?：(.*?)~.*')
    findEnd = re.compile(r'<div class="time">.*~(.*?)</div>')
    start = re.findall(findDate, info)[0].strip() + " " + re.findall(findStartTime, info)[0].strip()
    end = re.findall(findDate, info)[0].strip() + " " + re.findall(findEnd, info)[0].strip()
    data1 = []
    data1.append(name)
    data1.append(start)
    data1.append(end)
    # data1.append(length)
    data1.append('')
    data1.append(1)
    data1.append("https://leetcode-cn.com/contest/" + link)
    if '双周赛' in name:
        data1.append('双周赛')
    elif '周赛' in name:
        data1.append('周赛')
    elif '专场竞赛' in name:
        data1.append('专场竞赛')
    else:
        data1.append('其他')
    data1.append('')
    data1.append('LeetCode力扣')
    datalist.append(data1)
    info = str(soup.find_all('div', class_="contest-card-base col-sm-5 col-xs-6")[0])
    findLink = re.compile(r'a href="/contest/(.*?)"')
    link = re.findall(findLink, info)[0]
    findName = re.compile(r'<div class="title">(.*?赛)</div>')
    name = re.findall(findName, info)[0]
    findStartDate = re.compile(r'<span class="time">(.*?)/.*?~.*?</span>')
    findStartTime = re.compile(r'<span class="time">.*?/(.*?)~.*?</span>')
    findEndDate = re.compile(r'<span class="time">.*?~(.*?)/.*?</span>')
    findEndTime = re.compile(r'<span class="time">.*?~.*?/(.*?)</span>')
    start = re.findall(findStartDate, info)[0].strip() + " " + re.findall(findStartTime, info)[0].strip()
    end = re.findall(findEndDate, info)[0].strip() + " " + re.findall(findEndTime, info)[0].strip()
    data2 = []
    data2.append(name)
    data2.append(start)
    data2.append(end)
    data2.append('')
    data2.append(1)
    data2.append("https://leetcode-cn.com/contest/" + link)
    if '双周赛' in name:
        data2.append('双周赛')
    elif '周赛' in name:
        data2.append('周赛')
    elif '专场竞赛' in name:
        data2.append('专场竞赛')
    else:
        data2.append('其他')
    data2.append('')
    data2.append('LeetCode力扣')
    datalist.append(data2)
    # print(datalist)
    return datalist


def getDataAtCoder(baseurl):
    datalist = []
    html = askUrl(baseurl)
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup)
    form = soup.find('div', id="contest-table-upcoming")
    info = form.find('tbody')
    for item in info.find_all('tr'):
        data = []
        item = str(item)
        # print(item)
        findTD = re.compile(r'<td class="text-center">(.*?)</td>')
        TD = re.findall(findTD, item)
        # print(TD)
        length = TD[1]
        diff = 'AtCoder ' + TD[2]
        findStart = re.compile(r'<time class="fixtime fixtime-full">(.*?):00\+0900</time>')
        start = re.findall(findStart, TD[0])[0]
        # print(start)
        findLink = re.compile(r'<a href="(.*?)">')
        link = "https://atcoder.jp" + re.findall(findLink, item)[1]
        findName = re.compile(r'<a href="/contests/.*">(.*?)</a>')
        name = re.findall(findName, item)[0]
        data.append(name)
        data.append(start)
        data.append('')
        data.append(length)
        data.append(1)
        data.append(link)
        data.append(diff)
        data.append('')
        data.append('AtCoder')
        # print(data)
        datalist.append(data)

    return datalist


def getDataCodeForces(baseurl):
    # datalist = []
    # html = askUrl(baseurl)
    # soup = BeautifulSoup(html, features="html.parser")
    # #print(soup)
    # checkRedirect = "Redirecting"
    # strsoup = str(soup)
    # if checkRedirect in strsoup:
    #     checkUrl = re.compile(r'.*document.location.href="(.*?)";.*')
    #     realUrl = re.findall(checkUrl,strsoup)[0]
    #     html = askUrl(realUrl)
    #     soup = BeautifulSoup(html, features="html.parser")
    #     print(soup)
    datalist = []
    driver_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    s = selenium.webdriver.chrome.service.Service(driver_path)
    options = Options()
    options.add_argument('-headless')
    browser = webdriver.Chrome(service=s, options=options)
    browser.get(baseurl)
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html, features="html.parser")
    form = soup.find('div', class_="datatable")
    info = form.find('table')
    rows = info.find_all('tr')
    initial = 0
    for item in rows:
        if initial == 0:
            initial = 1
            continue
        data = []
        item = str(item).strip()
        # print(item)
        findLink = re.compile(r'<tr data-contestid="(.*?)">')
        link = "https://codeforces.com/contests/" + re.findall(findLink, item)[0]
        # print(link)
        findTD = re.compile(r'<td.*?>(.*?)</td>', re.S)
        TD = re.findall(findTD, item)
        TD[2] = TD[2].replace('\n', '')
        name = TD[0].strip()
        startMonth = re.findall('.*?>(.*?)/.*?<sup.*', TD[2])[0].strip()
        startDay = re.findall('.*?>.*?/(.*?)/.*?<sup.*', TD[2])[0].strip()
        startYear = re.findall('.*?>.*?/.*?/(.*?) .*?:.*<sup.*', TD[2])[0].strip()
        startTime = re.findall('.*?>.*?/.*?/.*? (.*?)<sup.*', TD[2])[0].strip()
        Monthdict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                     "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        start = startYear + "-" + Monthdict[startMonth] + "-" + startDay + " " + startTime
        end = ""
        length = TD[3].strip()
        if len(re.findall("(Div. \d)", name)) == 0:
            diff = ''
        else:
            diff = re.findall("(Div. \d)", name)[0]
        data.append(name)
        data.append(start)
        data.append(end)
        data.append(length)
        data.append(1)
        data.append(link)
        data.append(diff)
        data.append('')
        data.append('CodeForces')
        datalist.append(data)
        # print(datalist)

    return datalist


# 获取一个指定的URL的网页内容，用于静态网页爬取
def askUrl(url):
    # 模仿浏览器头部信息，向服务器发送信息
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        # "cookie": "__client_id=8a0f2ea889c94963e96578ae0c80440a54faf083; _uid=0; UM_distinctid=1802ecd4ccc33b-05734aaa87122f-978183a-144000-1802ecd4ccdda2; CNZZDATA5476811=cnzz_eid%3D88324547-1650042609-%26ntime%3D1650042609"
        # "accept-encoding": "gzip, deflate, br",
        # "accept-language": "zh,en;q=0.9,zh-CN;q=0.8,ja;q=0.7"
        # "cookie": "__client_id=4fc08e1c1261fa05be52868476682bab436a7941; UM_distinctid=1802d5f1df7356-0d03b0dda40d63-978183a-144000-1802d5f1df8df6; CNZZDATA5476811=cnzz_eid%3D1562450822-1650019661-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1650042609; _uid=0; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fcontest%2Flist; arp_scroll_position=0"
    }
    # cj = cookiejar.CookieJar()
    # pro = request.HTTPCookieProcessor(cj)
    # opener = request.build_opener(pro)
    # opener.addheaders = head

    # 用户代理，表示告诉服务器我们的机器类型、浏览器类型
    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        # response = opener.open(url, data=None, timeout=0.01)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 保存数据
def saveData(savepath, datalist):
    print("Saving to xls document...")
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet("DB Movie Top 250 Info")
    sheet.write(0, 0, 'game_name')
    sheet.write(0, 1, 'game_start')
    sheet.write(0, 2, 'game_end')
    sheet.write(0, 3, 'duration')
    sheet.write(0, 4, 'checked')
    sheet.write(0, 5, 'website')
    sheet.write(0, 6, 'game_type')
    sheet.write(0, 7, 'game_level')
    sheet.write(0, 8, 'platform')
    i = 0
    for item in datalist:
        j = -1
        i += 1
        for detail in item:
            j += 1
            sheet.write(i, j, detail)
    print("Data saved to %s." % savepath)
    book.save(savepath)


def timeprint():
    now = datetime.now()
    print(f"Time now:{now}")


if __name__ == '__main__':

    schedule.every(5).seconds.do(timeprint)  # 5秒输出一次时间，方便调试
    schedule.every(2).minutes.do(job)  # 设置成2分钟爬一次，方便调试，最终版本应该是下面这行
    # 亲测函数运行时间会影响计时，应该是运行完才开始计时，所以不用太在意，只要确定是定时在运行就好，最后建议设定成准确时间运行（见下一行）
    # schedule.every().day.at("04:30").do(job)    #按照SRS需要应该是每天4点~6点维护时间，所以设定为每天凌晨4点半爬取
    # 另外是考虑这些信息要不要写log

    while True:
        schedule.run_pending()
