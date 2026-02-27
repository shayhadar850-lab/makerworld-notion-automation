"""
MakerWorld -> Notion Automation Brain
Scrapes MakerWorld, parses 3D models, deduplicates against Notion, and syncs new entries.
Uses Firecrawl /v1/scrape (1 credit per category) + Notion API.

Usage:
  set FIRECRAWL_API_KEY=fc-xxxxx
  set NOTION_API_KEY=ntn_xxxxx
  python makerworld_brain.py
"""
import os
import re
import sys
import json
import time
import requests

# ============================================================
# CONFIGURATION
# ============================================================
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_DATABASE_ID = "192c8ff8-b6a1-4580-9dcb-bc214490a2a7"

CATEGORIES = ["Home"]  # Add more: "Office", "Art", "Tools", "Household"
MIN_DOWNLOADS = 500
WAIT_FOR_JS = 5000  # ms to wait for JS rendering

FIRECRAWL_BASE = "https://api.firecrawl.dev/v1"
NOTION_BASE = "https://api.notion.com/v1"

# ============================================================
# API HEADERS
# ============================================================
firecrawl_headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

notion_headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ============================================================
# STEP 1: SCRAPE MAKERWORLD (1 credit per category)
# ============================================================
def scrape_makerworld(category):
    """Scrape MakerWorld search page and return markdown content."""
    print(f"\n{'='*60}")
    print(f"[SCRAPE] Category: {category}")
    print(f"{'='*60}")

    payload = {
        "url": f"https://makerworld.com/en/search/models?keyword={category}",
        "formats": ["markdown"],
        "waitFor": WAIT_FOR_JS
    }

    response = requests.post(
        f"{FIRECRAWL_BASE}/scrape",
        headers=firecrawl_headers,
        json=payload,
        timeout=90
    )
    response.raise_for_status()
    markdown = response.json().get("data", {}).get("markdown", "")
    print(f"  Scraped {len(markdown)} chars")
    return markdown

