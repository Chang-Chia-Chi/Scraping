import numpy as np
import pandas as pd
import requests
from lxml import etree
from io import BytesIO 
from bs4 import BeautifulSoup
import datetime
import time

#讀入機關資料
data_path = "https://dainingtest.s3-ap-northeast-1.amazonaws.com/test_data.xlsx"
data_df = pd.read_excel(data_path)

#取得機關列表
#orgin_name = list(data_df["機關名稱"].unique())

#定義html_get網頁資料讀取
def get_budget_html_get(url):
  response = requests.get(url)
  text = response.text
  soup = BeautifulSoup(text)
  return soup

#定義html_post網頁資料讀取
def get_budget_html_post(url,form_data = None):
  response = requests.post(url,form_data)
  text = response.text
  soup = BeautifulSoup(text)
  return soup

#定義xml_get網頁資料讀取
def get_budget_xml_get(url):
  response = requests.get(url)
  response_content = response.content
  file = BytesIO(response_content)
  tree = etree.parse(file,etree.HTMLParser())
  return tree

#判斷名稱是否為所需檔案函式
def filter_fun(string,year):
  year = str(year)
  filter_1 = [year,"年","預算"]
  filter_2 = [year,"法定","預算"]
  filter_3 = [year,"單位","預算"]
  flag = True
  #三個filter的判定
  for fil in filter_1:
    if fil not in string:
      for fil in filter_2:
        if fil not in string:
          for fil in filter_3:
            if fil not in string:
              flag = False
              break
  return flag

#當預算及決算放在同一xpath時的過濾函式
def final_filter(lst):
  index = len(lst)
  if int(lst[0]) - int(lst[1]) < 0:
    for i in range(len(lst)-1):
      if int(lst[i+1]) - int(lst[i]) <=0:
        index = i
        break
  if int(lst[0]) - int(lst[1]) > 0:
     for i in range(len(lst)-1):
      if int(lst[i+1]) - int(lst[i]) >=0:
        index = i
        break   
  lst = lst[:index+1]
  return lst

#判斷單一元素是否為NaN (Python定義NaN為float，且不等於任何其他float)
def isnan(num):
  return num != num

#將各機關年份清單中，缺乏的年份補上no data
def add_nodata(lst):
  new_lst = lst.copy()
  count = 0
  total_count = 0
  for i in range(len(lst)-1):
    if int(lst[i+1]) - int(lst[i]) > 1:  #判斷年份是否不連續
      count = int(lst[i+1]) - int(lst[i]) - 1
      low_end = i + 1 + total_count   #需增補no data的最小索引
      high_end = low_end + count + 1  #需增補no data的最大索引
      for y in range(count):
   #     new_lst.append('no data')   #擴張年度串列(根本不用)
   #     no_data = new_lst.pop()     #pop() no data資料(根本不用)
        new_lst.insert(low_end,"no_data") #將"no data"插入年份空白處
      total_count += count

  #填補no data至最新年度
  if int(year_lst[-1]) > int(new_lst[-1]):
    lens = int(year_lst[-1]) - int(new_lst[-1])
    new_lst = new_lst + ["no data"]*lens

  #填補no data至最舊年度
  if int(year_lst[0]) < int(new_lst[0]):
    lens = int(new_lst[0]) - int(year_lst[0])
    new_lst = ["no data"]*lens + new_lst
  return new_lst

#輸入查詢最後年分
nowtime = datetime.datetime.now() #取得當前時間
nowyear = nowtime.year - 1911  #取得當前年分(民國)
year = int(input("請輸入查詢最後年度:\n104 ~ ")) #輸入最後查詢年度
while year>nowyear:
  print("超過目前年份，請重新輸入")
  year = int(input("請輸入查詢最後年度:\n"))
  nowtime = datetime.datetime.now()
  nowyear = nowtime.year - 1911  #計算民國年分
year_lst = [str(e) for e in range(104,year+1)] #產生年度清單

#依序讀取各機關預算清單
data_num = data_df.shape[0] #取得機關數量
orgin_dict = {} #產生機關與上傳預算清單的字典
form_data = {"pagesize":"100"} #若有多頁清單時，將單頁數量改為100筆
url_lst = []
for i in range(data_num):
  time.sleep(0.1)
  orgin_name = data_df.loc[i,"機關名稱"]
  url = data_df.loc[i,"預算書網址"]
  url_lst.append(url) 
  #依網頁格式、請求方法及有無多頁面，取得soup物件
  if data_df.loc[i,"格式"] == "html":
    if data_df.loc[i,"Request Method"] == "get":
      soup_data = get_budget_html_get(url)
    else:
      if not isnan(data_df.loc[i,"Form Data"]):
        soup_data = get_budget_html_post(url,form_data,)
      else:
        soup_data = get_budget_html_post(url) 
    #套入css selector 取得資料
    css = data_df.loc[i,"CSS selector"]
    tag = soup_data.select(css)
    budget_lst = [data.text.strip() for data in tag]
    #挑出104~"輸入年份"的預算清單
    budget_lst = [data.replace(".pdf","") for data in budget_lst for year in year_lst if filter_fun(data,year)==True]
     
    #將預算案清單表示成年度                   
    budget_lst  = [(''.join(filter(str.isdigit, data)))[:3] for data in  budget_lst] #取出年份
    budget_lst =  sorted(list(set(budget_lst)))  #刪除重複值並排序
    budget_lst  = add_nodata(budget_lst)  #若某年份無資料則填補no data  
    orgin_dict[orgin_name] = budget_lst   
  elif data_df.loc[i,"格式"] == "xml":
    tree_data = get_budget_xml_get(url)
    #套入xpath 取得資料
    path = data_df.loc[i,"CSS selector"]
    tag = tree_data.xpath(path)
    budget_lst = [e.text.strip() for e in tag]
    #挑出104~"輸入年份"的清單
    budget_lst = [(''.join(filter(str.isdigit,data)))[:3] for data in budget_lst] #取出年份
    budget_lst = [data for data in budget_lst if data in year_lst] #將104 ~ 109 以外的資料排除
    budget_lst = [data for data in budget_lst if "決算" not in data] #過濾掉含"決算"2字的內容
    budget_lst = final_filter(budget_lst) #過濾掉決算內容
    budget_lst = sorted(list(set(budget_lst)))  #刪除重複值並排序
    budget_lst  = add_nodata(budget_lst)  #若某年份無資料則填補no data 
    orgin_dict[orgin_name] = budget_lst 
  else:
    pass 

#orgin_dict["桃園市中壢區公所"][0] = "no data" 配合DataFrame重建字典測試用

#配合DataFrame重建字典
dict_for_df = {}
dict_for_df["name"] = list(orgin_dict.keys())
for i in range(len(year_lst)):
  yesno_lst = []
  for name in dict_for_df["name"]:
    if orgin_dict[name][i] == "no data":
      yesno_lst.append("no data")
    else:
      yesno_lst.append("V")
  dict_for_df[year_lst[i]] = yesno_lst

#增加網址字典
dict_for_df["網址"] = url_lst

#建立DataFrame
output_df = pd.DataFrame(dict_for_df)

#輸出為csv
output_df.to_csv('各機關預算書上傳狀況.csv',encoding='utf-8-sig')
