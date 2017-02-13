#! /usr/bin/env python2
# coding=utf-8

'''
Info
- author : "fekgih-yumin"
- email  : "fekgih@hotmail.com"
- date   : "2017.2.13"
'''

from bs4 import BeautifulSoup
import requests
import xlwt
import os
from django.http import HttpResponse
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# 获得某一个月的天气数据
def get_list(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    weathers=soup.select("#tool_site")
    # print "tool_site:   "
    # print weathers
    title=weathers[1].select("h3")[0].text
    weatherInfors=weathers[1].select("ul")
    weatherList=list()
    for weatherInfor in weatherInfors:
        singleweather=list()
        for li in weatherInfor.select('li'):
            singleweather.append(li.text)
        weatherList.append(singleweather)
    print (title)
    return weatherList,title

def get_list_by_address(addressUrl,excelSavePath):
    url=addressUrl
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    dates=soup.select(".tqtongji1 ul li a")
    # print ".tqtongji1 ul li a :  "
    # print dates
    workbook=xlwt.Workbook(encoding='utf-8')
    for d in dates:
        weatherList,title=get_list(d["href"])
        booksheet=workbook.add_sheet(title,cell_overwrite_ok=True)
        for i,row in enumerate(weatherList):
            for j,col in enumerate(row):
                booksheet.write(i,j,col)
    workbook.save(excelSavePath)

# def get_weather(request):
if __name__ == '__main__':
    # addressName=raw_input("请输入即将获取天气的城市：\n")
    addresses1=BeautifulSoup(requests.get('http://lishi.tianqi.com/').text,"html.parser")
    addresses=addresses1.select("a")
    addressList=list()
    for address1 in addresses:
        address1 = address1.string
        if address1 != None:
            if "首页" not in address1 and "娱乐" not in address1 and "范文" not in address1 and "律师" not in address1 or len(address1) == 3 and "区" in address1:
                print address1
                addressList.append(address1)
    print "----------------进入查询"
    for addressName in addressList:
    # for addressName in addresses:
        queryAddress = addresses1.find_all('a', text=addressName)
        # queryAddress = addresses
    # if len(queryAddress):
    #     print addressName
    #     savePath = raw_input(
    #         "检测到有该城市数据，请输入即将保存天气数据的路径（如若不输入，将默认保存到/Users/wufan/python/weather/" + addressName + ".xls）:\n")
    #     if not savePath.strip():
    #         if not os.path.exists('/Users/wufan/python/weather'):
    #             os.mkdir('/Users/wufan/python/weather')
        savePath = "/Users/wufan/python/weather/" + addressName + ".xls"
        for q in queryAddress:
            if "http://lishi.tianqi.com/" in q["href"] and "北京历史天气查询" not in addressName and "历史天气" not in addressName:
                get_list_by_address(q["href"], savePath)
                print ("已经天气数据保存到:", savePath)
    else:
        print ("不存在该城市的数据")
    # return HttpResponse("ok")
