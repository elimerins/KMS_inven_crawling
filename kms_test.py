from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

df = pd.DataFrame(columns=['main_cate','sub_cate','title'])

def getText(url):
    url = url
    html = urlopen(url)
    source = html.read()  # 바이트코드 type으로 소스를 읽는다.
    html.close()  # urlopen을 진행한 후에는 close를 한다.

    soup = BeautifulSoup(source, "html.parser")  # 파싱할 문서를 BeautifulSoup 클래스의 생성자에 넘겨주어 문서 개체를 생성, 관습적으로 soup 이라 부름
    table = soup.find(id="webzineNewsList")
    categories = table.find_all(class_="title")

    return categories


def Crawling(label, num):
    if num == 100:
        return
    if num % 5 == 0:
        print(str(num % 100) + "%완료 하였습니다.")
    for i in range(1,86):
        sub=''
        url = "http://www.inven.co.kr/webzine/news/?hotnews=1&page="+str(i)+"&premonth=" + str(num)
        categories = getText(url)
        print('page '+str(i)+' start')
        for cat in categories:
            title = cat.get_text()
            l_title = list(title)
            if '[' in l_title and l_title.index('[') == 0:
                sub=''.join(l_title[l_title.index('[')+1:l_title.index(']')])
                title = ''.join(l_title[l_title.index(']') + 1:-4])
            else:
                sub=''
                title = ''.join(l_title[:-4])

            print(sub+'!'+title)

            df.loc[len(df)] = [label, sub, title]  # df에 title과 label 하나씩 추가.
        print(str(num)+'month, '+str(i)+'page is done')
        df.to_csv('./inven_crawl.csv', sep=',', na_rep='NaN')

    Crawling(label,num+1)

Crawling('news', 1)