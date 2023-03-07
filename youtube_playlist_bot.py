import discord
from discord.ext import commands
from pytube import YouTube, Playlist
import random

intents = discord.Intents.default()
intents.message_content = True


class Video_Data:
    def __init__(self, curr_vid: YouTube = None):
        if curr_vid == None:
            self.is_favorite = None
            self.length = None
            self.views = None
            self.author = None
            self.title = None
            return
        self.url = curr_vid.watch_url
        # Adds video URL to list
        self.is_favorite = False
        # By default, all videos are false, to indicate they are not a favorite
        self.length = curr_vid.length/60
        # Add time of video in minutes to list
        self.views = curr_vid.views
        self.author = curr_vid.author
        self.title = curr_vid.title

    def categories_csv(self) -> str:
        return (f"{self.url}, {self.is_favorite}, {self.length}, {self.views}, {self.author}, {self.title}")


class Config:
    '''Stores a configuration of settings for videos. Can be called at any time.'''

    def __init__(self, title, min_length=None, max_length=None, min_views=None, max_views=None, author=None, title_contains=None, is_favorite=None):
        self.title = title.casefold()
        self.min_length = min_length
        self.max_length = max_length
        self.min_views = min_views
        self.max_views = max_views
        self.author = author
        self.title_contains = title_contains
        self.is_favorite = is_favorite
        print("New config class created!")

    def set_null(self):
        self.title = None
        self.min_length = None
        self.max_length = None
        self.min_views = None
        self.max_views = None
        self.author = None
        self.title_contains = None
        self.is_favorite = None

    def __str__(self):
        return (f"{self.title}, {self.min_length}, {self.max_length}, {self.min_views}, {self.max_views}, {self.author}, {self.title_contains}, {self.is_favorite}")

    def categories_csv(self):
        return (f"Config: {self.title}, {self.min_length}, {self.max_length}, {self.min_views}, {self.max_views}, {self.author}, {self.title_contains}, {self.is_favorite}")

    def get_args_from_string_list(self, args: list):
        '''Converts list to config class'''
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
            else:
                self.is_favorite = False
        print("New config settings chosen")
        print(self)

    def get_parameters(self) -> str:
        '''Returns a string that prints out all the parameters/Categories in the function.'''
        # Using str function to concatenate multiple types like int and none
        config_settings = (f"""min length(minutes): {str(self.min_length)}, max length(minutes): \
{str(self.max_length)}, min_views: {str(self.min_views)}, max_views: self.max_views, author: {str(self.author)},\
title contains: {str(self.title_contains)}, is_favorite: {str(self.is_favorite)}""")
        return config_settings


class Playlist_Data:
    ''' Stores data for playlist necessary for playlist. Not playlist class because it is self-made'''

    def __init__(self, title: str, id: str):
        self.title = title.casefold()
        self.id = id
        self.videos = []

    def add_video(self, video: Video_Data):
        self.videos.append(video)

    def add_details_from_playlist(self, playlist: Playlist):
        '''Extracts all videos from each video in playlist, and adds into videos list .'''
        print(
            f'Downloading all video data from playlist \"{self.title}\". Please wait a few moments.')
        for video in playlist:
            curr_vid = YouTube(video)
            try:
                if ((curr_vid is None) or (curr_vid.length is None)):
                    continue
                self.videos.append(Video_Data(curr_vid))
            except TypeError:
                print(f"Type error occurred! {curr_vid}")
                continue

    def rand_vid(self) -> Video_Data:
        '''Returns a random video's settings from a playlist'''
        if (len(self.videos) == 0):
            return None
        # Consider making this random.randomchoice after fixing other issues.
        random_video_index = random.randint(0, len(self.videos)-1)
        return self.videos[random_video_index]

    def rand_vid_category(self, min_length=None, max_length=None, min_views=None, max_views=None, author=None, title_contains=None, is_favorite=None, config: Config = None) -> Video_Data:
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
        # Playlist Object, but with categories removed
        shortened_playlist = Playlist_Data(self.title, self.id)
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

    def make_video_favorite(self, curr_vid_title) -> bool:
        # Go through a list of video objects
        for prev_vid in self.videos:
            if (curr_vid_title.casefold() == prev_vid.title):
                prev_vid.is_favorite = True
                return True
        print(f"{curr_vid_title} not found in playlist {self.title}.")
        return False

    def remove_video_favorite(self, curr_vid_title):
        # Go through a list of video objects
        for prev_vid in self.videos:
            if (curr_vid_title.casefold() == prev_vid.title):
                prev_vid.is_favorite = False
                return True
        print(
            f"{curr_vid_title} not found in playlist {self.title}, did you link it correctly?")
        return False


