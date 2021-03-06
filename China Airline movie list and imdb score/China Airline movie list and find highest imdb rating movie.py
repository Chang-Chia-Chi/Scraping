import requests
from bs4 import BeautifulSoups

#由華航首頁進入movie分頁
select_cs = '#main_navigation a'
url = 'http://www.fantasy-sky.com'
language_cookie = {
    'COOKIE_LANGUAGE':'en'
}
response_url = requests.get(url,cookies = language_cookie)
request_text = response_url.text
soup = BeautifulSoup(request_text)
select_cs_tag = soup.select(select_cs)
movie_href = select_cs_tag[2].get('href')
movie_url = url + movie_href
#print(movie_url)

#取得電影分類及對應href  (除href,也可用query string parameter處理)
response_url = requests.get(movie_url,cookies = language_cookie)
request_text = response_url.text
soup = BeautifulSoup(request_text)
list_cs = '.content-category-list a'
list_cat = [e.text for e in soup.select(list_cs)]
list_href = [e.get('href') for e in soup.select(list_cs)]

#依分類取得電影清單
movie_lst_dict = {}
movie_lst_tot = []
for i in range(len(list_cat)):
  cat = list_cat[i]
  movie_lst_cs ='.movies-name'
  movie_cat_url = url+list_href[i]
  response_url = requests.get(movie_cat_url,cookies = language_cookie)
  request_text = response_url.text
  soup = BeautifulSoup(request_text)
  if cat not in movie_lst_dict:
    movie_lst_dict[cat] = []
  movie_lst = [e.text for e in soup.select(movie_lst_cs)]
  movie_lst_dict[cat].append(movie_lst)
  movie_lst_tot += movie_lst
print(movie_lst_dict)
print(movie_lst_tot)

#創建[[電影名稱,評分],[],[]...]的串列
movie_lst_rating = []
for name in movie_lst_tot:
  try:
    get_movie_data(name)
  except:
    print(name,'無搜尋結果')
  else:
    rat = get_movie_data(name)['rating'].pop().pop()
    movie_lst_rating.append([name,rat])
    print(name,rat) 
movie_lst_rating.sort(key = lambda x:x[1],reverse=True)
#print(movie_lst_rating)

#找出評分最高的電影
max_rating_movie = movie_lst_rating[0]
movie_lst_rating.pop(0)
for i in movie_lst_rating:
  if i[1] == max_rating_movie[1]:
    max_rating_movie.append(i)
print(max_rating_movie)
