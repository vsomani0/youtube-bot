import discord
from discord.ext import commands
from pytube import YouTube, Playlist
import pytube.exceptions
import random
from requests.structures import CaseInsensitiveDict

intents = discord.Intents.default()
intents.message_content = True

class Video_Data:
    def __init__(self, url, is_favorite, lengthMinutes, views, author, title):
        self.url = url
        self.is_favorite = is_favorite
        self.length = lengthMinutes
        self.views = views
        self.author = author
        self.title = title
        print("Video successfully initialized directly")

    def __init__(self, curr_vid: YouTube):
        self.url = curr_vid.watch_url
        # Adds video URL to list
        self.is_favorite = False
        # By default, all videos are false, to indicate they are not a favorite
        self.length = curr_vid.length/60
        # Add time of video in minutes to list
        self.views = curr_vid.views
        self.author = curr_vid.author
        self.title = curr_vid.title
        print("Video successfully initialized through YouTube!")

class Config:
    '''Class that stores a configuration of settings for videos. Can be called at any time.'''
    def __init__(self, title, min_length = None, max_length = None, min_views = None, max_views = None, author = None, title_contains = None, is_favorite = None):
        self.title = title
        self.min_length = min_length
        self.max_length = max_length
        self.min_views = min_views
        self.max_views = max_views
        self.author = author
        self.title_contains = title_contains
        self.is_favorite = is_favorite
    
    def set_null(self):
        self.title = None
        self.min_length = None
        self.max_length = None
        self.min_views = None
        self.max_views = None
        self.author = None
        self.title_contains = None
        self.is_favorite = None

    def get_args_from_string_list(self, args: list):
        if (args[0].casefold() != "none"):
            self.min_length = int(args[0])
        if (args[1].casefold() != "none"):
            self.max_length = int(args[1])
        if (args[2].casefold() != "none"):
            self.min_views = int(args[2])
        if (args[3].casefold() != "none"):
            self.max_views = int(args[3])
        if (args[4].casefold() != "none"):
            self.author = args[4]
        if (args[5].casefold() != "none"):
            self.title_contains = args[5]
        if (args[6].casefold() != "none"):
            if (args[6].casefold() == "true"):
                self.is_favorite = True
            # If is_favorite isn't none or true, and it is a valid parameter, it must be false.
            else:
                self.is_favorite = False
    def get_parameters(self) -> str:
        '''Returns a string that prints out all the parameters/Categories in the function.'''
        # Using str function to concatenate multiple types like int and none
        config_settings = str(self.min_views) + " " + str(self.max_views) + " " + str(self.min_length) + " " + str(self.max_length) + " " + str(self.author) + " " + str(self.title_contains) + " " + str(self.is_favorite)
        return config_settings
    
class Playlist_Data:
    def __init__(self, title):
        self.title = title
        self.videos = []
        print("Empty playlist successfully initialize!")

    def add_video(self, video: Video_Data):
        self.videos.append(video)

    def add_details_from_playlist(self, playlist: Playlist):
        '''Extracts all videos from each video in playlist, and adds into videos list .'''
        print(f'Downloading all video data from playlist \"{playlist.title}\". Please wait a few moments.')
        for video in playlist:
            try:
                # Get the video details from its link using the Pytube library
                curr_vid = YouTube(video)
            except pytube.exceptions.VideoUnavailable:
            # Exception doesn't work, pytube library appears faulty
                print("Skipping video, because it is unaivalable.")
            else:
                # Adds the video itself to the playlist
                self.videos.append(Video_Data(curr_vid))

    def rand_vid(self) -> Video_Data:
        '''Returns a random video's settings from a playlist'''
        if (len(self.videos) == 0):
            return None
        # Consider making this random.randomchoice after fixing other issues.
        random_video_index = random.randint(0, len(self.videos)-1)
        return self.videos[random_video_index]

    def rand_vid_category(self, min_length = None, max_length = None, min_views = None, max_views = None, author = None, title_contains = None, is_favorite = None, config: Config = None) -> Video_Data:
        '''Takes a playlist and some chosen categories, and gives a video from that category. Deletes all videos from
        different categories in a temporary list, and then takes a random video out of the temporary list.'''
        if (config != None):
            min_length = config.min_length
            max_length = config.max_length
            min_views = config.min_views
            max_views = config.max_views
            author = config.author
            title_contains = config.title_contains
            is_favorite = config.is_favorite
        shortened_playlist = Playlist_Data(self.title)
        for vid_details in self.videos:
            if (is_favorite != None):
                if (vid_details.is_favorite != is_favorite):
                    continue
            if (min_length != None):
                if (vid_details.length < min_length):
                    continue
                    # Skips current video if it doesn't meet criteria
            if (max_length != None):
                if (vid_details.length > max_length):
                    continue
            if (min_views != None):
                if (vid_details.views < min_views):
                    continue
            if (max_views != None):
                if (vid_details.views > max_views):
                    continue
            if (author != None):
                if (vid_details.author.casefold() != author.casefold()):
                    continue
            if (title_contains != None):
                if (title_contains.casefold() not in vid_details.title.casefold()):
                    continue
            shortened_playlist.add_video(vid_details)
            # If video meets all criteria, it's added to the appropriate list
        return shortened_playlist.rand_vid()
        
    def make_video_favorite_with_title(self, videoTitle) -> bool:
        # Go through a list of video objects
        for video in self.videos:
            if (videoTitle.casefold() == video.title.casefold()):
                video.is_favorite = True
                return True
        # If it goes through the entire for loop, print error to console and return bool
        print(f"{videoTitle} not found in playlist {self.title}.")
        return False

    def make_video_favorite_with_url(self, video_url):
        # Go through a list of video objects
        for video in self.videos:
            if (video_url == video.url):
                video.is_favorite = True
                return True
        # If it goes through the entire for loop, print error to console and return bool
        print(f"{video_url} not found in playlist {self.title}, did you link it correctly?")
        return False