all_playlists = []
all_configs = []
last_config = Config("last")  # Stores last settings if no config is created
all_configs.append(last_config)


def write_playlist_data(curr_playlist_data: Playlist_Data) -> None:
    '''Write data specifically for a playlist to a file'''
    # Allows for specific user-inputted title or the default title
    with open("user_data.txt", "a", encoding="utf-8") as f:
        f.write(
            f"Playlist: {curr_playlist_data.title}\t{curr_playlist_data.id}\n")
        for video in curr_playlist_data.videos:
            f.write(video.categories_csv())
            f.write("\n")
        f.write("\n")
    print("Playlist Data stored to file!")


def write_config_data(curr_config: Config):
    with open("user_data.txt", "a", encoding="utf-8") as f:
        f.write(curr_config.categories_csv())
        f.write("\n")
    print("Config data stored to file!")


def read_all_details_from_file():
    with open("user_data.txt", "r", encoding="utf-8") as f:
        while True:
            curr_line = f.readline().strip()
            if curr_line == (''):
                return
            split_curr_line = curr_line.split(" ", 1)
            config_or_playlist = split_curr_line[0]
            if (config_or_playlist == "Config:"):
                read_config_details_from_file(split_curr_line[1])
                continue
            elif (config_or_playlist != "Playlist:"):
                raise RuntimeError(
                    f"Reading from file at {split_curr_line} is neither config nor playlist!")
            playlist_details = split_curr_line[1].split('\t', 1)
            playlist_title = playlist_details[0]
            playlist_id = playlist_details[1]
            print(f"Extracting details of playlist titled: {playlist_title}")
            # currLine stores the title first if the file doesn't immediately end. Adds title to dictionary at right index.
            curr_playlist_data = Playlist_Data(playlist_title, playlist_id)
            all_playlists.append(curr_playlist_data)
            for curr_line in f:
                if curr_line == '\n':
                    break  # Return to previous loop
                if curr_line == '':
                    return
                # todo
                print(
                    f"Attempting to add video to playlist {curr_playlist_data.title}")
                read_video_details_from_file(curr_playlist_data, curr_line)

                # If there's an extra newline, file end will get caught in other loop

                # Reads current line as a CSV, appending it to playlist


def read_config_details_from_file(line_to_read):
    split_line = line_to_read.split(', ')  # todo
    if (len(split_line) != 8):
        raise RuntimeError(
            f"{split_line} has {len(split_line)} elements -- not 8!")
    curr_config = Config(split_line[0])
    curr_config.get_args_from_string_list(split_line[1:])
    all_configs.append(curr_config)


def read_video_details_from_file(curr_playlist_data: Playlist_Data, line_to_read):
    '''Reads current line as a CSV, and appends it's video details to playlist. Helper function for reading file'''
    split_line = line_to_read.split(', ')
    print(split_line)
    part_six = split_line[5]
    for i in range(6, len(split_line)):
        part_six += ", " + split_line[i]  # Continue if title has comma in it
    curr_vid = Video_Data()
    part_six = part_six.strip()
    curr_vid.url = split_line[0]
    curr_vid.is_favorite = split_line[1]
    curr_vid.length = float(split_line[2])
    curr_vid.views = float(split_line[3])
    curr_vid.author = split_line[4]
    curr_vid.title = split_line[5]
    curr_playlist_data.add_video(curr_vid)


