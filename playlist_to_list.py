from pytube import YouTube, Playlist
import pytube.exceptions
import random

def get_playlist(playlist: Playlist):
    '''Stores all chosen video data from a playlist into a list.'''
    all_vids = []
    print(f'Downloading all video data from playlist \"{playlist.title}\". Please wait a few moments.')
    for video in playlist:
        try:
            curr_vid = YouTube(video)
        except pytube.exceptions.VideoUnavailable:
            print("Skipping video, because it is unaivalable.")
        else:
            all_vids.append(get_video_details(curr_vid))
    print(f"Playlist \"{playlist.title}\" Stored Successfully!")
    return all_vids

def get_video_details(curr_vid: YouTube) -> list:
    '''Returns a list containing all details from a video object.'''
    curr_vid_details = []
    curr_vid_details.append(curr_vid.watch_url)
    # Adds video URL to list
    curr_vid_details.append(curr_vid.title)
    curr_vid_details.append(curr_vid.length/60)
    # Add time of video in minutes to list
    curr_vid_details.append(curr_vid.views)
    curr_vid_details.append(curr_vid.author)
    return curr_vid_details

def add_vid_to_playlist(playlist: Playlist, curr_vid: YouTube) -> None:
    '''Adds video curr_vid to playlist'''
    playlist.append(get_video_details(curr_vid))

def rand_vid(playlist: Playlist) -> list:
    '''Returns a random video's settings from a playlist'''
    if (len(playlist) <= 0):
        print("No video found!")
        return []
    random_video_index = random.randint(0, len(playlist)-1)
    return playlist[random_video_index]

def rand_vid_category(playlist, min_length = -1, max_length = -1, min_views = -1, max_views = -1, author = ""):
    '''Takes a playlist and some chosen categories, and gives a video from that category. Deletes all videos from
    different categories in a temporary list, and then takes a random video out of the temporary playlist.'''
    new_playlist = playlist
    if (min_length != -1):
        for i in reversed(range(0, len(new_playlist))):
            if (new_playlist[i][2] < min_length):
                del(new_playlist[i])
    if (max_length != -1):
        for i in reversed(range(0, len(new_playlist))):
            if (new_playlist[i][2] > max_length):
                del(new_playlist[i])
    if (min_views != -1):
        for i in reversed(range(0, len(new_playlist))):
            if (new_playlist[i][3] < min_views):
                del(new_playlist[i][3])
    if (max_views != -1):
        for i in reversed(range(0, len(new_playlist))):
            if (new_playlist[i][3] > max_views):
                del(new_playlist[i])
    if (author != ""):
        for i in reversed(range(0, len(new_playlist))):
            if (new_playlist[i][4].casefold() != author.casefold()):
                del(new_playlist[i])
    if (len(playlist) <= 0):
        print("No video found with the search criteria!")
        return []
    return(rand_vid(new_playlist))

all_playlists = []
pl_link = "https://www.youtube.com/playlist?list=PLEhSYc84M4xCljuyXNxEgVHLgdCzAm0vu"
playlist_one = Playlist(pl_link)
playlist_reference = {}
playlist_reference[playlist_one.title] = len(all_playlists)
# Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
all_playlists.append(get_playlist(playlist_one))
for x in range(5):
    print(rand_vid_category(all_playlists[playlist_reference["Favorite Videos"]], author = 'secret base'))




