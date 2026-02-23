import subprocess
import os

CHANNELS = [
    ("ARY News", "Pakistan | News", "https://www.youtube.com/@arynews/live"),
    ("Geo News", "Pakistan | News", "https://www.youtube.com/@geonews/live"),
    ("Dunya News", "Pakistan | News", "https://www.youtube.com/@DunyaNewsOfficial/live"),
    ("Samaa TV", "Pakistan | News", "https://www.youtube.com/@Samaatv/live"),
    ("92 News HD", "Pakistan | News", "https://www.youtube.com/@92newschannel/live"),
    ("ARY QTV", "Pakistan | Islamic", "https://www.youtube.com/@aryqtvofficial/live"),
    ("Madani Channel", "Pakistan | Islamic", "https://www.youtube.com/@madanichannel/live"),
    ("Hum TV", "Pakistan | Entertainment", "https://www.youtube.com/@HUMTV/live"),
    ("ARY Digital", "Pakistan | Entertainment", "https://www.youtube.com/@arydigitalasia/live"),
]

def get_hls(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", url],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")[0]
    except:
        return None
    return None

def main():
    lines = ["#EXTM3U"]

    for name, group, url in CHANNELS:
        print(f"Extracting {name}...")
        hls = get_hls(url)

        if not hls:
            print("  ❌ Not live or failed")
            continue

        lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
        lines.append(hls)
        print("  ✅ Added")

    os.makedirs("playlists", exist_ok=True)

    with open("playlists/pakistan_major.m3u", "w") as f:
        f.write("\n".join(lines))

    print("Playlist built.")

if __name__ == "__main__":
    main()
