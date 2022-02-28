import json
import os
import matplotlib.pyplot as plt

class ArtistDataHandler :
    def __init__ (self, material="all") :
        self.data = None   
        self.load_data(material=material)     
    def load_data(self, material="all") :
        self.data = []
        file_list = os.listdir('data')
        if material != "all" :
            file_list = list(filter(lambda x : material in x,  file_list))            
        for file in file_list :
            f = open('data/'+file)
            a = json.loads(json.load(f))
            self.data += a['obj']
    def album_loader(self) :
        self.album_dict = {}
        file_list = list(filter(lambda x : "album" in x, os.listdir('metrics')))
        for file in file_list :
            f = open('metrics/'+file)
            try:
                a = json.loads(json.load(f))
                artist_id = int(file.split("_")[1])
                album_id = int(file.split("_")[2].split('.')[0])
                if not artist_id in list(self.album_dict.keys()) :
                    self.album_dict[artist_id] = []
                self.album_dict[artist_id].append(a['obj'])
            except :
                pass
        self.album_timeseries_dict={}
        for artist_id in self.album_dict.keys() :
            self.album_timeseries_dict[artist_id] = {}
            for album_elem in self.album_dict[artist_id] :
                if album_elem['cm_statistics']['sp_playlist_total_reach'] :
                    timestp = album_elem['release_date'].split("T")[0]
                    if not timestp in self.album_timeseries_dict[artist_id].keys() :
                        self.album_timeseries_dict[artist_id][timestp] = 0                    
                    self.album_timeseries_dict[artist_id][timestp] += album_elem['cm_statistics']['sp_playlist_total_reach']
    def streaming_aggr_loader(self) :
        self.strm_aggr_dict = {}
        file_list = list(filter(lambda x  : "sp_month_listen" in x, os.listdir('metrics')))
        for file in file_list :
            f = open('metrics/'+file)
            try :
                a = json.loads(json.load(f))
                id = int(file.split("_")[3])
                if not id in list(self.strm_aggr_dict.keys()) :
                    self.strm_aggr_dict[id] = []
                self.strm_aggr_dict[id].append(a['obj'])
            except :
                pass 
        self.streaming_timeseries_dict={}
        for id in self.strm_aggr_dict.keys() :
            self.streaming_timeseries_dict[id] = {}
            for elem in self.strm_aggr_dict[id] :
                for city in elem['cities'].keys() :
                    for timestemp_elem in elem['cities'][city] :
                        timestp = timestemp_elem['timestp'].split('T')[0]
                        if not timestp in self.streaming_timeseries_dict[id].keys() :
                            self.streaming_timeseries_dict[id][timestp] = 0
                        self.streaming_timeseries_dict[id][timestp]+=timestemp_elem['listeners']
    def merging_data(self):
        self.album_loader()
        self.streaming_aggr_loader()        
        merged_artists = list(set(self.album_timeseries_dict.keys()) & set(self.streaming_timeseries_dict.keys()))
        self.merged_dict = {}
        for merged_artist in merged_artists :
            timestamp_album = list(self.album_timeseries_dict[merged_artist].keys())
            timestamp_stream = list(self.streaming_timeseries_dict[merged_artist].keys())
            total_timestamp_list = list(set(timestamp_album) | set(timestamp_stream))
            timestamp_album.sort()
            timestamp_stream.sort()
            total_timestamp_list.sort()
            self.merged_dict[merged_artist]={}
            point = [0,0]
            for timestamp in total_timestamp_list :
                if timestamp in timestamp_album : 
                    point[0] = self.album_timeseries_dict[merged_artist][timestamp]
                    timestamp_album.remove(timestamp)
                if timestamp in timestamp_stream :  
                    point[1] = self.streaming_timeseries_dict[merged_artist][timestamp]
                    timestamp_stream.remove(timestamp)
                self.merged_dict[merged_artist][timestamp] = point
        with open("merged_dict.json", 'w') as outfile:
            json.dump(self.merged_dict, outfile)

        self.final={}
        for id, value in list(self.merged_dict.items()) :
            album_list = []
            stream_list = []
            for _, i in list(value.items()) :
                album_list.append(i[0])
                stream_list.append(i[1])
            self.final[str(id)] = {"album_list":album_list, "stream_list":stream_list} 
        with open("final.json", 'w') as outfile:
            json.dump(self.final, outfile)


    def plot(self) :
        for id, lists in list(self.final.items()):
            plt.plot(lists["album_list"], lists["stream_list"])
            plt.xlabel("Album's reaching out")
            plt.yladel("Monthly Streaming Listener")
        plt.show()
        
        
for id, lists in list(final.items()):
    plt.scatter(lists["album_list"], lists["stream_list"], linewidth=2, markersize=12)
plt.title("Monthly Streaming vs Album Reaching Out")
plt.xlabel("Album's reaching out")
plt.ylabel("Monthly Streaming Listener")
plt.show()
            
import math
for id, lists in list(final.items()):
    x = list(map(lambda x : math.log(x) if x != 0 else 0, lists["album_list"]))
    y = list(map(lambda x : math.log(x) if x != 0 else 0, lists["stream_list"]))
    plt.scatter(x, y)
plt.title("Logged Monthly Streaming vs Logged Album Reaching Out")
plt.xlabel("Logged Album's reaching out")
plt.ylabel("Logged Monthly Streaming Listener")
plt.show()
            
        


    # def get_
    #     https://api.chartmetric.com/api/artist/4904/spotify_top_daily/charts?since=2020-03-01&until=2020-03-04

# t = ArtistDataHandler()
# t = ArtistDataHandler('spotify_popularity')
# t.streaming_aggr_loader()
# dict_time = t.streaming_timeseries_dict

# t = ArtistDataHandler('spotify_popularity')
# t.album_loader()
# dict_album = t.album_dict
# dict_artist_album = t.artist_album_dict



        # self.artist_album_dict = {}
        # for artist_elem in self.data :
        #     self.artist_album_dict[int(artist_elem['id'])]=artist_elem['releases']

t = ArtistDataHandler('spotify_popularity')
t.merging_data()
t.plot()