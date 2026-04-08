import json
import os

path = r"e:\project\hoa\lab\config\languages\vi\config.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean(text):
    text = text.replace("BASF Virtual Lab", "Hệ thống A1K50")
    text = text.replace("Phòng thí nghiệm ảo BASF", "Hệ thống A1K50")
    text = text.replace("BASF Kids' Lab", "A1K50 Lab")
    text = text.replace("BASF", "Hồ Hoàng Anh")
    text = text.replace("Tiến sĩ Bong Bóng", "Trợ lý AI")
    text = text.replace("Tiến Sĩ Bong Bóng", "Trợ lý AI")
    text = text.replace("Tiến sĩ", "Trợ lý AI")
    text = text.replace("bong bóng", "Hệ thống")
    text = text.replace("Bong Bóng", "Hệ thống")
    text = text.replace("phòng thí nghiệm ảo", "phòng mô phỏng A1K50")
    text = text.replace("Phòng thí nghiệm ảo", "Phòng mô phỏng A1K50")
    return text

def traverse(d):
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = clean(v)
        elif isinstance(v, dict):
            traverse(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], str):
                    v[i] = clean(v[i])
                elif isinstance(v[i], dict):
                    traverse(v[i])

traverse(data)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Text scrub completed successfully!")
