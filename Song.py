class Song:
    found = False

    def __init__(self,searchTerm, header):
        self.searchTerm = searchTerm.replace(" ", "%20")
        self.header = header
        self.request = self.getSpotifyItem(self.searchTerm)
        self.URI = self.uriFromItem(self.request)
        self.ID = self.URI[14:]
        self.audioFeatures = self.getTrackAudioFeature(self.ID)


    def getSpotifyItem(self,searchTerm):
        import requests
        header = self.header
        baseURL = 'https://api.spotify.com/v1/'
        reqJSON = requests.get(baseURL + "search?q=" + searchTerm + "&type=track" + "&limit=1",headers=header)
        req = reqJSON.json()
        if req["tracks"]["items"] == []:
            print("Song not found!")
            return {"Not Found" : f"'{searchTerm}'"}
        print("we found it")
        self.found = True
        return req
    
    def getTrackAudioFeature(self, ID):
        import requests
        header = self.header
        baseURL = 'https://api.spotify.com/v1/'
        reqJSON = requests.get(baseURL + "audio-features/" + ID ,headers=header)
        req = reqJSON.json()
        return req
    
    def getAudioFeature(self, feature):
        value = self.audioFeatures.get(feature)
        if value == "":
            print("The feature: " + feature + " does not exist")
            return
        return value
                              

    def uriFromItem(self,dic):
        if dic.get("Not Found"):
            URI = "Not Found"
            return URI

        URI = dic["tracks"]["items"][0]["uri"]
        return URI

    def add_queue(self):
        headers = self.header
        import requests
        if self.URI == "Not Found":
            print("No URI to queue")
            return
        link='https://api.spotify.com/v1/me/player/queue?uri={}'.format(self.URI)
        p = requests.post(link,headers=headers)
        print(p)
