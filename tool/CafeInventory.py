import random
import csv

cafe_item_ids = [i for i in range(1, 500)]

def generate_date(min, max):
    year = random.randint(min, max)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

# generate 100 dummy records
records = []
for i in range(500):
    count = random.randint(1, 15)
    date = generate_date(2018, 2022)
    records.append([random.choice(cafe_item_ids), count, date])

# write data to a CSV file
with open("CafeInventory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["CafeItemID", "count", "date"])
    writer.writerows(records)
