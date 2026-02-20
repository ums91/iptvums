import subprocess
import os
import datetime

OUTPUT_FILE = "playlists/youtube-pakistan.m3u"
GROUP_NAME = "Pakistan Live"


def extract_stream(url):
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-f", "best[protocol=m3u8]",
                "-g",
                "--no-warnings",
                "--live-from-start",
                url
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        stream = result.stdout.strip()

        if "googlevideo.com" in stream:
            return stream

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

        stream = extract_stream(url)

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
            print(f"Offline or not live: {name}")

    os.makedirs("playlists", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("Total live channels added:", added)
    print("Updated at:", datetime.datetime.utcnow())


if __name__ == "__main__":
    main()
