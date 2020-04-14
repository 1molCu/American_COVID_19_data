# —*— coding: utf-8 —*—
import io
import os
import json
import time

import requests
import pandas as pd

class DoSomething:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.is_cache = False

    def get_data(self):
        try:
            r = requests.get(self.url % time.time(), headers = self.headers)
        except requests.exceptions.ConnectionError as e:
            cache_path = 'data_cache.txt'
            if not (os.path.exists(cache_path) and os.path.isfile(cache_path)):
                open('data_cache.txt','w').close()
            with open('data_cache.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                if data == '': raise Exception('Fatal')
                self.is_cache = True
        else:
            data = json.loads(r.text)['data']
            with open('data_cache.txt', 'w', encoding='utf-8') as f:
                f.write(data)

        return json.loads(data)

    def handle_data(self, data):
        lastUpdateTime = data['globalStatis']['lastUpdateTime']
        print(f"数据更新时间: {lastUpdateTime} " + ('(使用了缓存！)' if self.is_cache else ''))

        names = ['地区','确诊人数','死亡人数','治愈人数']

        df = pd.DataFrame(columns=names)

        country = data['foreignList']

        for i in range(len(country)):
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
        df.to_csv(f'./test{(lastUpdateTime).split()[0]}.csv', encoding = 'utf_8_sig', header = 'true')

        print(df)

if __name__ == "__main__":
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'referer': 'https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0'
    }
    ds = DoSomething(url, headers)
    data = ds.get_data()
    ds.handle_data(data)
