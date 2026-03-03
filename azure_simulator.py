fake_azure_data = [
    {"name": "Production-Web-RG", "location": "East US", "cost": 500},
    {"name": "Staging-App-RG", "location": "West Europe", "cost": 200},
    {"name": "Legacy-DB-RG", "location": "Central India", "cost": 0},
    {"name": "Testing-Zombie-RG", "location": "East US", "cost": 50}
]

total_bill = 0
india_count = 0

print("🔍 STARTING SRE ANALYSIS...")

for resource in fake_azure_data:
    
    # 1. THE PRICE HIKE LOGIC: Only add to bill if cost is 100 or more
    if resource['cost'] >= 100:
        total_bill = total_bill + resource['cost']

    # 2. THE INDIA COUNT: Count how many are in Central India
    if resource['location'] == "Central India":
        india_count = india_count + 1

print("------------------------------")
print(f"💰 Total High-Cost Bill: ${total_bill}") # Should be 700 (500 + 200)
print(f"🇮🇳 Resources in India: {india_count}")
print("✅ ANALYSIS COMPLETE.")
