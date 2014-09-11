#!/usr/bin/env python
# encoding: utf-8
#Takes a list of bands as seeds, downloads json data, finds related artists and continues until stopped
#loads existing list of bands to prevent duplicates. so can be started and stopped

import spotipy
import json

uniq_bands = [] #loads entire bandlist.txt to check for duplicates

#gets similar artists, checks for duplicates, appends to bandlist.txt
def show_similar_art(id):
    sp = spotipy.Spotify()
    art = []
    results = sp.artist_related_artists(id)
    art.extend(results['artists'])
    seen = set()
    art.sort(key=lambda art:art['name'].lower())
    for art in art:
        if art['name'] not in uniq_bands:
            uniq_bands.append(art['name'])
            name = art['name']
            out.write(name.encode('utf8') + "\n")

#Get the artists JSON info and pass the ID to similar artists
def get_artist_info(name):

    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        with open(artist['name'] + '.txt', 'w') as outfile:
            json.dump(results, outfile)
        show_similar_art(artist['id'])
        print "Completed " + artist['name']
    pass


if __name__ == '__main__':
    while(True): #Run forever
        f = open('bandlist.txt', 'r').readlines()
        out = open('bandlist.txt', 'a')
        lines_set = set(f)
        for r in lines_set:
            uniq_bands.append(r)
            get_artist_info(r)


