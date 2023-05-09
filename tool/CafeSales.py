import random
import csv

# crete a script that generates 100 dummy records for the cafe_SALES table

"""
CREATE TABLE IF NOT EXISTS CAFE_SALES (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
CafeItemID INTEGER(8),
CustomerID INTEGER(8),
count INTEGER(8),
date TEXT(10),
FOREIGN KEY(CafeItemID) REFERENCES CAFE_ITEM(ID),
FOREIGN KEY(CustomerID) REFERENCES CUSTOMER(ID)
)
"""

cafe_item_ids = [f'{i}' for i in range(1, 500)]
customer_ids = [f'{i}' for i in range(1, 500)]

def generate_date():
    year = random.randint(2018, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

# generate 100 dummy records
records = []
for i in range(1000):
    count = random.randint(1, 10)
    date = generate_date()
    records.append([random.choice(cafe_item_ids), random.choice(customer_ids), count, date])

# write data to a CSV file
with open("CafeSales.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["CafeItemID", "CustomerID",  "count", "date"])
    writer.writerows(records)
