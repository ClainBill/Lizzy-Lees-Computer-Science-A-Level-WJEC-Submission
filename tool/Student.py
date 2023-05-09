import csv
import random

forenames = ["Aneirin", "Branwen", "Cadell", "Dyfan", "Eira", "Ffion", "Gethin", "Haf", "Iestyn", "Llio", "Mabon", "Nia", "Owain", "Rhian", "Sioned", "Tegan", "Urien", "Wyn", "Ynyr", "Zara"]
surnames = ["Ap Dafydd", "Bevan", "Ceredig", "Davies", "Edwards", "Fychan", "Griffiths", "Howells", "Iorwerth", "Jenkins", "Khan", "Lloyd", "Morgan", "Neville", "Owen", "Price", "Roberts", "Stephens", "Thomas", "Williams"]
towns = ["Holyhead", "Llangefni", "Amlwch", "Menai Bridge", "Benllech", "Beaumaris", "Gaerwen", "Llanfairpwllgwyngyll", "Pentraeth", "Rhosneigr"]
counties = ["Anglesey", "Gwynedd", "Conwy"]

def generate_phone_number():
    phone_number = "0" + str(random.randint(7, 9))
    for i in range(9):
        phone_number += str(random.randint(0, 9))
    return phone_number

def generate_date():
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

def generate_dummy_data(num_records):
    with open("Students.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["username", "password", "forename", "surname", "sex", "title", "birthdate", "town", "county", "postcode", "phone_num", "guardian_phone_num", "email"])
        for i in range(num_records):
            username = random.choice(forenames) + str(random.randint(100, 999))
            password = "P@ssw0rd" + str(random.randint(100, 999))
            forename = random.choice(forenames)
            surname = random.choice(surnames)
            sex = random.choice(["M", "F"])
            title = random.choice(["Mr", "Mrs", "Miss", "Ms"])
            birthdate = generate_date()
            hire_date = generate_date()
            town = random.choice(towns)
            county = random.choice(counties)
            postcode = "LL77 " + str(random.randint(0, 9)) + str(random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "J", "L", "N", "P", "Q", "R", "S", "T", "U", "W", "X", "Y"]) + random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "J", "L", "N", "P", "Q", "R", "S", "T", "U", "W", "X", "Y"]))
            phone_num = str(generate_phone_number())
            guardian_phone_num = str(generate_phone_number())
            email = forename.lower() + "." + surname.lower() + "@example.com"
            writer.writerow([username, password, forename, surname, sex, title, birthdate, town, county, postcode, phone_num, guardian_phone_num, email])

generate_dummy_data(120)
