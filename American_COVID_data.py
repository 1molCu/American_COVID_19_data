# —*— coding: utf-8 —*—
import requests
import json
import time
import pandas as pd


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'referer': 'https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0'
}

r = requests.get(url % time.time(), headers = headers)

data = json.loads(r.text)

data = json.loads(data['data'])

lastUpdateTime = data['globalStatis']['lastUpdateTime']

print('数据更新时间' + str(lastUpdateTime))

names = ['地区','确诊人数','死亡人数','治愈人数']

df = pd.DataFrame(columns=names)

country = data['foreignList']

for i in range(0,len(country)):
    if country[i]['name'] == '美国':
        item_ps = country[i]['children']

        for item_p in item_ps:
            province = item_p['name']
            confirm = item_p['confirm']
            death = item_p['dead']
            heal = item_p['heal']

            data_dict = {
                '地区': province,
                '确诊人数' : confirm,
                '死亡人数' : death,
                '治愈人数' : heal
            }
            
            df.loc[len(df)] = data_dict

df.index += 1
df.to_csv(r'./test{}.csv'.format(str(lastUpdateTime).split()[0]),encoding='utf_8_sig',header = 'true')

print('成功')


