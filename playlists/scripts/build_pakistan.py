import requests
import re
import json
import os

USER_AGENT = {"User-Agent": "Mozilla/5.0"}

def validate_stream(url, headers=None):
    try:
        r = requests.get(url, headers=headers or USER_AGENT, timeout=10)
        return r.status_code == 200
    except:
        return False

def extract_stream(channel):
    try:
        r = requests.get(channel["page"], headers=USER_AGENT, timeout=15)
        match = re.search(channel["pattern"], r.text)
        if match:
            return match.group(0)
    except:
        return None

def main():
    with open("scripts/channels_pakistan.json") as f:
        channels = json.load(f)

    lines = ["#EXTM3U"]

    for ch in channels:
        print(f"Checking {ch['name']}")
        stream = extract_stream(ch)

        if not stream:
            print("  ❌ No stream found")
            continue

        headers = ch.get("headers", {})

        if not validate_stream(stream, headers):
            print("  ❌ Invalid stream")
            continue

        header_string = ""
        if headers:
            header_string = "|" + "&".join(
                f"{k}={v}" for k, v in headers.items()
            )

        lines.append(
            f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}'
        )
        lines.append(stream + header_string)

        print("  ✅ Added")

    os.makedirs("playlists", exist_ok=True)

    with open("playlists/pakistan_full.m3u", "w") as f:
        f.write("\n".join(lines))

    print("Pakistan playlist built.")

if __name__ == "__main__":
    main()
