import requests
from bs4 import BeautifulSoup
import json
import time
import datetime

ERROR_SLEEP_TIME=10
SLEEP_TIME=20

#获取网页html
def get_html(url,data):
    #url指请求的网址；data指请求时带的参数
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'Connection':"keep-alive",
    }
    response=requests.get(url,data,headers=headers)
    response.encoding='gbk'
    #返回网页源码html
    return response.text

#解析传入的网页，抽取出网页中的字段内容
def parse(html):
    soup=BeautifulSoup(html)
    table=soup.find("table",attrs={"id":"report"})
    trs=table.find("tr").find_next_siblings()
    for tr in trs:
        tds=tr.find_all("td")
        yield [
            tds[0].text.strip(),
            tds[1].text.strip(),
            tds[2].text.strip(),
            tds[3].text.strip(),
            tds[4].text.strip(),
        ]

#将爬取的数据写入文件
def write_to_file(content):
    with open("E:\python\data\sh_court_data.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

#获取一共需要爬取的页数
def get_page_nums():
    base_url='http://www.hshfy.sh.cn//shfy/gweb2017/ktpq_qxbg_list.jsp?'
    date_time=datetime.date.fromtimestamp(time.time())
    data={
        'pktrqks':date_time,
        'ktrqjs':date_time,
    }
    while True:
        html=get_html(base_url,data)
        soup=BeautifulSoup(html,'lxml')
        try:
            if soup.body.text.strip() == "系统繁忙":
                print("系统繁忙，登录太频繁，ip被封锁")
                time.sleep(ERROR_SLEEP_TIME)
                continue
            else:
                break
        except:
            print("系统繁忙，登录太频繁，ip被封锁")
            time.sleep(ERROR_SLEEP_TIME)
            continue
    res=soup.find("div",{'class':'meneame'})
    page_nums=res.find('strong').text
    page_nums=int(page_nums)
    if page_nums % 15 == 0:
        page_nums = page_nums // 15
    else:
        page_nums = page_nums // 15 + 1
    print("总页数:",page_nums)
    return page_nums

#主函数
def main():
    status_num=0
    page_nums=get_page_nums()
    base_url = 'http://www.hshfy.sh.cn//shfy/gweb2017/ktpq_qxbg_list.jsp?'
    while status_num==0:
        date_time = datetime.date.fromtimestamp(time.time())
        page_num = 1
        data={
            "pktrqks":date_time,
            "ktrqjs":date_time,
            "pagesnum":page_num
        }
        while page_num<=page_nums:
            while True:
                html = get_html(base_url,data)
                soup = BeautifulSoup(html,'lxml')
                try:
                    if soup.body.text.strip() == "系统繁忙":
                        print("系统繁忙，登录太频繁，ip被封锁")
                        time.sleep(ERROR_SLEEP_TIME)
                        continue
                    else:
                        break
                except:
                    print("系统繁忙，登录太频繁，ip被封锁")
                    time.sleep(ERROR_SLEEP_TIME)
                    continue
            res=parse(html)
            for row_data in res:
                write_to_file(row_data)
            print("爬取完第【%d】页，总共【%d】页"%(page_num,page_nums))
            page_num+=1
            data["pagesnum"]=page_num
            time.sleep(1)
        else:
            status_num=1
            print("爬取完毕")

if __name__ == '__main__':
    main()
