from pytube import YouTube, Playlist
import pytube.exceptions
import random
from requests.structures import CaseInsensitiveDict

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
            all_vids.append(add_video_details_from_playlist(curr_vid))
    print(f"Playlist \"{playlist.title}\" Stored Successfully!")
    return all_vids

def add_video_details_from_playlist(curr_vid: YouTube) -> list:
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

def rand_vid_category(all_vids, min_length = -1, max_length = -1, min_views = -1, max_views = -1, author = "", title_contains = "", is_favorite = False):
    '''Takes a playlist and some chosen categories, and gives a video from that category. Deletes all videos from
    different categories in a temporary list, and then takes a random video out of the temporary list.'''
    temp_list = []
    for vid_details in all_vids:
        if (min_length != -1):
            if (vid_details[2] < min_length):
                continue
                # Skips current video if it doesn't meet criteria
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
        if (title_contains != ""):
            if (title_contains.casefold() not in vid_details[5].casefold()):
                continue
        if (is_favorite == True):
            if (vid_details[1] != True):
                continue
        temp_list.append(vid_details)
        # If video meets all criteria, it's added to the appropriate list
    if (len(temp_list) <= 0):
        print("No video found with the search criteria!")
        return []
    return(rand_vid(temp_list))

def make_video_favorite(all_vids: list, vid_title: str) -> None:
    compare_string = vid_title.casefold()
    # Makes the comparison string casefold once rather than in each for-loop iteration
    for vid_details in all_vids:
        if (vid_details[5].casefold() == compare_string):
            vid_details[1] = True
            return
    print(f"{vid_title} not found in the playlist. Did you spell it correctly?")

def get_video_details(vid_details: list) -> str:
    '''Stores all details from a video into comma-separated format'''
    stringVal = ""
    for i in range(len(vid_details)-1):
        stringVal += f"{vid_details[i]}, "
    stringVal += f"{vid_details[i+1]}\n"
    # Stores video details. Stores title of video last so video title doesn't interrupt CSV
    # CSV still interrupted if a YouTube author has a comma in their username, but extremely uncommon.
    return (stringVal)

def write_playlist_data(all_vids: list, playlistTitle: str) -> None:
    # Allows for specific user-inputted title or the default title
    with open("user_data.txt", "a", encoding = "utf-8") as f:
        f.write(playlistTitle + "\n")
        for vid_details in all_vids:
            f.write(get_video_details(vid_details))
        f.write("\n")
    print("Playlist Data stored to file!")

def read_all_playlist_data(all_playlists: list, playlist_reference: dict):
    with open("user_data.txt", "r", encoding = "utf-8") as f:
        while True:
            curr_line = f.readline().strip()
            if curr_line == (''):
                return
            print(f"Extracting details of playlist titled: {curr_line}")
            playlist_reference[curr_line] = len(all_playlists)
            # currLine stores the title first if the file doesn't immediately end. Adds title to dictionary at right index.
            curr_playlist = []
            all_playlists.append(curr_playlist)
            for curr_line in f:
                if curr_line == '\n':
                    break
                    # Goes back to while loop to add a new playlist after a newline
                if curr_line == '':
                    return
                    # If there's an extra newline, file end will get caught in other loop
                add_video_details_from_file(curr_playlist, curr_line)
                # Reads current line as a CSV, appending it to playlist
                
def add_video_details_from_file(all_vids, line_to_read):
    '''Reads current line as a CSV, and appends it's video details to playlist'''
    curr_vid = []
    split_line = line_to_read.split(', ')
    part_six = split_line[5]
    for i in range(6, len(split_line)):
        part_six += ", " + split_line[i]
        # Doesn't stop if title has a comma in it
    part_six = part_six.strip()
    curr_vid.append(split_line[0])
    if split_line[1] == 'True': 
        curr_vid.append(True)
    else:
        curr_vid.append(False)
    curr_vid.append(float(split_line[2]))
    curr_vid.append(float(split_line[3]))
    curr_vid.append(split_line[4])
    curr_vid.append(part_six)
    all_vids.append(curr_vid)

def store_playlist(all_playlists, playlist_reference, playlist_link) -> None:
    '''Stores playlist in list, dictionary, and file, where it can be re-extracted'''
    curr_playlist = Playlist(playlist_link)
    playlist_reference[curr_playlist.title] = len(all_playlists)
    # Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
    all_playlists.append(get_playlist(curr_playlist))
    # Gets all playlist data and appends it
    write_playlist_data(all_playlists[playlist_reference[curr_playlist.title]], curr_playlist.title)

all_playlists = []
playlist_reference = CaseInsensitiveDict()
# Creates a dictionary to store all the video titles by their index. Case-insensitive gives user more potential keys.
pl_link = "https://www.youtube.com/playlist?list=PLEhSYc84M4xCljuyXNxEgVHLgdCzAm0vu"
pl_link2 = "https://www.youtube.com/playlist?list=PLUXSZMIiUfFS6azeerXYR4gQExSwPCx-s"
# Playlists given purely to test
# store_playlist(all_playlists, playlist_reference, pl_link)
# store_playlist(all_playlists, playlist_reference, pl_link2)
read_all_playlist_data(all_playlists, playlist_reference)

for x in range(5):
   print(rand_vid_category(all_playlists[playlist_reference["favorite videos"]], title_contains = "angry"))
# Testing the playlist




