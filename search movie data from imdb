#以movie title進行搜尋
def get_movie_data(movie_title):
  #CSS selector 標記 lsit
  css_dict = {
      'movie_title_cs' : 'h1',
      'movie_poster_cs' : '.poster img',
      'movie_rating_cs' : 'strong span',
      'movie_release_date_cs' : '.subtext a',
      'movie_cast_cs' : '.primary_photo+ td a'
  }
    QS_Parameter = {
       'q': movie_title,
       's': 'tt',
       'ttype': 'ft',
       'ref_': 'fn_ft'
  }
  url = 'https://www.imdb.com/find'
  requests_url = requests.get(url, QS_Parameter)
  response_text = requests_url.text
  soup = BeautifulSoup(response_text)
  result_text_cs = '.result_text > a'
  result_hrefs = [e.get('href') for e in soup.select(result_text_cs)]
  movie_href = result_hrefs[0]
  movie_url1 = 'https://www.imdb.com%s'%(movie_href)
  requests_url = requests.get(movie_url1)
  response_text = requests_url.text
  soup = BeautifulSoup(response_text)
  data_list = ['title','poster','rating','release_date','cast']
  css_dict_keys = ['movie_title_cs','movie_poster_cs','movie_rating_cs',
                   'movie_release_date_cs','movie_cast_cs']
  movie_data = {}
  for i in range(len(data_list)):
    data = data_list[i]
    css_dict_key = css_dict_keys[i]
    if data not in movie_data:
      movie_data[data] = []
    element_tag = soup.select(css_dict[css_dict_key])
    if data == 'poster':
      content = [tag.get('src') for tag in element_tag]
      movie_data[data].append(content)
    else:
      content = [tag.text.strip().replace('\xa0',' ') for tag in element_tag]
      movie_data[data].append(content)
  return movie_data, movie_url1

movie_dict = get_movie_data('寄生上流')
print(movie_dict)
