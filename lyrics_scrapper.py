from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib.error

hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

for i in range(0,6278): #site has 6278 pages where one can do GET request which makes scrapping so easy
    url = "https://www.lyricsindia.net/songs/"+str(i+1)
    req=Request(url, headers=hdr)
    
    try:
      html = urlopen(req)
      soup = BeautifulSoup(html, 'lxml')
      contents=soup.pre.contents
      content_list=contents[0].split("\r\n") #creates list of sentences seperated by nextline
      
      with open("txt_gen/" + "lyrics"+ str(i+1) + ".txt", 'w', encoding="utf-8") as f:
          f.write("\n".join(i for i in content_list if i != '')) #if condition removes unnecessary blanklines
    
    except urllib.error.HTTPError as e:
      print("missing lines : ", i)
    
    if i%100==0:
      print("completed lyrics till :", i)