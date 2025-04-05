import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Setup
fake = Faker()
Faker.seed(42)
random.seed(42)

drivers = ['Raju', 'Suresh', 'Manoj', 'Kiran', 'Teja']
statuses = ['Delivered', 'Pending', 'Canceled', 'Failed']

# Generate sample data
data = []
start_date = datetime(2025, 4, 1)

for i in range(1, 51):
    delivery_date = start_date + timedelta(days=random.randint(0, 4))
    status = random.choices(statuses, weights=[0.7, 0.2, 0.05, 0.05])[0]
    delivery_time = fake.time() if status == 'Delivered' else ''
    driver = random.choice(drivers) if status == 'Delivered' else ''
    liters = random.choice([20, 50, 100, 200])
    revenue = liters * 3 if status == 'Delivered' else 0

    data.append({
        'Delivery_ID': f'D{i:03}',
        'Date': delivery_date.strftime('%Y-%m-%d'),
        'Customer_Name': fake.company(),
        'Address': fake.address().replace("\n", ", "),
        'Liters': liters,
        'Status': status,
        'Delivery_Time': delivery_time,
        'Driver_Name': driver,
        'Revenue': revenue
    })

df = pd.DataFrame(data)

# ---- CLEANING ----
# Strip text columns
df['Customer_Name'] = df['Customer_Name'].str.strip()
df['Address'] = df['Address'].str.strip()
df['Status'] = df['Status'].str.strip()
df['Driver_Name'] = df['Driver_Name'].str.strip()

# Replace empty strings with NaN
df.replace("", pd.NA, inplace=True)

# Remove rows where delivery failed or canceled
df = df[~df['Status'].isin(['Canceled', 'Failed'])]

# Save cleaned file
df.to_excel("cleaned_water_delivery_data.xlsx", index=False)
print("Cleaned data exported successfully!")
