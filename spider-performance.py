# #列表循环的方式
# import requests
# from datetime import datetime
# start_time=datetime.now()
# url_list={
#     'http://www.baidu.com',
#     'http://www.pythonsite.com',
#     'http://www.cnblogs.com/'
# }
# for url in url_list:
#     reults = requests.get(url)
#     print(reults.text)
#
# end_time=datetime.now()
# use_time=end_time - start_time
# print("程序运行所用时间为%s"%(use_time))

# #通过线程池的方式
# import requests
# from concurrent.futures import ThreadPoolExecutor
# from datetime import datetime
# start_time=datetime.now()
#
# def fetch_request(url):
#     result=requests.get(url)
#     print(result.text)
# url_list={
#     'http://www.baidu.com',
#     'http://www.pythonsite.com',
#     'http://www.cnblogs.com/'
# }
# pool = ThreadPoolExecutor(10)
# for url in url_list:
#     #去线程池中获取一个线程，线程去执行fetch_request方法
#     pool.submit(fetch_request,url)
# pool.shutdown(True)
#
# end_time=datetime.now()
# use_time=end_time-start_time
# print("程序运行所用时间为%s"%(use_time))

#通过线程池加回调函数
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

start_time=datetime.now()

def fetch_async(url):
    response=requests.get(url)
    return response
def callback(future):
    print(future.result().text)
url_list={
    'http://www.baidu.com',
    'http://www.pythonsite.com',
    'http://www.cnblogs.com/'
}
pool =ThreadPoolExecutor(5)
for url in url_list:
    v=pool.submit(fetch_async,url)
    v.add_done_callback(callback)

pool.shutdown()
end_time=datetime.now()
use_time=end_time-start_time
print("程序运行所用时间为%s"%(use_time))