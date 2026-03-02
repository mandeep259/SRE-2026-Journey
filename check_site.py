import requests # This is a "tool" that lets Python talk to the internet

# This is our target
#url = "https://www.google.com"

# LAYER: The List (A tray of multiple websites)
sites_to_check = ["https://www.google.com", "https://www.github.com", "https://this-site-is-fake.com"]

# LAYER: The Function (The Recipe for checking a site)
def check_my_website(site_url):
    try:        # We tell Python: "Go try to grab this website"
        response = requests.get(site_url, timeout=5)
        # In SRE language, '200' means "Everything is OK!"
        if response.status_code == 200:
            print(f"✅ {site_url} is healthy!")
        else:
            print(f"⚠️ {site_url} returned a code: {response.status_code}")
    except:
        print(f"🚨 {site_url} is NOT reachable!") # If the internet is down or the site is dead, this happens

# LAYER: The Loop (The Manager doing the task for every site)
print("--- SRE DAILY HEALTH CHECK STARTING ---")

for site in sites_to_check:
    check_my_website(site)

print("--- CHECK COMPLETE ---")
