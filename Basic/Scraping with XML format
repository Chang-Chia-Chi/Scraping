"""# XML"""

#Form data or Query String Parameter代入方式
import requests

#進行 POST 請求時要攜帶資料，以字典形式輸入
form_data = {
    "commandid": "GetTown",
    "cityid": "01"
}
request_url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
response = requests.post(request_url, data=form_data)
print(response.status_code)

response_content = response.content
print(type(response_content))
print(response_content)

#lxml解析資訊
from lxml import etree
from io import BytesIO  #bytes類別的Input及Output

file = BytesIO(response_content)
tree = etree.parse(file)
#以lxml解析資料時，以上四行為必帶程式碼
town_names = [t.text for t in tree.xpath("//TownName")] # XPath 亦可以指定 /iMapSDKOutput/GeoPosition/TownName
print(town_names)

#Form data or Query String Parameter代入方式
import requests

#進行 POST 請求時要攜帶資料，以字典形式輸入
form_data = {
    'commandid': 'SearchRoad',
    'city': '台北市',
    'town': '松山區'
}
request_url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
response = requests.post(request_url, data=form_data)  #取出xml資料
response_content = response.content #xml資料轉換
print(response.status_code)

from lxml import etree
from io import BytesIO  #bytes類別的Input及Output

file = BytesIO(response_content)
tree = etree.parse(file)
#以lxml解析資料時，以上四行為必帶程式碼
road_names = [t.text for t in tree.xpath("//rd_name_1")] # XPath 亦可以指定 /iMapSDKOutput/GeoPosition/rd_name_1
print(road_names)

#取得台北市所有的店舖

#Import必要函式庫
import requests
from lxml import etree
from io import BytesIO  #bytes類別的Input及Output
#產生不同區域相對應的form data，並將店鋪對應資料鍵入字典中
store_dict={}
request_url = "https://emap.pcsc.com.tw/EMapSDK.aspx" #向網站提出資料請求
for town in town_names:
  form_data ={'commandid': 'SearchStore','city': '台北市','town': town}
  response = requests.post(request_url, data=form_data) #取出xml資料
  response_content = response.content #轉換xml資料
  file = BytesIO(response_content) #Bytes Input/Output
  tree = etree.parse(file) #解析xml資料
  Poiids = [t.text.strip() for t in tree.xpath("//POIID")]
  Poinas = [t.text for t in tree.xpath("//POIName")] 
  xs = [float(t.text)/1000000 for t in tree.xpath("//X")]
  ys = [float(t.text)/1000000 for t in tree.xpath("//Y")]
  Tels = [t.text for t in tree.xpath("//Telno")]
  faxs = [t.text for t in tree.xpath("//FaxNo")]
  Addrs = [t.text for t in tree.xpath("//Address")]
  store_dict[town] = []
  for Poiid,Poina,x,y,Tel,fax,Addr in zip(Poiids,Poinas,xs,ys,Tels,faxs,Addrs):
    store_info = {
        'ID':Poiid,
        'Name':Poina,
        'xdir':x,
        'ydir':y,
        'Tel':Tel,
        'Fax':fax,
        'Address':Addr
    }
    store_dict[town].append(store_info)

print(store_dict)
print(store_dict['松山區'][0])
