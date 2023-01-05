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

def write_playlist_data(all_vids, playlistTitle) -> None:
    # Allows for specific user-inputted title or the default title
    with open("user_data.txt", "a", encoding = "utf-8") as f:
        f.write(playlistTitle + "\n")
        for vid_details in all_vids:
            f.write(get_video_details(vid_details))
        f.write("\n")
    print("Playlist Data Stored!")

def read_all_playlist_data(all_playlists, playlist_reference):
    with open("user_data.txt", "r", encoding = "utf-8") as f:
        while True:
            curr_line = f.readline()
            if curr_line == (''):
                return
            playlist_reference[curr_line] = len(all_playlists)
            # currLine stores the title first if the file doesn't immediately end. Adds title to dictionary at right index.
            curr_playlist = []
            all_playlists.append(curr_playlist)
            for curr_line in f.readline():
                if curr_line == '\n':
                    break
                    # Goes back to while loop to add a new playlist after a newline
                if curr_line == '':
                    return
                    # If file ends, return. If there's an extra newline, it will get caught later.
                read_file_line(curr_playlist, curr_line)
                # Gives the current 
                
def read_file_line(all_vids, line_to_read):
    split_line = line_to_read.split(', ')
    part_five = split_line - split_line[0] - split_line[1] - split_line[2] - split_line[3]
    # Split_line[4], but works with comma in title
    all_vids.append(split_line[0])
    if split_line[1] == 'True': 
        all_vids.append(True)
    else:
        all_vids.append(False)
    all_vids.append(int(split_line[2]))
    all_vids.append(int(split_line(3)))
    all_vids.append(part_five)

all_playlists = []
pl_link = "https://www.youtube.com/playlist?list=PLEhSYc84M4xCljuyXNxEgVHLgdCzAm0vu"
# Playlist given purely to test

playlist_one = Playlist(pl_link)
playlist_reference = {}
playlist_reference[playlist_one.title] = len(all_playlists)
all_playlists.append(get_playlist(playlist_one))
write_playlist_data(all_playlists[0], playlist_one.title)

# Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
# Playlist stored in list, dictionary, and file, where it can be re-extracted


for x in range(0):
    print(rand_vid_category(all_playlists[playlist_reference["Favorite Videos"]], min_length = 30, max_length = 500, min_views = 20))
# Testing the playlist




