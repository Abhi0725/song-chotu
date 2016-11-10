#-------------------------------------------------------------------------------
# Name:        Song Chotu
# Purpose:     To download songs from internet
#
# Author:      Abhishek Chakravarty (abhi072592@gmail.com)
#
# Created:     03-01-2015
# Copyright:   None
# Licence:     Use Any
#-------------------------------------------------------------------------------

import sys
import requests
from bs4 import BeautifulSoup
import os

def get_movie(url):
    movie_search_page = requests.get(url, allow_redirects= True)
    if movie_search_page.status_code == 200:
        movie_search_soup = BeautifulSoup(movie_search_page.text)
        movie_p_tags = movie_search_soup.findAll(class_="dj")
        for num, movie_names in enumerate(movie_p_tags):
            if movie_names.a.text != 'Home':
                print str(num+1)+'. '+movie_names.a.text
        movie_index = int(raw_input("Enter movie number: "))
        return movie_p_tags[movie_index-1].a['href']
    else:
        return 'failed to connect'


def get_song(movie_link):
    song_search_page = requests.get(movie_link)
    song_search_soup = BeautifulSoup(song_search_page.text)
    song_p_tags = song_search_soup.findAll(class_="dj")
    for num, song_names in enumerate(song_p_tags):
        if song_names.a.text == '48Kbps':
            break
        else:
            print str(num+1)+'. '+song_names.a.text
    song_index = int(raw_input("Enter song number: "))
    return song_p_tags[song_index-1].a.text, song_p_tags[song_index-1].a['href']



def main():
    print '='*30
    print 'Song Downloader'
    print '='*30
    base_url = 'http://djraag.com'
    movie = raw_input("Please enter the movie name: ")
    if not movie:
        print 'No movie name. exiting...'
        sys.exit(1)
    else:
        url = base_url+'/bollywood/searchbycat.html?search='+movie+'&type=album&cat_id=5&submit=Submit'
        movie_link = get_movie(url)
        if movie_link == 'failed to connect':
            print 'failed to connect'
            sys.exit(1)
        else:
            movie_link = base_url+movie_link
            song_name, song_url = get_song(movie_link)
            song_url = base_url+song_url
            print 'please wait...'
            page = requests.get(song_url)
            soup = BeautifulSoup(page.text)
            links = soup.findAll('a',href=True)
            song_urls = []
            kbps_number = 0
            for link in links:
                if "Kbps_-_www.DjRaag.Net.mp3" in link['href']:
                    kbps_number += 1
                    print str(kbps_number)+'. '+link.contents[0]
                    song_urls.append(link['href'])

            kbps_choice = int(raw_input("Enter kbps choice number (e.g 1): "))

            if not kbps_choice:
                kbps_choice = 1

            print "===="
            song_url = song_urls[kbps_choice-1]
            print "Downloading..."

            data = requests.get(song_url).content

            os.chdir('songs')
            filename = song_name+".mp3"

            with open(filename, 'wb') as f:
                    f.write(data)
            print 'download complete'
            print 'saved in '+os.getcwd()+' as '+filename


if __name__ == '__main__':
    main()
