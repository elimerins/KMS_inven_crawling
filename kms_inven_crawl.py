from bs4 import BeautifulSoup
import requests
import pandas as pd

req = requests.get("http://www.inven.co.kr/board/maple/2816?sort=PID&p=1")
req.encoding=None

html=req.text

soup= BeautifulSoup(html,'html.parser')

form=soup.find('form',{'name':'board_list1'})
trs=form.find_all('tr')

df = pd.DataFrame(columns=['main_cate','sub_cate','title'])


def KMS_Crawling(url):
    inven_url = url
    dict = {'도전!기자단': '2316',
            '전사': '2294',
            '마법사': '2295',
            '궁수': '2297',
            '해적': '2298',
            '베스트유저리포트': '2816',
            '실시간소식공지': '2314',
            '팁과 노하우': '2304',
            '자유게시판': '2299',
            '질문과답변': '2300',
            '메이플에 바란다': '2587',
            '사고팔고': '2357',
            '길드/친구/농장찾기': '2302'
            }
    # 게시판 별 dictionary화
    url_msg = '?sort=PID&p='  # 페이지 이동을 위한 MSG

    for idx, key in enumerate(dict.keys()):
        print(key + ' start!')
        pagenum=0
        for i in range(1, 200):
            try:

                base_url = inven_url + dict[key] + url_msg + str(i)
                #print(base_url)

                html = requests.get(base_url)

                print(key + ' ' + str(i) + 'page start')
                soup = BeautifulSoup(html.text, 'html.parser')  # soup로 변경
                #print('soup created')
                form = soup.find('form', {'name': 'board_list1'})  # html속에서 form을 찾음
                trs = form.find_all('tr')  # form 에서 tr 들만 선별
                if len(trs) < 5:
                    break
                pagenum += 1
                for tr in trs:

                    notice = 0
                    imgs = tr.find_all('img', src=True)
                    for img in imgs:
                        if img['src'] == "http://www.inven.co.kr/board/bbs/skin/notice_img/notice.gif":
                            notice = 1
                            print("notice detect!")
                    td = tr.find('a', {'class', 'sj_ln'})
                    # title text가 있는 곳 선별
                    if td is None:
                        continue
                    if notice == 0:
                        # 공지 이미지가 있는 tr pass
                        list_tdtext = list(td.text)
                        sub_category = ''.join(list_tdtext[list_tdtext.index('[') + 1:list_tdtext.index(']')])
                        # title 앞에 [ 와 ]가 있으므로 sub_cate로 구분
                        # print(sub_category)
                        while '\xa0' in list_tdtext:
                            list_tdtext.remove('\xa0')

                        title = ''.join(list_tdtext[list_tdtext.index(']') + 1:])
                        #print(title)
                        # sub_cate 인덱스 이후 list를 다시 title 변수로 지정

                        df.loc[len(df)] = [key, sub_category, title]
                        # df 문서에 하나씩 삽입
                print(key + ' ' + str(i) + 'page end!\n')  # 게시판 1 페이지 종료!
            except Exception as e:
                print('No more page.')
            # break
        print(key + ' end!\n' + str(pagenum) + 's complete')
        df.to_csv('./kms_crawl_alpha.csv', sep=',', na_rep='NaN')

KMS_Crawling('http://www.inven.co.kr/board/maple/')