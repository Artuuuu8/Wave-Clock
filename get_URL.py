import requests

SPOT_ID = "5842041f4e65fad6a77088a6"
PAGE_URL = f"https://www.surfline.com/surf-report/terra-mar-point/{SPOT_ID}"

# GraphQL payload
GQL = {
    "operationName": "LiveCamera",
    "variables": {"spotId": SPOT_ID},
    "query": """
      query LiveCamera($spotId: ID!) {
        spot(id: $spotId) {
          liveCamera {
            streamUrl
          }
        }
      }
    """
}

# Common “real browser” headers
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": PAGE_URL,
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
}

# 1. Use a session to get any Cloudflare cookies
session = requests.Session()
r1 = session.get(PAGE_URL, headers=headers)
print("GET status:", r1.status_code)
print("Cookies after GET:", session.cookies.get_dict())

# 2. Fire off the GraphQL query
r2 = session.post(
    "https://www.surfline.com/graphql",
    json=GQL,
    headers=headers
)
print("POST status:", r2.status_code)
print("Response headers:", r2.headers.get("Content-Type"))
print("Response snippet:", r2.text[:500])  # first 500 chars

# 3. Only if it looks like JSON, parse it
try:
    data = r2.json()
    hls_url = data["data"]["spot"]["liveCamera"]["streamUrl"]
    print("Found HLS URL:", hls_url)
except ValueError:
    print("❌ Not valid JSON. Check the snippet above for clues.")
except KeyError:
    print("❌ JSON parsed but no streamUrl field—schema may have changed.")
