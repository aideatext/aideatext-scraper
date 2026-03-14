import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime

SOURCES = {
    "funds": [
        "https://www.sbir.gov/opportunities",
        "https://eic.ec.europa.eu/eic-funding-opportunities_en",
        "https://www.grants.gov/search-grants?oppStatuses=forecasted%7Cposted&sortBy=openDate%7Cdesc"
    ],
    "call4paper": [
        "https://www.wikicfp.com/cfp/call?conference=education",
        "https://www.wikicfp.com/cfp/call?conference=learning",
        "https://www.wikicfp.com/cfp/call?conference=edtech",
        "https://www.cfplist.com/search?q=education+digital",
        "https://callsforpapers.org/category/education/"
    ],
    "communities": [
        "https://www.freelists.org/search?q=education+digital",
        "https://www.freelists.org/search?q=learning+digital+technology",
        "https://groups.io/search?q=education+digital+learning"
    ]
}

def scrape_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AIdeaTextBot/1.0)"}
        r = requests.get(url, timeout=15, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        results = []
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href  = a["href"]
            if len(title) > 10:
                full_url = href if href.startswith("http") else f"https://{url.split('/')[2]}{href}"
                results.append({
                    "title": title,
                    "url": full_url,
                    "source": url,
                    "scraped_at": datetime.utcnow().isoformat()
                })
        return results[:50]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def run(category):
    urls = SOURCES.get(category, [])
    if not urls:
        print(f"⚠️ Categoría '{category}' no encontrada")
        print(f"Categorías disponibles: {list(SOURCES.keys())}")
        sys.exit(1)
    
    all_results = []
    for url in urls:
        print(f"Scraping: {url}")
        results = scrape_url(url)
        all_results.extend(results)
        print(f"  → {len(results)} items")
    
    output = f"data/{category}.json"
    with open(output, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(all_results)} items guardados en {output}")

if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "funds"
    run(category)