def store_playlist_helper(playlist_link, title=None) -> str:
    '''Stores playlist in list, dictionary, and file, where it can be re-extracted'''
    try:
        curr_playlist = Playlist(playlist_link)
        if (curr_playlist.title is None):
            # Exception keyerror comes here, trying to extract details
            return "Failed to store playlist data!"
    except KeyError:
        return "Playlist data not found! Make sure your playlist is public, and is a valid link!"
    # If no extra title is given, title automatically takes the title of the playlist
    if (title is None):
        # Title for playlist_data object. If not set, default to title of playlist itself.
        title = curr_playlist.title
    for prev_playlist in all_playlists:
        if prev_playlist.id == curr_playlist.playlist_id:
            return "You have already stored this playlist!"
        if prev_playlist.title.casefold() == title.casefold():
            # No unique id for title. Cannot store
            return "There is a playlist with the same title as the current one. Use a different title!"

    # Dictionary matches up playlist name with index in list, allowing user to call a playlist by its name.
    curr_playlist_data = Playlist_Data(title, curr_playlist.playlist_id)
    curr_playlist_data.add_details_from_playlist(curr_playlist)
    # Get all playlist data and append it to the list
    all_playlists.append(curr_playlist_data)
    write_playlist_data(curr_playlist_data)
    return "no error"


def find_playlist(playlist_name: str):
    '''Finds and returns playlist with name, None if no playlist with matching title'''
    casefold_playlist_name = playlist_name.casefold()
    for curr_playlist in all_playlists:
        if (curr_playlist.title == casefold_playlist_name):
            return curr_playlist
    return None


def find_config(config_name: str):
    '''Finds and returns config with matching name'''
    casefold_config_name = config_name.casefold()
    for curr_config in all_configs:
        if (curr_config.title == casefold_config_name):
            return curr_config
    return None


read_all_details_from_file()
for playlist_data in all_playlists:
    print(f"{playlist_data.title} has {len(playlist_data.videos)} videos!")  # todo
bot = commands.Bot(command_prefix='$', intents=intents)


def check_valid_categories(args: list) -> str:
    '''Checks for an error in giving categories for rand_vid_category. Either returns the error message, which the discord
    bot can asynchronously send, or returns no error to indicate no error.'''
    error_message = ""
    if (len(args) < 7):
        error_message = "Too few categories selected. Need 7(min_length, max_length, min_views, max_views, author, title_contains, isFavorite)"
        return error_message
    if (len(args) > 7):
        error_message = "Too many categories selected. Need 7(min_length, max_length, min_views, max_views, author, title_contains, isFavorite)"
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
            error_message = (
                "Is favorite needs to be either \"true\" or \"false\" or \"none\"")
            return error_message
    return "no error"


@bot.command()
async def random_video(ctx, arg):
    playlist_to_use = find_playlist(arg)
    if (playlist_to_use is None):
        await ctx.send(f"{arg} not found as a valid playlist. Did you save this playlist yet?")
        await ctx.send("If you did save the playlist, make sure to state its name correctly. Use quotations around multi-word names")
        await ctx.send("Syntax: $random_video \"Playlist Name\"")
        return
    else:
        video_chosen = (playlist_to_use).rand_vid()
        if (video_chosen is None):
            await ctx.send("No video found!")
            return
        await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")


@bot.command()
async def save_playlist(ctx, *args):
    if (len(args) == 0):
        await ctx.send("Please provide the playlist URL")
        return
    if (len(args) == 1):
        await ctx.send("Attempting to store the playlist. This may take a few moments.")
        # Stores playlist and checks for error
        error_message = store_playlist_helper(playlist_link=args[0])
        if (error_message == "no error"):
            playlist_title = all_playlists[len(all_playlists)-1].title
            playlist_num_vids = len(all_playlists[len(all_playlists)-1].videos)
            await ctx.send(f"Playlist {playlist_title} saved successfully with {playlist_num_vids} videos!")
            return
        else:
            await ctx.send("An error occured while trying to save the playlist")
            await ctx.send(error_message)
            return
    error_message = store_playlist_helper(args[0], title=args[1])
    if (error_message == "no error"):
        await ctx.send(f"Playlists saved successfully with title {args[1]}")
    else:
        await ctx.send("An error occured while trying to save the playlist")
        await ctx.send(error_message)


