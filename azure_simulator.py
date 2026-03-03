# 1. THE DATA (Our Ingredients)
fake_azure_data = [
    {"name": "Production-Web-RG", "location": "East US", "cost": 500},
    {"name": "Staging-App-RG", "location": "West Europe", "cost": 200},
    {"name": "Legacy-DB-RG", "location": "Central India", "cost": 0},
    {"name": "Testing-Zombie-RG", "location": "East US", "cost": 50}
]

# 2. THE BUCKETS (We set these to zero before we start)
total_bill = 0
production_count = 0

print("🔍 STARTING SRE ANALYSIS...")

# 3. THE LOOP (The Manager walking through the list)
for resource in fake_azure_data:
    
    # --- STEP A: Calculate Total Bill ---
    # We add the current cost to our bucket
    total_bill = total_bill + resource['cost']

    # --- STEP B: Filter by Location ---
    if resource['location'] == "East US":
        print(f"📍 Found East US Resource: {resource['name']}")

    # --- STEP C: Search for 'Production' ---
    if "Production" in resource['name']:
        # If we find the word, we add 1 to our count bucket
        production_count = production_count + 1

# 4. THE FINAL REPORT (After the manager finishes walking)
print("------------------------------")
print(f"💰 Total Cloud Cost: ${total_bill}")
print(f"🏢 Total Production Environments: {production_count}")
print("✅ ANALYSIS COMPLETE.")
