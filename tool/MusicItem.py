import csv
import random

# list of guitar brands
brands = ['Fender', 'Gibson', 'Ibanez', 'Epiphone', 'PRS', 'ESP', 'Schecter', 'Jackson']

# list of guitar types
types = ['Electric', 'Acoustic', 'Classical', 'Bass']

# list of guitar models
models = ['Stratocaster', 'Telecaster', 'Les Paul', 'SG', 'PRS Custom 24', 'JEM', 'Flying V', 'Explorer', 'Warlock']

# generate 100 dummy sales records
sales = []
for i in range(500):
    brand = random.choice(brands)
    guitar_type = random.choice(types)
    model = random.choice(models)
    price = round(random.uniform(50, 2000), 2)
    serial_num = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
    sales.append([brand, guitar_type, model, price, serial_num])

# write the sales records to a CSV file
with open('MusicItem.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Brand', 'Type', 'Model', 'Price', 'serial_num'])
    writer.writerows(sales)
