from pytube import YouTube, Playlist
import pytube.exceptions
import random

def get_playlist(playlist: Playlist) -> list:
    '''Stores all chosen video data from a playlist into a list.'''
    all_vids = []
    print(f'Downloading all video data from playlist \"{playlist.title}\". Please wait a few moments.')
    for video in playlist:
        try:
            curr_vid = YouTube(video)
        except pytube.exceptions.VideoUnavailable:
    # Exception doesn't work, pytube library appears faulty
            print("Skipping video, because it is unaivalable.")
        else:
            all_vids.append(add_video_details(curr_vid))
    print(f"Playlist \"{playlist.title}\" Stored Successfully!")
    return all_vids

def add_video_details(curr_vid: YouTube) -> list:
    '''Returns a list containing all details from a video object.'''
    curr_vid_details = []
    curr_vid_details.append(curr_vid.watch_url)
    # Adds video URL to list
    curr_vid_details.append(False)
    # By default, all videos are false, to indicate they are not a favorite
    curr_vid_details.append(curr_vid.length/60)
    # Add time of video in minutes to list
    curr_vid_details.append(curr_vid.views)
    curr_vid_details.append(curr_vid.author)
    curr_vid_details.append(curr_vid.title)
    
    return curr_vid_details

def rand_vid(all_vids) -> list:
    '''Returns a random video's settings from a playlist'''
    if (len(all_vids) <= 0):
        print("No video found!")
        return []
    random_video_index = random.randint(0, len(all_vids)-1)
    return all_vids[random_video_index]

def rand_vid_category(all_vids, min_length = -1, max_length = -1, min_views = -1, max_views = -1, author = ""):
    '''Takes a playlist and some chosen categories, and gives a video from that category. Deletes all videos from
    different categories in a temporary list, and then takes a random video out of the temporary list.'''
    temp_list = []
    for vid_details in all_vids:
        if (min_length != -1):
            if (vid_details[2] < min_length):
                continue
        if (max_length != -1):
            if (vid_details[2] > max_length):
                continue
        if (min_views != -1):
            if (vid_details[3] < min_views):
                continue
        if (max_views != -1):
            if (vid_details[3] > max_views):
                continue
        if (author != ""):
            if (vid_details[4].casefold() != author.casefold()):
                continue
        temp_list.append(vid_details)
    if (len(temp_list) <= 0):
        print("No video found with the search criteria!")
        return []
    return(rand_vid(temp_list))

def get_video_details(vid_details: list) -> str:
    '''Stores all details from a video into comma-separated format'''
    stringVal = ""
    for i in range(len(vid_details)-1):
        stringVal += f"{vid_details[i]}, "
    stringVal += f"{vid_details[i+1]}\n"
    # Stores video details. Stores title of video last so video title doesn't interrupt CSV
    # CSV interrupted if a YouTube author had a comma in their username, but this is extremely uncommon.
    return (stringVal)

def write_playlist_data(all_vids: list, playlistTitle: str) -> None:
    # Allows for specific user-inputted title or the default title
    with open("user_data.txt", "a", encoding = "utf-8") as f:
        f.write(playlistTitle + "\n")
        for vid_details in all_vids:
            f.write(get_video_details(vid_details))
        f.write("\n")
    print("Playlist Data Stored!")

all_playlists = []
pl_link = "https://www.youtube.com/playlist?list=PLEhSYc84M4xCljuyXNxEgVHLgdCzAm0vu"
# Playlist given purely to test

playlist_one = Playlist(pl_link)
playlist_reference = {}
all_playlists.append(get_playlist(playlist_one))
write_playlist_data(all_playlists[0], playlist_one.title)
playlist_reference[playlist_one.title] = len(all_playlists) - 1
# Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
# Playlist stored in list, dictionary, and file, where it can be re-extracted


for x in range(0):
    print(rand_vid_category(all_playlists[playlist_reference["Favorite Videos"]], min_length = 30, max_length = 500, min_views = 20))
# Testing the playlist




