import json
import re

json_path = "config/languages/vi/config.json"
html_path = "index.html"

# Load JSON translations
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        texts = config.get("text", {})
except Exception as e:
    print(f"Error reading JSON: {e}")
    exit(1)

# Read HTML file
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace tags like [% trans('key') %]
def replacer(match):
    key = match.group(1)
    if key in texts:
        return texts[key]
    else:
        print(f"Warning: translation missing for key '{key}'")
        return match.group(0) # leave as is

new_html = re.sub(r'\[%\s*trans\(\'([^\']+)\'\)\s*%\]', replacer, html_content)

# Write back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Translation applied successfully to index.html!")