def get_video_details(vid_details: list) -> str:
    '''Stores all details from a video into comma-separated format as a helper function'''
    stringVal = ""
    for i in range(len(vid_details)-1):
        stringVal += f"{vid_details[i]}, "
    stringVal += f"{vid_details[i+1]}\n"
    # Stores video details. Stores title of video last so video title doesn't interrupt CSV
    # CSV still interrupted if a YouTube author has a comma in their username, but extremely uncommon.
    return (stringVal)

def write_playlist_data(all_vids: list, playlistTitle: str) -> None:
    '''Write data specifically for a playlist to a file'''
    # Allows for specific user-inputted title or the default title
    with open("user_data.txt", "a", encoding = "utf-8") as f:
        f.write(playlistTitle + "\n")
        for vid_details in all_vids:
            f.write(get_video_details(vid_details))
        f.write("\n")
    print("Playlist Data stored to file!")

def read_all_playlist_data_helper(all_playlists: list, playlist_reference: dict):
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
    '''Reads current line as a CSV, and appends it's video details to playlist. Helper function for reading file'''
    curr_vid = []
    split_line = line_to_read.split(', ')
    part_six = split_line[5]
    for i in range(6, len(split_line)):
        part_six += ", " + split_line[i]
        # Doesn't stop midway through title if title has a comma in it
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

def store_playlist_helper(all_playlists, playlist_reference, playlist_link, title = None) -> bool:
    '''Stores playlist in list, dictionary, and file, where it can be re-extracted'''
    curr_playlist = Playlist(playlist_link)
    # If no extra title is given, title automatically takes the title of the playlist
    if (title == None):
        title = curr_playlist.title
    # Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
    curr_playlist_data = Playlist_Data(title)
    curr_playlist_data.add_details_from_playlist(curr_playlist)
    # Get all playlist data and append it to the list
    all_playlists.append(curr_playlist_data)
    playlist_reference[title] = len(all_playlists)-1
    # write_playlist_data(all_playlists[playlist_reference[title]], title)
    return True

# Create a dictionary to store all the video titles by their index. Case-insensitive gives user more potential keys.
playlist_reference = CaseInsensitiveDict()
all_playlists = []
config_reference = CaseInsensitiveDict()
all_configs = []
last_config = Config("last config")
# config_reference = CaseInsensitiveDict()
# all_configs = []

bot = commands.Bot(command_prefix = '$', intents = intents)


def check_valid_categories(args: list) -> str:
    '''Checks for an error in giving categories for rand_vid_category. Either returns the error message, which the discord
    bot can asynchronously send, or returns no error to indicate no error.'''
    error_message = ""
    if (len(args) != 7):
        error_message = "Wrong number of arguments"
        return error_message
    if (args[0].casefold() != "none"):
        if not (args[0].isdigit()):
            error_message = ("Min time needs to be a number!")
            return error_message
    if (args[1].casefold() != "none"):
        if not (args[1].isdigit()):
            error_message = ("Max time needs to be a number!")
            return error_message
    if (args[2].casefold() != "none"):
        if not (args[2].isdigit()):
            error_message = ("Min views needs to be a number!")
            return error_message
    if (args[3].casefold() != "none"):
        if not (args[3].isdigit()):
            error_message = ("Max views needs to be a number!")
            return error_message
    if (args[6].casefold() != "none"):
        if (args[6].casefold() != "true" & args[7].casefold() != "false"):
            error_message = ("Is favorite needs to be either \"true\" or \"false\" or \"none\"")
            return error_message
    return "no error"

