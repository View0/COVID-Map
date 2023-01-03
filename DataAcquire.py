import requests
url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=325331491756" #存放网址
headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"}
req = requests.get(url, headers = headers)
req.status_code #如果返回403，需要对爬虫进行伪装,200表示成功import

import pandas as pd
data = req.json()

#中国各省实时数据提取
head = pd.DataFrame(data['data']['areaTree'][2]['children'])[["id", "lastUpdateTime", "name"]] #后半部分[["", "", ""]]是需要数据的索引
today = pd.DataFrame([i['today'] for i in data['data']['areaTree'][2]['children']])
today.columns = ['today_'+ i for i in today.columns] #修改列名
total = pd.DataFrame([i['total'] for i in data['data']['areaTree'][2]['children']])
total.columns = ['total_'+ i for i in total.columns] #修改列名
table=pd.concat([head, today, total],axis = 1) #将三列数据合并
table.to_excel('china_prov_data.xlsx', index = None) #存储数据pip

#世界各国数据的提取
head = pd.DataFrame(data['data']['areaTree'])[["id", "lastUpdateTime", "name"]]
today = pd.DataFrame([i['today'] for i in data ['data']['areaTree']])
today.columns = ['today_'+ i for i in today.columns] #修改列名
total = pd.DataFrame([i['total'] for i in data ['data']['areaTree']])
total.columns = ['total_'+ i for i in total.columns] #修改列名
table = pd.concat([head, today, total],axis = 1) #将三列数据合并
table.to_excel('world_total_data.xlsx', index = None) #存储数据

#中国各省的历史数据
china_data = pd.read_excel('./china_prov_data.xlsx') #先读取之前保存的数据
id_name = china_data[['id', 'name']].values.tolist()
urls = [f"https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode={i[0]}&" for i in id_name] #不大清楚怎么来的
for z, i in enumerate(urls):
    req = requests.get(i, headers = headers)
    data = req.json()
    date = pd.DataFrame(data['data']['list'])['date']
    today = pd.DataFrame([i['today'] for i in data['data']['list']])
    today.columns = ['today_' + i for i in today.columns] #修改列
    total = pd.DataFrame([i['total'] for i in data['data']['list']])
    total.columns = ['total_' + i for i in total.columns] #修改列名
    table = pd.concat([date, today, total], axis = 1) #将三列数据合并
    table.insert(0, 'name', id_name[z][1])
    #把其他省份信息拼到第一个省份下面
    if z == 0:
        tables = table
    else:
        tables = pd.concat([tables, table], axis = 0)
    print(f"{id_name[z][1]}省份数据抓取完成，共获取{table.shape[0]}条数据")
print(f'全国各省数据抓取完成，共获取到{tables.shape[0]}条数据')
tables.to_excel(f'china_all_prov_history_data.xlsx', index = None)

#世界各国的历史数据
import time #导入时间模块，防止爬取过快
world_data = pd.read_excel('./world_total_data.xlsx')
id_name = world_data[['id', 'name']].values.tolist()
urls = [f"https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode={i[0]}&" for i in id_name]
for z, i in enumerate(urls):
    req = requests.get(i, headers = headers)
    data = req.json()
    date = pd.DataFrame(data['data']['list'])['date']
    today = pd.DataFrame([i['today'] for i in data['data']['list']])
    today.columns = ['today_' + i for i in today.columns] #修改列
    total = pd.DataFrame([i['total'] for i in data['data']['list']])
    total.columns = ['total_' + i for i in total.columns] #修改列
    table = pd.concat([date, today, total], axis = 1) #将三列合并，axis = 1代表按列合并
    table.insert(0, 'name', id_name[z][1])
    #拼接各国的信息
    if z == 0:
        tables = table
    else:
        tables = pd.concat([tables, table], axis = 0) #合并，axis = 0代表按行合并
    time.sleep(1)
    print(f"{id_name[z][1]}国家数据抓取完成，共获取{table.shape[0]}条数据")
print(f'世界各国数据抓取完成，共获取到{tables.shape[0]}条数据')
tables.to_excel(f'world_all_country_history_data.xlsx', index = None) #注意，这里默认路径是你python运行的文件夹
