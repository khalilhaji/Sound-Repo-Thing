import requests
import json
import urllib
from bs4 import BeautifulSoup, NavigableString
import complex_json_encoder as cje

'''
def getSeedId(query):
    encodedQueryString = urllib.parse.urlencode({'query' : query, 'queryType': 'track'})
    url = "https://tunebat.com/Advanced/SeedQuery?" + encodedQueryString
    r = requests.get(url).json()['TrackItems'][0]['Id']
    #print(r)
    return r

def getOrderedBPMMatches(bpm, seedId=""):
    minBPMStr = str(bpm - 5)
    maxBPMStr = str(bpm + 5)
    seedIdStr = "[]" if seedId == "" else "[%22" + seedID + "%22]"
    url = "https://tunebat.com/Advanced/AdvancedQuery?inputs={%22Target%22:{%22DurationMs%22:null,%22Energy%22:null,%22Danceability%22:null,%22Valence%22:null,%22Loudness%22:null,%22Acousticness%22:null,%22Instrumentalness%22:null,%22Liveness%22:null,%22Speechiness%22:null},%22Min%22:{%22Tempo%22:" + minBPMStr + ",%22Popularity%22:30},%22Max%22:{%22Tempo%22:" + maxBPMStr + ",%22Popularity%22:100},%22TrackSeeds%22:" + seedIdStr + ",%22ArtistSeeds%22:[]}"
    r = requests.get(url).json()['TrackItems']
    #print(json.dumps(r[0:2]))
    r.sort(key=lambda item : (abs(bpm - int(item['BPM'])), 100 - int(item['Popularity'])))
    #print(json.dumps(r[0:2]))
    return r
'''

class Song(cje.ComplexJSONSerializable):
    def __init__(self, title, artist, bpm, relPopularity):
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.relPopularity = relPopularity


def getSongsByBPM(targetBPM, pageNum=1):
    url = "https://jog.fm/popular-workout-songs?bpm=" + str(targetBPM) + "&page=" + str(pageNum)

    page = requests.get(url).content

    soup = BeautifulSoup(page, 'lxml')

    entries =  soup.find_all(class_="song list-item")

    songs = []

    for i, entry in enumerate(entries):
        titleParent = entry.findChild("div", class_="title")
        artistParent = entry.findChild("div", class_="top")
        bpmParent = entry.findChild("div", class_="side-box fixed")
        bpmParent = bpmParent.findChild("div", class_="middle") if bpmParent is not None else bpmParent

        if (titleParent is not None and artistParent is not None and bpmParent is not None):
            title = titleParent.a.string
            artist = artistParent.a.string
            bpm = bpmParent.a.string
            
            songs += [Song(title, artist, int(bpm), int(i))]
        
        #print(title)

    songs.sort(key=lambda song : (abs(targetBPM - song.bpm), song.relPopularity))

    return json.loads(json.dumps(songs, cls=cje.ComplexEncoder))

def findMatches(seed, bpm):
    if seed is not None:
        print(seed)
        seedId = getSeedId(seed)
        matches = getOrderedBPMMatches(bpm, seedId)[0:5]
    else:
        matches = getOrderedBPMMatches(bpm)[0:5]

    return list(map(lambda match: match['SearchName'], matches))

if __name__ == '__main__':
    print(findMatches("avicii the nights", 126))
    print(findMatches(None, 126))
