from pytube import YouTube, Playlist
import random

def get_playlist(pl_link):
    playlist = Playlist(pl_link)
    all_vids = []

    for video in playlist:
        curr_vid_details = []
        curr_vid = YouTube(video)
        curr_vid_details.append(video)
        curr_vid_details.append(curr_vid.title)
        curr_vid_details.append(curr_vid.length/60)
        curr_vid_details.append(curr_vid.views)
        curr_vid_details.append(curr_vid.author)
        all_vids.append(curr_vid_details)

    print(all_vids[2])
    return all_vids

def rand_vid(*playlist):
    random_int = random.randint(1, playlist.len())
    print(playlist[random_int])

all_playlists = get_playlist("https://www.youtube.com/playlist?list=PLEhSYc84M4xCljuyXNxEgVHLgdCzAm0vu")
rand_vid(all_playlists)
