import subprocess
import os
import json
import datetime

OUTPUT_FILE = "playlists/youtube-pakistan.m3u"
GROUP_NAME = "Pakistan Live"

def get_live_stream(url):
    try:
        # Get JSON metadata
        result = subprocess.run(
            ["yt-dlp", "-J", url],
            capture_output=True,
            text=True,
            timeout=90
        )

        if not result.stdout:
            return None

        data = json.loads(result.stdout)

        # If not live, skip
        if data.get("is_live") is not True:
            return None

        # Extract HLS URL directly
        formats = data.get("formats", [])

        for f in formats:
            if f.get("protocol") == "m3u8_native":
                return f.get("url")

        return None

    except Exception:
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

    for url in channels:
        name = extract_name(url)
        print(f"Checking: {name}")

        stream = get_live_stream(url)

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
            print(f"Offline: {name}")

    os.makedirs("playlists", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("Total added:", added)
    print("Updated at:", datetime.datetime.utcnow())


if __name__ == "__main__":
    main()
