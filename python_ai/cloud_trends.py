import urllib.request, json, sys

def fetch_live_global_trends():
    # Fetching real, unlimited data from multiple global sectors
    urls = {
        "Global_Mainstream": "https://itunes.apple.com/us/rss/topsongs/limit=15/json",
        "India_Regional": "https://itunes.apple.com/in/rss/topsongs/limit=15/json",
        "Electronic_Dance": "https://itunes.apple.com/us/rss/topsongs/genre=17/limit=10/json"
    }
    
    trends_matrix = {"status": "success", "platforms": {}}
    
    for region, url in urls.items():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                # Extract the unique genres dominating right now
                genres = [entry['category']['attributes']['label'] for entry in data['feed']['entry']]
                trends_matrix["platforms"][region] = list(set(genres))
        except:
            trends_matrix["platforms"][region] = ["Data Unavailable"]

    sys.stdout.write(json.dumps(trends_matrix))

if __name__ == "__main__":
    fetch_live_global_trends()