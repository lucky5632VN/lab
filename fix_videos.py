import os
import urllib.request

print("Scanning for 'No Content' dummy files...")
downloaded_count = 0

for root, dirs, files in os.walk('.'):
    for file in files:
        filepath = os.path.join(root, file)
        # Only check small files (under 1KB) to avoid reading large binaries
        if os.path.getsize(filepath) < 1024:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                if content.startswith('No Content:'):
                    url = content.split('No Content:')[1].strip()
                    print(f"Found dummy: {filepath}")
                    print(f"Downloading real file: {url}")
                    
                    # Prevent timeout
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=30) as response, open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
                    downloaded_count += 1
                    print("Success!")
            except Exception as e:
                pass

print(f"All done! Replaced {downloaded_count} dummy files with real media.")
