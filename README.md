# Discord Bot

The discord bot provides convenient tool for syncing playing a video via discord bot. The different commands can be used for playing the video. 

## Bot commands 
- ___$save_playlist___ <playlist_url> <playlist_name> (optional)
    - Saves a playlist. Takes a few seconds and is stored by bot which can be reused even when the bot goes offline.
- ___$random_video___ <playlist_title>
    - Gets a random video from the playlist (no criteria)
- ___$random_video_with_filter___ <playlist_title> <min_length> <max_length> <min_views> <max_views> <author_name> <title_contains>, <is_favorite>
    - Type "none" for any categories to not use them. You can retrieve the last category list by using the config name "last".
- ___$add_preset___ <config_title> <min_length> <max_length> <min_views> <max_views> <author_name> <title_contains> <is_favorite>
    - Creates a new configuration for the lengths and similar features which are subsequently defaulted. 
- ___$random_video_with_filter___ <playlist_title> <config_title>
    - Gets a random video with the chosen playlist and the categories from chosen config. Use "last" keyword if config not explicitly built, but to reuse last categories.
- ___$list___
    - Help text that describes commands (this message)
- ___$add_favorite___ <playlist_title> <video_title>
    - Makes video with given title favorite in playlist with given title.
- ___$remove_favorite___ <playlist_title> <video_title>
    - Makes video no longer a favorite in playlist with given title
- ___$get_config_settings___ <config_title>
    - Lists config settings with given title.


[![Video Tutorial](https://img.youtube.com/vi/voYB8JojGAg/0.jpg)](https://www.youtube.com/watch?v=voYB8JojGAg)
