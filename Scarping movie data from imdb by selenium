def get_movie_info(search_movie_title):
  from selenium import webdriver

  #使用特定環境執行，必須指定driver_path
  driver_path = "C:/Python/chromedriver.exe"
  driver = webdriver.Chrome(executable_path=driver_path) # Use Chrome
  imdb_home = "https://www.imdb.com/"
  #driver = webdriver.chrome()
  driver.get(imdb_home)
  #print(driver.current_url)

  #xpath tag
  movie_title_xpath = "//h1"
  movie_poster_xpath = "//div[@class='poster']/a/img"
  movie_rating_xpath = "//strong/span"
  movie_type_xpath = "//div[@class='subtext']/a"
  movie_cast_xpath = "//td[2]/a"
  imdb_search_input = "//input[@id='suggestion-search']"
  imdb_search_button = "//button[@id='suggestion-search-button']" 
  imdb_search_movie = "//ul[@class='findTitleSubfilterList']/li[1]/a"
  imdb_search_result = "//tr/td[@class='result_text']/a"

  #movie_title input
  elem = driver.find_element_by_xpath(imdb_search_input)
  elem.send_keys(search_movie_title)
  #click search button
  elem = driver.find_element_by_xpath(imdb_search_buttom)
  elem.click()
  #only movie category
  elem = driver.find_element_by_xpath(imdb_search_movie)
  elem.click()
  #search results
  elems = driver.find_elements_by_xpath(imdb_search_result)
  #get url and click to most relevant result
  first_elem = elems[0]
  first_elem.get_attribute("href")
  first_elem.click()
  #scrape information about movie
  movie_data = {}
  elem = driver.find_element_by_xpath(movie_title_xpath)
  movie_data['movie_title'] = elem.text
  elem = driver.find_element_by_xpath(movie_poster_xpath)
  movie_data['poster'] = elem.get_attribute("src")
  elem = driver.find_element_by_xpath(movie_rating_xpath)
  movie_data['rating'] = elem.text
  elems = driver.find_elements_by_xpath(movie_type_xpath)
  movie_types = [e.text for e in elems]
  movie_data['release_date'] = movie_types.pop()
  movie_data['movie_types'] = movie_types
  elems = driver.find_elements_by_xpath(movie_cast_xpath)
  movie_data['movie_cast'] = [e.text for e in elems]
  driver.close()
  return movie_data
Avengers_movie_data = get_movie_info('Avengers')

#output data in json format
import json
with open("avengers.json", "w") as f:
    json.dump(Avengers_movie_data, f)
