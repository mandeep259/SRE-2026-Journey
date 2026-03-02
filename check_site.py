import requests  # This is a "tool" that lets Python talk to the internet

# This is our target
url = "https://www.google.com"

try:
    # We tell Python: "Go try to grab this website"
    response = requests.get(url)

    # In SRE language, '200' means "Everything is OK!"
    if response.status_code == 200:
        print(f"✅ Success! {url} is up and running.")
    else:
        print(f"⚠️ Warning! {url} is acting weird. Status code: {response.status_code}")

except:
    # If the internet is down or the site is dead, this happens
    print(f"🚨 ALERT! {url} is DOWN! Get the coffee ready.")
