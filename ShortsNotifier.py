from googleapiclient.discovery import build
from plyer import notification
import time
from datetime import datetime
import csv
import webbrowser


# Function to send a desktop notification
def send_notification(video_link: str, author: str, link: str):
    notification_title = "New Shorts Video"
    notification_message = "A new video by " + author + " is available."
    notification_timeout = 10  # Notification timeout in seconds

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=notification_timeout,
        app_name="YouTube Shorts Notifier",
        app_icon=r"cool_pepe.ico",
    )
    webbrowser.open(link)


# Load the channel IDs from a CSV file
channel_ids_csv = "channel_ids.csv"
yt_channels_and_playlists = []
with open(channel_ids_csv, "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Access the values in each row
        channel_id = row[0]
        yt_channels_and_playlists.append({"channel_id": channel_id, "playlist_id": ""})

# Get API key
API_KEY = ""
with open("API_KEY.txt", "r") as file:
    API_KEY = file.read().replace("\n", "")
youtube = build("youtube", "v3", developerKey=API_KEY)

# Get the 'uploads' playlist IDs for each channel
yt_channels = (
    youtube.channels()
    .list(
        part="contentDetails",
        id=",".join([pair["channel_id"] for pair in yt_channels_and_playlists]),
    )
    .execute()
)
for channel in yt_channels["items"]:
    playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    channel_id = channel["id"]
    for pair in yt_channels_and_playlists:
        if pair["channel_id"] == channel_id:
            pair["playlist_id"] = playlist_id
print("Playlist ID retrieval complete.")

videos_already_seen = set()
is_first_scan = True
try:
    while True:
        num_new_videos = 0
        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )  # Get current time in 24-hour format

        # For each channel, get/process the most recent video
        for playlist_id in [pair["playlist_id"] for pair in yt_channels_and_playlists]:
            channel_playlist = (
                youtube.playlistItems()
                .list(
                    part="snippet",
                    playlistId=playlist_id,
                )
                .execute()
            )
            most_recent_video = channel_playlist["items"][0]
            video_id = most_recent_video["snippet"]["resourceId"]["videoId"]
            video_title = most_recent_video["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            channel_name = most_recent_video["snippet"]["channelTitle"]
            if is_first_scan:
                videos_already_seen.add(video_id)
                print(
                    f"{current_time}: Latest video detected on startup by {channel_name}: '{video_title}' ({video_url})"
                )
            elif video_id in videos_already_seen:
                continue
            else:
                videos_already_seen.add(video_id)
                num_new_videos += 1
                print(
                    f"{current_time}: New YouTube Shorts video by {channel_name}!\nURL: {video_url}\n"
                )
                send_notification(video_url, channel_name, video_url)
        if num_new_videos == 0:
            print(f"{current_time}: No new videos found.")
        time.sleep(60)  # Wait for 60 seconds before checking again
        is_first_scan = False
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    notification_title = "ShortsNotifier Crashed"
    notification_message = "simple as."
    notification_timeout = 5  # Notification timeout in seconds

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=notification_timeout,
        app_name="YouTube Shorts Notifier",
    )
    print(e)
