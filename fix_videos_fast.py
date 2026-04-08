import os
import urllib.request

print("Fixing videos quickly...")
downloaded = 0
for root, dirs, files in os.walk('.'):
    # Only process actual video formats to avoid tracking pixels
    for file in files:
        if file.endswith(('.mp4', '.webm', '.ogg', '.mp3', '.m4a')):
            filepath = os.path.join(root, file)
            if os.path.getsize(filepath) < 2048: # Dummy files are tiny
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read(500)
                    if content.startswith('No Content:'):
                        url = content.split('No Content:')[1].strip()
                        print(f"Downloading {file} from {url}")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=30) as response, open(filepath, 'wb') as out_file:
                            out_file.write(response.read())
                        print("Done.")
                        downloaded += 1
                except Exception as e:
                    pass
print(f"Fixed {downloaded} video files!")