@bot.command()
async def random_video(ctx, arg):
    if (arg not in playlist_reference):
        await ctx.send(f"{arg} not found as a valid playlist. Did you save this playlist yet?")
        await ctx.send("If you did save the playlist, make sure to state its name correctly. Use quotations around multi-word names")
        await ctx.send("Syntax: $random_video \"Playlist Name\"")
        return
    else:
        index_to_use = playlist_reference[arg]
        video_chosen = (all_playlists[index_to_use]).rand_vid()
        if (video_chosen is None):
            await ctx.send("No video found!")
            return
        await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")

@bot.command()
async def save_playlist(ctx, *args):
    if (len(args) == 0):
        await ctx.send("Please provide the playlist URL")
    if (len(args) == 1):
        await ctx.send("Attempting to store the playlist. This may take a few moments.")
        if (store_playlist_helper(all_playlists, playlist_reference, args[0])) == True:
            await ctx.send("Playlist saved successfully!")
        else:
            await ctx.send("An error occured while trying to save the playlist")
    else:
        if (store_playlist_helper(all_playlists, playlist_reference, args[0], title = args[1])) == True:
            ctx.send(f"Playlists saved successfully with title {args[1]}")
        else:
            ctx.send("An error occured while trying to save the playlist")

@bot.command()
async def random_video_with_category(ctx, *args):
    video_chosen = []
    if (len(args) == 0):
        await ctx.send("Please provide a playlist name")
        return
    if (len(args) != 2 & len(args) != 8):
        await ctx.send("Invalid number of arguments.")
        await ctx.send("If config is set, syntax: $random_video_with_category \"Playlist Name\" \"Config Name\" ")
        await ctx.send("If not, syntax: $random_video_with_category \"Playlist Name\" min_length max_length min_views max_views author_name title_contains is_favorite")
        await ctx.send("For every category intended to not be set, \"-\" or \"None\" indicate it is not set")
    if (args[0] not in playlist_reference):
        await ctx.send(f"{args[0]} not found as a valid playlist. Did you save this playlist yet?")
        await ctx.send("If you did save the playlist, make sure to state its name correctly. Use quotations around multi-word names")
        return
    playlist_to_use = all_playlists[playlist_reference[args[0]]]
    if (len(args) == 2):
        
        if (args[1] not in config_reference):
            await ctx.send(f"{args[1]} not found as a valid config.")
            await ctx.send("Make sure to spell config name correctly. Use quotations around multi-word names")
            return
        config_to_use = all_configs[config_reference[args[1]]]
        await ctx.send(f"Attempting to find playlist in {config_to_use.title}")
        video_chosen = playlist_to_use.rand_vid_category(config = config_to_use)
        print(video_chosen)
        if video_chosen is None:
            await ctx.send("No video found with selected criteria!")
        else:
            await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")
    if (len(args) == 8):
        error_message = check_valid_categories(args[1:])
        if (error_message != "no error"):
            await ctx.send(f"Error in categories with playlist: {error_message}")
            return
        last_config.get_args_from_string_list(args[1:])
        video_chosen = (playlist_to_use.rand_vid_category(last_config))
        if video_chosen is None:
            await ctx.send("No video found with selected criteria!")
        else:
            await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")

# @bot.command()
# async def help(ctx):
#     await ctx.send("FIXME!")

@bot.command()
async def list(ctx):
    await ctx.send("FIXME!")

@bot.command()
async def add_config(ctx, *args):
    error_message = check_valid_categories(args[1:])
    if (error_message != "no error"):
        await ctx.send(f"Error creating config: {error_message}")
        return
    curr_config = Config(args[0])
    curr_config.get_args_from_string_list(args[1:])
    all_configs.append(curr_config)
    config_reference[curr_config.title] = len(all_configs) - 1
    await ctx.send(f"Successfully creating config named {curr_config.title}")
    await ctx.send(f"Parameters: {curr_config.get_parameters()}")
# Use with a discord key -- key is hidden in a different file
with open ("key.txt", "r", encoding= "utf-8") as f:
    key = f.readline()
bot.run(key)
# a