@bot.command()
async def random_video_with_category(ctx, *args):
    video_chosen = []
    if (len(args) == 0):
        await ctx.send("Please provide a playlist name")
        return
    if (len(args) != 2) & (len(args) != 8):
        # Not config type, and doesn't have all categories listed out
        await ctx.send("Invalid number of arguments. Need either 2 or 8 arguments AFTER initial random_video_with_category call")
        await ctx.send("If config is set, syntax: $random_video_with_category \"Playlist Name\" \"Config Name\" ")
        await ctx.send("If not, syntax: $random_video_with_category \"Playlist Name\" min_length max_length min_views max_views author_name title_contains is_favorite")
        await ctx.send("For every category intended to not be set, \"None\" indicates it is not set")
        return
    playlist_to_use = find_playlist(args[0])
    if (playlist_to_use is None):
        await ctx.send(f"{args[0]} not found as a valid playlist. Did you save this playlist yet?")
        await ctx.send("If you did save the playlist, make sure to state its name correctly. Use quotations around multi-word names")
        return
    if (len(args) == 2):
        config_to_use = find_config(args[1])
        if (config_to_use is None):
            await ctx.send(f"{args[1]} not found as a valid config.")
            await ctx.send("Make sure to spell config name correctly. Use quotations around multi-word names")
            return
        video_chosen = playlist_to_use.rand_vid_category(config=config_to_use)
        print(video_chosen)
        if video_chosen is None:
            await ctx.send("No video found with selected criteria!")
        else:
            await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")
    if (len(args) == 8):
        # All categories listed out
        error_message = check_valid_categories(args[1:])
        if (error_message != "no error"):
            await ctx.send(f"Error in categories with playlist: {error_message}")
            return
        last_config.set_null()
        # Sets new categories, adds it to last_config
        last_config.get_args_from_string_list(args[1:])
        video_chosen = (playlist_to_use.rand_vid_category(config=last_config))
        if video_chosen is None:
            await ctx.send("No video found with selected criteria!")
        else:
            await ctx.send(f"{video_chosen.url} -- {video_chosen.title} by {video_chosen.author}")


@bot.command()
async def list(ctx):
    await ctx.send("Link to commands: https://docs.google.com/document/d/1lWFo4FM3kI9snYTbAWLvjgvuUP1IkLcbzcUSId_IdZ4/edit")

@bot.command()
async def add_favorite(ctx, *args):
    playlist_name = args[0]
    video_name = args[1]

    playlist_to_use = find_playlist(playlist_name)
    if (playlist_to_use is None):
        await ctx.send("Playlist not found. Double check your spelling!")
        return
    if (playlist_to_use.make_video_favorite(video_name) is False):
        await ctx.send(f"Failed to find video in playlist titled {playlist_to_use.title}. Make sure you spelled it's name correctly!")
        return
    await ctx.send(f"{video_name} is now a favorite in playlist {playlist_to_use.title}!")


@bot.command()
async def remove_favorite(ctx, *args):
    playlist_name = args[0]
    video_name = args[1]

    playlist_to_use = find_playlist(playlist_name)
    if (playlist_to_use is None):
        await ctx.send("Playlist not found. Double check your spelling!")
        return
    if (playlist_to_use.remove_video_favorite(video_name) is False):
        await ctx.send(f"Failed to find video in playlist titled {playlist_to_use.title}. Make sure you spelled it's name correctly!")
        return
    await ctx.send(f"{video_name} is no longer a favorite in playlist {playlist_to_use.title}!")


@bot.command()
async def add_config(ctx, *args):
    ''' Creates new config '''
    curr_config_title = args[0].casefold()
    if curr_config_title == "last":
        await ctx.send("\"last\" is not a valid config name. Use a different name!")
    for prev_config in all_configs:
        if prev_config.title == curr_config_title:
            await ctx.send(f"\"{curr_config_title}\" is already in a previous config's title. Use a new name!")
            return
    error_message = check_valid_categories(args[1:])
    if (error_message != "no error"):
        await ctx.send(f"Error creating config: {error_message}")
        return
    curr_config = Config(curr_config_title)
    curr_config.get_args_from_string_list(args[1:])
    all_configs.append(curr_config)
    write_config_data(curr_config)
    await ctx.send(f"Successfully creating config named {curr_config.title.casefold()}")
    await ctx.send(f"Parameters: {curr_config.get_parameters()}")

@bot.command()
async def get_config_settings(ctx, arg):
    config_to_use = find_config(arg)
    if (config_to_use is None):
        await ctx.send("No config with given name found!")
        return
    config_settings = config_to_use.get_parameters()
    await(ctx.send(config_settings))

# Use with a discord key -- key is hidden in a different file
with open("key.txt", "r", encoding="utf-8") as f:
    key = f.readline()
bot.run(key)
