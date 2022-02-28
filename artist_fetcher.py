from auth import ChartMetric
from loader import ArtistDataHandler
import json
import os


def download_sp_month_listen(m):
    t = ArtistDataHandler('spotify_popularity')
    limit = 50
    for i in t.data :
        for offset in range(0, 100) :
            if not "sp_month_listen_"+str(i['id'])+"_"+str(offset*limit)+'.json' in os.listdir('metrics') :
                res = m.request("https://api.chartmetric.com/api/artist/"+str(i['id'])+"/where-people-listen?limit="+str(limit)+"&offset="+str(offset*limit)+"&since=2018-01-01")
                with open("metrics/sp_month_listen_"+str(i['id'])+"_"+str(offset*limit)+'.json', 'w') as outfile:
                    json.dump(res.text, outfile)
                data = json.loads(res.text)
                print(i['id'], 'sp_month_listen', offset*limit)
                if (len(data['obj']['cities'].items())+len(data['obj']['countries'].items())) == 0 :
                    break

def download_albums_data(m) :
    t = ArtistDataHandler('spotify_popularity')
    for i in t.data :
        # print(i['releases'])
        for album in i['releases'] :
            if not "album_"+str(i["id"])+"_"+str(album['cm_album'])+".json" in os.listdir('metrics') :
                res = m.request("https://api.chartmetric.com/api/album/"+str(album['cm_album']))
                with open("metrics/album_"+str(i['id'])+"_"+str(album['cm_album'])+".json", 'w') as outfile:
                    json.dump(res.text, outfile)
                print(i['id'], 'album', album['cm_album'])

def download_user_data(m) :
    limit = 100
    for sortBy in ['spotify_popularity', 'spotify_followers', 'spotify_monthly_listeners', 'twitter_followers', 'instagram_followers', 'wiki_views', 'soundcloud_followers', 'youtube_channel_views'] :
        for offset in range(0, 10000) :
            a = m.request('https://api.chartmetric.com/api/artist/anr/by/social-index?limit='+str(limit)+'&offset='+str(offset*limit)+'&sortBy='+sortBy)
            if '504 Gateway Time-out' in a.text :     
                print(sortBy, offset*limit, "fail")
                break
            else :       
                with open('data/'+sortBy+'_'+str(offset)+'.json', 'w') as outfile:
                    json.dump(a.text, outfile)
                    print(sortBy, offset*limit, "success")

def download_youtube_data(m) :
    # Youtube
    t = ArtistDataHandler('spotify_popularity')
    youtubeList = ['youtube']
    for type in youtubeList :
        for i in t.data :
            print(i['id'], type)
            res = m.request("https://api.chartmetric.com/api/artist/"+str(i['id'])+"/market-coverage-views/youtube")
            with open('metrics/'+type+"_"+i['id']+'.json', 'w') as outfile:
                json.dump(res.text, outfile)
            data = json.loads(res.text)
            print(data)
            i[type] = data['obj']  

# import json
# res_list = []
# for i in range(0, 100) :
#   a = m.request('https://api.chartmetric.com/api/artist/4234/where-people-listen?since=2021-06-01&until=2021-10-31&limit=50&offset='+str(i*50))
#   if (a.text == '{"obj":{"cities":{},"countries":{}}}') :
#     break
#   data = json.loads(a.text)
#   res_list.append(data['obj'])

###########
timestps = {}
for res in res_list :
  for city in res['cities'].keys() :
      for elem in res['cities'][city] :
        if not elem['timestp'] in list(timestps.keys()) :
          timestps[elem['timestp']] = 0
        timestps[elem['timestp']] += elem['listeners']


if __name__ == "__main__":
    m = ChartMetric()
    # download_albums_data(m)
    download_sp_month_listen(m)