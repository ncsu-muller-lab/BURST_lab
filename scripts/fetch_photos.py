import os
import re
import urllib.request

URL = "https://muller.wordpress.ncsu.edu/people/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Target file names to save into assets/img/
NAME_MAP = {
    "sashank": "sashank-gautam.jpg",
    "gautam": "sashank-gautam.jpg",
    "shahriar": "shahriar-chowdhury.jpg",
    "chowdhury": "shahriar-chowdhury.jpg",
    "aniket": "aniket-beldar.jpg",
    "beldar": "aniket-beldar.jpg",
    "parniyan": "parniyan-norouzzadeh.jpg",
    "norouzzadeh": "parniyan-norouzzadeh.jpg",
    "hossein": "hossein-ahmadian.jpg",
    "ahmadian": "hossein-ahmadian.jpg",
    "caleb": "caleb-moore.jpg",
    "moore": "caleb-moore.jpg",
}

def main():
    os.makedirs("assets/img", exist_ok=True)
    req = urllib.request.Request(URL, headers=HEADERS)
    html = urllib.request.urlopen(req).read().decode("utf-8")

    # Find all image URLs from the WordPress page
    img_urls = re.findall(r'<img[^>]+src=["\'](https?://[^"\']+)["\']', html)
    print(f"Found {len(img_urls)} total images on WordPress.")

    downloaded = set()
    for src in img_urls:
        src_lower = src.lower()
        for key, target_filename in NAME_MAP.items():
            if key in src_lower and target_filename not in downloaded:
                target_path = os.path.join("assets", "img", target_filename)
                print(f"Downloading {key} -> {target_path} ...")
                try:
                    img_data = urllib.request.urlopen(urllib.request.Request(src, headers=HEADERS)).read()
                    with open(target_path, "wb") as f:
                        f.write(img_data)
                    downloaded.add(target_filename)
                except Exception as e:
                    print(f"Failed to download {src}: {e}")

    print(f"\nDone! Downloaded {len(downloaded)} member photos into assets/img/.")

if __name__ == "__main__":
    main()
