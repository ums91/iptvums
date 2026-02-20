import subprocess
import os
import json
import datetime
import re

OUTPUT_FILE = "playlists/youtube-pakistan.m3u"
GROUP_NAME = "Pakistan Live"


def resolve_live_video(channel_live_url):
    try:
        # Ask yt-dlp for flat list of live tab
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "-J", channel_live_url],
            capture_output=True,
            text=True,
            timeout=90
        )

        if not result.stdout:
            return None

        data = json.loads(result.stdout)

        entries = data.get("entries", [])
        if not entries:
            return None

        video_id = entries[0].get("id")
        if not video_id:
            return None

        return f"https://www.youtube.com/watch?v={video_id}"

    except:
        return None


def extract_stream(video_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "-f", "best[protocol=m3u8]", video_url],
            capture_output=True,
            text=True,
            timeout=90
        )

        stream = result.stdout.strip()

        if "googlevideo.com" in stream:
            return stream

        return None

    except:
        return None


def extract_name(url):
    try:
        return url.split("@")[1].split("/")[0]
    except:
        return "LiveChannel"


def main():
    playlist = "#EXTM3U\n"
    added = 0

    if not os.path.exists("channels.txt"):
        print("channels.txt missing")
        return

    with open("channels.txt", "r") as f:
        channels = [line.strip() for line in f if line.strip()]

    for channel_url in channels:
        name = extract_name(channel_url)
        print(f"Resolving: {name}")

        video_url = resolve_live_video(channel_url)

        if not video_url:
            print(f"No live video: {name}")
            continue

        stream = extract_stream(video_url)

        if stream:
            playlist += (
                f'#EXTINF:-1 tvg-id="{name}" '
                f'tvg-name="{name}" '
                f'group-title="{GROUP_NAME}",{name}\n'
            )
            playlist += stream + "\n"
            print(f"Added: {name}")
            added += 1
        else:
            print(f"Stream extraction failed: {name}")

    os.makedirs("playlists", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("Total live channels added:", added)
    print("Updated at:", datetime.datetime.utcnow())


if __name__ == "__main__":
    main()
