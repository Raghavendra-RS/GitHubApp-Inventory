import requests
import csv
import time
import os
from dotenv import load_dotenv

# Load token and org from .env
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_NAME = os.getenv('ORG_NAME')

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

BASE_URL = f"https://api.github.com/orgs/{ORG_NAME}/installations"
CSV_FILE = "github_apps.csv"

def handle_rate_limit(response):
    if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
        remaining = int(response.headers.get('X-RateLimit-Remaining'))
        if remaining == 0:
            reset_time = int(response.headers.get('X-RateLimit-Reset'))
            wait_time = reset_time - int(time.time())
            print(f"Rate limit exceeded. Sleeping for {wait_time + 5} seconds.")
            time.sleep(wait_time + 5)

def fetch_all_apps():
    all_apps = []
    page = 1
    per_page = 100

    while True:
        url = f"{BASE_URL}?per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)

        handle_rate_limit(response)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code} - {response.text}")
            break

        data = response.json()
        installations = data.get("installations", [])

        if not installations:
            break

        for app in installations:
            all_apps.append({
                "App Name": app["app_slug"],
                "App ID": app["app_id"],
                "Target Type": app["target_type"],
            })

        page += 1

    return all_apps

def write_to_csv(apps, filename):
    if not apps:
        print("No apps found.")
        return

    keys = apps[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(apps)

    print(f"Data written to {filename}")

if __name__ == "__main__":
    print("Fetching GitHub Apps...")
    apps = fetch_all_apps()
    write_to_csv(apps, CSV_FILE)
