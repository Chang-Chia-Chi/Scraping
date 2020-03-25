#DaiNing Project

This is the first python side project I'v done which is requested by my gf with some basic tools for scraping, pandas and numpy.
The purpose of the project is to figure out whether goverment agencies in Taoyuan City uploaded
budget proposal for years in interest. Opening each website by hand is a waste of time because 
there are almost a hundred orginizations we have to check, and it's just maybe 1/10 of all btw.

Here's an example:
Go to website 
https://www.dayuan.tycg.gov.tw/home.jsp?id=40&parentpath=0,5&mcustomize=multimessages_list.jsp&qclass=201410290024
and you'll find a list of budget proposal for each year as shown below.

![image](https://github.com/Chang-Chia-Chi/Scraping/blob/master/Pic/ex1.jpg)

First thing is to build a excel file has all the agencies you want to observe with important parameter you need for scraping.

![image](https://github.com/Chang-Chia-Chi/Scraping/blob/master/Pic/ex.2.jpg)

Then scrape the text related to budget for each agency, judge which years are lost within the interest range. 

Through programming I'll get a dictionary with name of agency as key and a value in list like ["v",..."no data",..."v"], "V" means
I can find the file for certain years and "no data" means I can't.
Finally use pandas to tranform the dictionary I got from above as dataframe and output it in .csv form.

![image](https://github.com/Chang-Chia-Chi/Scraping/blob/master/Pic/ex.3.jpg)
