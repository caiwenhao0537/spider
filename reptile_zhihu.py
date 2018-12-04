#-*- coding:utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

class zhiHu(object):
    baseurl = 'http://www.zhihu.com'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    }

    def getData(self,url):
        data = requests.get(url= url,headers= self.headers).content.decode('utf-8')
        soup = BeautifulSoup(data,'lxml')
        infos = soup.find_all('div',{'class': 'List-item TopicFeedItem'})
        items={}
        self.store_header()
        i=0
        for info in infos:
            #问题名称
            try:
                question_name = info.find('h2',{'class':'ContentItem-title'}).find('meta',{'itemprop':'name'}).get('content').strip()
                print(question_name)
                items['question_name']=question_name
            except:
                question_name = info.find('h2',{'class':'ContentItem-title'}).find('a').get_text().strip()
                print(question_name)
                items['question_name']=question_name
            #问题url
            try:
                question_url= info.find('h2',{'class':'ContentItem-title'}).find('meta',{'itemprop':'url'}).get('content').strip()
                items['question_url']=question_url
                print(question_url)
            except:
                question_url=info.find('h2',{'class':'ContentItem-title'}).find('a').get('href').strip()
                items['question_url']=question_url
                print(question_url)
            #用户名称
            try:
                user_name=info.find('div',{'class':'ContentItem-meta'}).find('meta',{'itemprop':'name'}).get('content').strip()
                items['user_name']=user_name
                print(user_name)
            except:
                user_name=u'匿名用户'
                items['user_name']=user_name
            #用户url
            try:
                user_url=info.find('div',{'class':'ContentItem-meta'}).find('meta',{'itemprop':'url'}).get('content').strip()
                items['user_url']=user_url
                print(user_url)
            except:
                items['user_url']=u''
            #回答获赞数量
            try:
                answer_upvoteCount=info.find('meta',{'itemprop':'upvoteCount'}).get('content').strip()
                items['answer_upvoteCount']=answer_upvoteCount
                print(answer_upvoteCount)
            except:
                answer_upvoteCount=info.find('button',{'class':'Button VoteButton VoteButton--up'}).get_text().strip().replace('赞同<!-- -->','')
                items['answer_upvoteCount']=answer_upvoteCount
                print(answer_upvoteCount)
            #详细回答url
            try:
                answer_url=self.baseurl + info.find('h2',{'class':'ContentItem-title'}).find('a').get('href')
                items['answer_url']=answer_url
                print(answer_url)
            except:
                items['answer_url']=u''
            self.store(items)
            i+=1
            print('正在处理第%d个答案' %(i))
    def store_header(self,):
        with open('E:\python\data\zhihu.csv','a',encoding='utf-8',newline='') as f:
            field_names=['question_name','question_url','user_name','user_url','answer_upvoteCount','answer_url']
            writer= csv.DictWriter(f,fieldnames=field_names)
            writer.writeheader()

    def store(self,item={}):
        with open('E:\python\data\zhihu.csv','a',encoding='utf-8',newline='') as f:
            field_names=['question_name','question_url','user_name','user_url','answer_upvoteCount','answer_url']
            writer= csv.DictWriter(f,fieldnames=field_names)
            writer.writerow(item)

if __name__ == '__main__':
    url = "https://www.zhihu.com/topic/19552832/top-answers"
    zhihu = zhiHu()
    zhihu.getData(url)







