import json
import requests
import math
import time
import csv


#每次手动更改的有 job url_parse url_start


#job是 招聘网站搜索项 如：java c++ 算法工程师等
job = 'mysql'

#url_parse:链接里的Request URL
url_parse = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
#url_start:地址栏网址
url_start = 'https://www.lagou.com/jobs/list_MYSQL?labelWords=&fromSearch=true&suginput='
# 创建一个csv文件，并将表头信息写入文件中
with open(job+'.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['businessZones', 'companyFullName', 'companyLabelList', 'companyShortName', 'companySize', 'district',
                  'education', 'financeStage', 'firstType', 'industryField', 'industryLables', 'linestaion',
                  'positionAdvantage', 'positionName', 'publisherId', 'salary', 'secondType', 'stationname', 'workYear']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# 判断所查询的信息是否用30页可以展示完，大于30页的爬取30页内容
def get_page(url_start, url_parse, params):
    s = requests.Session()
    s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    response = s.post(url_parse, data=params, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
    time.sleep(5)
    response.encoding = response.apparent_encoding
    text = json.loads(response.text)
    #info = text["content"]["positionResult"]["result"]
    
    #html = requests.post(url, data=params, headers=headers)

   #json_data = json.loads(html.text)
    total_count = text['content']['positionResult']['totalCount'] # 获取信息公司信息总数
    page_number = math.ceil(total_count / 15) if math.ceil(total_count / 15) < 30 else 30
    get_info(url_start, url_parse, page_number)


def get_info(url_start, url_parse, page):
    for pn in range(1, page + 1):
        params = {
            'first': 'true' if pn == 1 else 'false',  # 第一页点击是true，其余页均为false
            'pn':str(pn), # 传入页面数的字符串类型
            'kd': job # 想要获取的职位
        }
        try:
            s = requests.Session()
            s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
            cookie = s.cookies  # 为此次获取的cookies
            response = s.post(url_parse, data=params, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
            time.sleep(5)
            response.encoding = response.apparent_encoding
            text = json.loads(response.text)
            results = text["content"]["positionResult"]["result"]
            #html = requests.post(url, data=params, headers=headers)
            #json_data = json.loads(html.text)
            #results = json_data['content']['positionResult']['result'] # 获取JSON数据内容
            for result in results: # 获取每条数据并以字典类型存储
                infos = {
                    'businessZones' : result['businessZones'],
                'companyFullName' : result['companyFullName'],
                'companyLabelList' : result['companyLabelList'],
                'companyShortName' : result['companyShortName'],
                'companySize' : result['companySize'],
                'district' : result['district'],
                'education' : result['education'],
                'financeStage' : result['financeStage'],
                'firstType' : result['firstType'],
                'industryField' : result['industryField'],
                'industryLables' : result['industryLables'],
                'linestaion' : result['linestaion'],
                'positionAdvantage' : result['positionAdvantage'],
                'positionName' : result['positionName'],
                'publisherId' : result['publisherId'],
                'salary' : result['salary'],
                'secondType' : result['secondType'],
                'stationname' : result['stationname'],
                'workYear' : result['workYear']
                }
                print('-------------')
                print(infos)
                write_to_file(infos) # 调用写入文件函数
            time.sleep(2)
        except requests.RequestException :
            pass


# 将数据追加写入之前创建的csv文件中
def write_to_file(content):
    with open(job+'.csv', 'a', newline='',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(content)
        csvfile.close()

# 传入url ，引用get_page函数
if __name__ == '__main__':
    params = {
        'first': 'true',
        'pn': '1',
        'kd': job
    }
    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E5%8C%97%E4%BA%AC',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}
    get_page(url_start, url_parse, params)
