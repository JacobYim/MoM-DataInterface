import json
import re
import requests
class ChartMetric :
    def __init__(self) :
        f = open("apis.json")
        contents = json.load(f)
        self.username = contents["ChartMetric"]['Username']
        self.password = contents["ChartMetric"]['Password']
        self.refreshtoken = contents["ChartMetric"]['RefreshToken']
        self.refresh()
    def refresh(self) :
        payload = {"refreshtoken" : self.refreshtoken}
        header = {"Content-Type": "application/json"}
        res = requests.post("https://api.chartmetric.com/api/token", json=payload, headers=header)
        self.accesstoken = json.loads(res.text)['token']
        self.header = {"Authorization": "Bearer "+self.accesstoken}
    def request(self, url, method='get', data=None) :
        if method == "post" :
            res = requests.post(url, headers=self.header, json=data)
        elif method == "get" :
            res = requests.get(url, headers=self.header)
        else :
            print('method is not defined')
            return None
        if res.status_code != 200 :
            self.refresh()
            if method == "post" :
                res = requests.post(url, headers=self.header, json=data)
            elif method == "get" :
                res = requests.get(url, headers=self.header)
            else :
                print('method is not defined')     
                return None
        return res

class Musiio :
    def __init__(self) :
        f = open("apis.json")
        contents = json.load(f)
        self.key = contents["Musillo"]['key']
    def request(self, url, method='get', data=None) :
        header = {"Authorization": "Basic "+self.key, "Content-Type": "application/json"}
        # "https://api-us.musiio.com/v2/widget"
        # res = requests.post("https://api.chartmetric.com/api/token", headers=header)
        # res = requests.post("https://api-us.musiio.com/v2/widget/search/perform", headers=header)
        
        if method == "post" :
            res = requests.post(url, headers=self.header)
        elif method == "get" :
            res = requests.get(url, headers=self.header)
        else :
            res = None
        return res


# m = ChartMetric()
# a = m.request('https://api.chartmetric.com/api/charts/airplay/artists?since=2020-09-09&duration=daily')
# a = m.request('https://api.chartmetric.com/api/charts/amazon/tracks?date=2019-5-26&type=popular_track&genre=All+Genres')

