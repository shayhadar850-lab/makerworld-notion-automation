import re, json

with open('.firecrawl/home-decor-trending.md', 'r', encoding='utf-8') as f:
    markdown = f.read()

pattern = re.compile(
    r'\[!\[([^\]]*)\]\((https://makerworld\.bblmw\.com[^\)]+)\)\]'
    r'\((https://makerworld\.com/en/models/[^\)]+)\)'
    r'.*?'
    r'\[([^\]]*)\]\(https://makerworld\.com/en/models/[^\)]+\s+"[^"]+"\)'
    r'.*?'
    r'([\w\s\-_.]+)\]\(https://makerworld\.com/en/@'
    r'.*?\n\n'
    r'([\d,.]+\s*k?)\n\n'
    r'([\d,.]+\s*k?)',
    re.DOTALL
)

models = []
for m in pattern.finditer(markdown):
    title = m.group(1).strip()
    img = m.group(2).strip()
    url = m.group(3).split('?')[0]
    creator = m.group(5).strip().strip('\\').strip()
    dl = m.group(6).strip()
    lk = m.group(7).strip()
    models.append({'title': title, 'img': img, 'url': url, 'creator': creator, 'dl': dl, 'lk': lk})

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print(f'Found {len(models)} trending home decor models:\n')
for i, m in enumerate(models):
    print(f'{i+1}. {m["title"]}')
    print(f'   Creator: {m["creator"]} | DL: {m["dl"]} | Likes: {m["lk"]}')
    print(f'   URL: {m["url"]}')
    print()

with open('.firecrawl/trending-parsed.json', 'w', encoding='utf-8') as f:
    json.dump(models, f, indent=2, ensure_ascii=False)