# ============================================================
# STEP 2: PARSE MODELS FROM MARKDOWN
# ============================================================
MODEL_PATTERN = re.compile(
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

def parse_number(s):
    """Parse '8.7 k' -> 8700, '500' -> 500"""
    s = s.strip().lower()
    if 'k' in s:
        return int(float(s.replace('k', '').strip()) * 1000)
    return int(float(s.replace(',', '')))

def parse_models(markdown, category):
    """Extract model data from scraped markdown."""
    models = []
    for match in MODEL_PATTERN.finditer(markdown):
        title = match.group(1).strip()
        image_url = match.group(2).strip()
        model_url = match.group(3).split("?")[0]
        creator = match.group(5).strip().lstrip('\\').strip()

        try:
            downloads = parse_number(match.group(6))
            likes = parse_number(match.group(7))
        except (ValueError, AttributeError):
            downloads = 0
            likes = 0

        models.append({
            "title": title,
            "primaryImageUrl": image_url,
            "modelUrl": model_url,
            "creatorName": creator,
            "downloads": downloads,
            "likes": likes,
            "category": category
        })

    print(f"  [PARSE] Found {len(models)} models")
    return models

# ============================================================
# STEP 3: FILTER
# ============================================================
def filter_models(models):
    """Apply minimum download threshold."""
    filtered = [m for m in models if m["downloads"] >= MIN_DOWNLOADS]
    print(f"  [FILTER] {len(filtered)}/{len(models)} passed (>= {MIN_DOWNLOADS} downloads)")
    return filtered

# ============================================================
# STEP 4: NOTION DEDUPLICATION (by Source Link URL)
# ============================================================
def get_existing_urls():
    """Query Notion database and return set of existing Source Link URLs."""
    print(f"\n[DEDUP] Fetching existing entries from Notion...")
    existing = set()
    has_more = True
    start_cursor = None

    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(
            f"{NOTION_BASE}/databases/{NOTION_DATABASE_ID}/query",
            headers=notion_headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        for page in data.get("results", []):
            url_prop = page.get("properties", {}).get("Source Link", {})
            url_val = url_prop.get("url")
            if url_val:
                existing.add(url_val)

        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    print(f"  Found {len(existing)} existing entries in Notion")
    return existing

def deduplicate(models, existing_urls):
    """Remove models that already exist in Notion."""
    new_models = [m for m in models if m["modelUrl"] not in existing_urls]
    skipped = len(models) - len(new_models)
    print(f"  [DEDUP] {len(new_models)} new, {skipped} already in Notion")
    return new_models

# ============================================================
# STEP 5: CREATE NOTION PAGES
# ============================================================
def create_notion_page(model):
    """Create a single Notion page with properties + embedded product image."""
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "cover": {
            "type": "external",
            "external": {"url": model["primaryImageUrl"]}
        },
        "properties": {
            "Model Name": {
                "title": [{"text": {"content": model["title"]}}]
            },
            "Source Link": {
                "url": model["modelUrl"]
            },
            "Designer": {
                "rich_text": [{"text": {"content": model["creatorName"]}}]
            },
            "Downloads": {
                "number": model["downloads"]
            },
            "Likes": {
                "number": model["likes"]
            },
            "Category": {
                "select": {"name": model["category"]}
            },
            "Status": {
                "status": {"name": "\u05d7\u05d3\u05e9"}  # חדש
            }
        },
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": model["primaryImageUrl"]}
                }
            }
        ]
    }

    response = requests.post(
        f"{NOTION_BASE}/pages",
        headers=notion_headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def sync_to_notion(models):
    """Create Notion pages for all new models."""
    print(f"\n[SYNC] Creating {len(models)} new Notion pages...")
    created = 0
    errors = 0

    for model in models:
        try:
            create_notion_page(model)
            created += 1
            print(f"  [{created}/{len(models)}] {model['title']}")
            time.sleep(0.35)  # Notion rate limit: ~3 req/sec
        except requests.exceptions.HTTPError as e:
            errors += 1
            print(f"  [ERROR] {model['title']}: {e}")
            if e.response and e.response.status_code == 429:
                print("  Rate limited! Waiting 10s...")
                time.sleep(10)

    print(f"\n[DONE] Created: {created}, Errors: {errors}")
    return created, errors

# ============================================================
# MAIN PIPELINE
# ============================================================
def run():
    print("=" * 60)
    print("  MakerWorld -> Notion Automation Brain")
    print("=" * 60)

    if not NOTION_API_KEY:
        print("\n[ERROR] Set NOTION_API_KEY environment variable.")
        print("  1. Create integration: https://www.notion.so/my-integrations")
        print("  2. Share the database with your integration")
        print("  3. Run: set NOTION_API_KEY=ntn_xxxxx && python makerworld_brain.py")
        sys.exit(1)

    # Collect models from all categories
    all_models = []
    for category in CATEGORIES:
        markdown = scrape_makerworld(category)
        models = parse_models(markdown, category)
        filtered = filter_models(models)
        all_models.extend(filtered)

    print(f"\n[TOTAL] {len(all_models)} models across {len(CATEGORIES)} categories")

    if not all_models:
        print("[DONE] No models found!")
        return

    # Deduplicate against Notion
    existing_urls = get_existing_urls()
    new_models = deduplicate(all_models, existing_urls)

    if not new_models:
        print("\n[DONE] No new models to add - all already in Notion!")
        return

    # Sync to Notion
    created, errors = sync_to_notion(new_models)

    # Save run log
    os.makedirs(".firecrawl", exist_ok=True)
    log = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "categories": CATEGORIES,
        "total_scraped": len(all_models),
        "new_added": created,
        "errors": errors,
        "models": [{"title": m["title"], "url": m["modelUrl"]} for m in new_models]
    }
    with open(".firecrawl/run-log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    print(f"\nRun log saved to .firecrawl/run-log.json")

if __name__ == "__main__":
    run()
