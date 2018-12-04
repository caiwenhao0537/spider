#导入BeautifulSoup包用于解析网页
from bs4 import BeautifulSoup
#导入requests包用于获取网页
import requests
#导入pandas包，用于将字典数据转换为DataFrame，然后写入csv文件
import pandas as pd

#获取豆瓣首页网页
html=requests.get('https://book.douban.com/')

#将获取的豆瓣首页放入BeautifulSoup中进行解析，这里使用"lxml"库对网页进行解析
soup=BeautifulSoup(html.text,'lxml')
#获取每本书的div
book_divs=soup.find_all('div',{'class':'info'})

def get_information(book_div):
    book_dict={}
    try:
        book_dict['book_link']=book_div.find('div',{'class':'title'}).find('a').get('href').strip()
    except:
        book_dict['book_link']=u''
    try:
        book_dict['book_name']=book_div.find('div',{'class':'title'}).find('a').get('title').strip()
    except:
        book_dict['book_name']=u''
    try:
        book_dict['book_author']=book_div.find('div',{'class':'author'}).get_text().strip()
    except:
        book_dict['book_author']=u''
    try:
        book_dict['book_year']=book_div.find('span',{'class':'year'}).get_text().strip()
    except:
        book_dict['book_year']=u''
    try:
        book_dict['book_publisher']=book_div.find('span',{'class':'publisher'}).get_text().strip()
    except:
        book_dict['book_publisher']=u''
    try:
        book_dict['book_abstract']=book_div.find('p',{'class':'abstract'}).get_text().strip().replace('\n','')
    except:
        book_dict['book_abstract']=u''
    return book_dict


if __name__ == '__main__':
    i=0
    for book_div in book_divs:
        data = pd.DataFrame(get_information(book_div), index=[i])
        i+=1
        print('正在处理第%d文章'%(i))
        data.to_csv('E:\python\data\douban4.csv',encoding='utf-8',mode='a',header=False)