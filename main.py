import json
import requests
from private import spotify_user_id
from refresh import Refresh
import random
"""
Program that makes a spotify playlist based on a search term.
Will search for 20 playlists that have that search term, and add a random song from each playlist.
Some code was used from EuanMorgan's SpotifyDiscoverWeeklyRescuer tutorial.

Author: Angela Eang
Date: 11/04/21
"""

class PlaylistTermSearch:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.tracks = ""
        self.new_playlist_id = ""
        self.search_term = ""

    def search_keyword(self):
        print("Let's make a playlist based off a term!")
        self.search_term = input("Enter a search term: ")
        print("")
        search_query = self.search_term.replace(" ", "%20")
    
        query = 'https://api.spotify.com/v1/search?q={}&type=playlist'.format(search_query)

        response = requests.get(query, headers={
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()
        print(response)

        #finding number of playlists found to do error handling!
        num_of_playlists = len(response_json["playlists"]["items"])
        if num_of_playlists == 0:
            print("Sorry, this term was hard to search for!")
            exit()

        #go through 20 playlists and find/add a random song from each
        print("Finding songs in the playlist...")
        print("")
        for i in range(num_of_playlists):
            playlist_id = response_json["playlists"]["items"][i]["id"]
            self.find_songs(playlist_id)

        #fix formatting before we send tracks to get added in playlist
        self.tracks = self.tracks[:-1]

        #create playlist and add all of our tracks to the playlist
        self.add_to_playlist()



    def find_songs(self, id):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(id)

        response = requests.get(query, headers={
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()
        print(response)

        #items are the songs in the playlist
        playlist_len = len(response_json["items"])
        num = random.randint(0, playlist_len-1)

        #adding one random song to our list of tracks
        self.tracks += (response_json["items"][num]["track"]["uri"] + ",")
    
    def create_playlist(self):
        print("trying to create playlist...")
        print("")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        request_body = json.dumps({
            "name": self.search_term,
            "description": "A cool new playlist!",
            "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self):
        print("adding songs...")
        print("")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={
            "Content-Type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        print(response.json)
        print("DONE!")

    def call_refresh(self):
        print("Refreshing Token...")
        print("")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.search_keyword()
                                                                


a = PlaylistTermSearch()
a.call_refresh()