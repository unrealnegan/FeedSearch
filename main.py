import feedparser
from datetime import datetime

# Schlagwörter
KEYWORDS = ["Trump", "USA", "Biden", "Demokraten", "Republikaner", "Grönland"]

RSS_FEEDS = {
    "Netzpolitik": "https://netzpolitik.org/feed/",
    "Tagesschau": "https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml",
    "BR24": "https://nachrichtenfeeds.br.de/rss/nachrichten/seiten/QXAPkQJ",
    "Welt": "https://www.welt.de/feeds/latest.rss",
    "Der Spiegel": "https://www.spiegel.de/index.rss",
    "FAZ": "https://www.faz.net/rss/aktuell/",
    "Die Zeit": "https://newsfeed.zeit.de/index",
}

COLORS = {
    "Netzpolitik": "\033[95m",
    "Tagesschau": "\033[91m",
    "BR24": "\033[92m",
    "Welt": "\033[93m",
    "Der Spiegel": "\033[94m",
    "FAZ": "\033[96m",
    "Die Zeit": "\033[97m",
}

RESET = "\033[0m"


def extract_date(entry):
    """Gibt (anzeige_string, datetime_objekt) zurück."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6])
    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
        dt = datetime(*entry.updated_parsed[:6])
    else:
        return "Unbekanntes Datum", datetime.min  

    return dt.strftime("%d.%m.%Y %H:%M"), dt


def search_news(keywords):
    results = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            text = f"{entry.title} {entry.get('summary', '')}".lower()
            if any(k.lower() in text for k in keywords):
                date_str, date_obj = extract_date(entry)

                results.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "date": date_str,
                    "date_obj": date_obj
                })

    results.sort(key=lambda x: x["date_obj"], reverse=True)

    return results


if __name__ == "__main__":
    print(f"🔍 Suche nach Schlagwörtern: {', '.join(KEYWORDS)}")
    print("=" * 105)

    articles = search_news(KEYWORDS)
    print(f"✅ Gefundene Artikel: {len(articles)}\n")

    if not articles:
        print("Keine passenden Artikel gefunden.")
    else:
        for a in articles:
            color = COLORS.get(a["source"], "")
            print(f"{color}[{a['source']}] {a['title']}{RESET}")
            print(f"{color}📅 Veröffentlicht: {a['date']}{RESET}")
            print(f"{color}{a['link']}{RESET}")
            print("-" * 60)
