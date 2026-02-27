import os
import re
import requests
import json

FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
CATEGORY = "Home"
DAYS_RECENCY = 7
MIN_DOWNLOADS = 500

BASE_URL = "https://api.firecrawl.dev/v1"
headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

# Step 1: Scrape MakerWorld search page (JS rendered)
print(f"Scraping MakerWorld for category: {CATEGORY}...")
scrape_payload = {
    "url": f"https://makerworld.com/en/search/models?keyword={CATEGORY}",
    "formats": ["markdown"],
    "waitFor": 5000
}

response = requests.post(f"{BASE_URL}/scrape", headers=headers, json=scrape_payload, timeout=60)
response.raise_for_status()
data = response.json()
markdown = data.get("data", {}).get("markdown", "")
print(f"Scraped {len(markdown)} chars of markdown")

# Step 2: Parse models from markdown
# Pattern: [![Title](image_url)](model_url) followed by creator and stats
model_pattern = re.compile(
    r'\[!\[([^\]]*)\]\((https://makerworld\.bblmw\.com[^\)]+)\)\]'  # [![title](image)]
    r'\((https://makerworld\.com/en/models/[^\)]+)\)'                # (model_url)
    r'.*?'                                                            # stuff between
    r'\[([^\]]*)\]\(https://makerworld\.com/en/models/[^\)]+\s+"[^"]+"\)'  # [title](url "title")
    r'.*?'                                                            # stuff between
    r'([\w\s\-_.]+)\]\(https://makerworld\.com/en/@'                 # creator](profile)
    r'.*?\n\n'                                                        # rest
    r'([\d,.]+\s*k?)\n\n'                                            # first number (downloads)
    r'([\d,.]+\s*k?)',                                                # second number (likes)
    re.DOTALL
)

def parse_number(s):
    """Parse numbers like '8.7 k' -> 8700, '500' -> 500"""
    s = s.strip().lower()
    if 'k' in s:
        return int(float(s.replace('k', '').strip()) * 1000)
    return int(float(s.replace(',', '')))

models = []
for match in model_pattern.finditer(markdown):
    title = match.group(1).strip()
    image_url = match.group(2).strip()
    model_url = match.group(3).split("?")[0]  # Clean URL
    creator = match.group(5).strip().lstrip('\\').strip()
    downloads_raw = match.group(6)
    likes_raw = match.group(7)

    try:
        downloads = parse_number(downloads_raw)
        likes = parse_number(likes_raw)
    except:
        downloads = 0
        likes = 0

    models.append({
        "title": title,
        "primaryImageUrl": image_url,
        "modelUrl": model_url,
        "creatorName": creator,
        "downloads": downloads,
        "likes": likes,
        "downloads_raw": downloads_raw.strip(),
        "likes_raw": likes_raw.strip()
    })

# Step 3: Filter by minimum downloads
filtered = [m for m in models if m["downloads"] >= MIN_DOWNLOADS]

print(f"\nExtracted {len(models)} models, {len(filtered)} passed filter (>= {MIN_DOWNLOADS} downloads)")
print("\nTop models:")
for m in filtered[:5]:
    print(f"  - {m['title']} | by {m['creatorName']} | {m['downloads_raw']} downloads | {m['likes_raw']} likes")
    print(f"    URL: {m['modelUrl']}")
    print(f"    Image: {m['primaryImageUrl'][:80]}...")

# Save results
os.makedirs(".firecrawl", exist_ok=True)
with open(".firecrawl/models-home.json", "w", encoding="utf-8") as f:
    json.dump({"models": filtered, "total_found": len(models), "total_filtered": len(filtered)}, f, indent=2, ensure_ascii=False)
print(f"\nResults saved to .firecrawl/models-home.json")
