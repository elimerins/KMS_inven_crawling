from bs4 import BeautifulSoup
import requests
import openpyxl

req = requests.get('https://www.koreabaseball.com/Record/Team/Hitter/Basic1.aspx')
req.encoding=None

html=req.text

soup= BeautifulSoup(html,'html.parser')
tds=soup.find("tbody")

trs=tds.find_all("td")

arr = list(range(14))
memo=""
for idx,i in enumerate(trs):

    if idx%15 in arr:
        memo+=i.text+","
    elif idx%15==14:
        memo+=i.text+'\n'

f=open('memo.txt','a')
f.write(memo)
f.close