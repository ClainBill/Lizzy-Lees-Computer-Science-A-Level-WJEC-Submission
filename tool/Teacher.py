import csv
import random
import string

# Define the headers for the CSV file
headers = ['username', 'password', 'forename', 'surname', 'sex', 'title', 'birthdate', 'hire_date', 'town', 'county', 'postcode', 'phone_number', 'email']

# Define some arrays for generating random data
welsh_forenames = ['Aled', 'Bryn', 'Carys', 'Dafydd', 'Elin', 'Ffion', 'Gareth', 'Huw', 'Iwan', 'Jade', 'Katie', 'Llion', 'Megan', 'Nia', 'Owain', 'Rhian', 'Sian', 'Tegan', 'Urien', 'Wyn']
welsh_surnames = ['Bevan', 'Ceri', 'Davies', 'Edwards', 'Fychan', 'Glyn', 'Hedd', 'Idris', 'Jones', 'Lloyd', 'Morgan', 'Nia', 'Owen', 'Price', 'Rees', 'Roberts', 'Thomas', 'Walters', 'Williams', 'Yorath']
anglesey_towns = ['Amlwch', 'Beaumaris', 'Benllech', 'Bodedern', 'Cemaes', 'Gaerwen', 'Holyhead', 'Llanbadrig', 'Llanddona', 'Llandegfan', 'Llanerchymedd', 'Llanfairpwllgwyngyll', 'Menai Bridge', 'Moelfre', 'Newborough', 'Pentraeth', 'Rhosneigr', 'Trearddur Bay', 'Valley', 'Y Felinheli']
anglesey_counties = ['Anglesey', 'Gwynedd', 'Conwy']

# Define some helper functions for generating random data
def generate_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def generate_username(forename, surname):
    return (forename[0] + surname).lower()

def generate_password():
    return "Passw0rd!" + str(random.randint(1, 100))

def generate_welsh_forename():
    return random.choice(welsh_forenames)

def generate_welsh_surname():
    return random.choice(welsh_surnames)

def generate_sex():
    return random.choice(['M', 'F'])

def generate_title():
    return random.choice(['Mr', 'Mrs', 'Ms', 'Dr'])

def generate_birthdate():
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

def generate_hire_date():
    year = random.randint(2010, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

def generate_job_description():
    return random.choice(['Manager', 'Employee'])

def generate_town():
    return random.choice(anglesey_towns)

def generate_county():
    return random.choice(anglesey_counties)

def generate_phone_number():
    phone_number = "0" + str(random.randint(7, 9))
    for i in range(9):
        phone_number += str(random.randint(0, 9))
    return phone_number

def generate_postcode():
  """Generates a random Anglesey postcode following the format "LL77 nll".

  Returns:
    A string containing the random postcode.
  """

  # Generate a random number between 1 and 99
  random_number = random.randint(1, 9)

  # Generate a random capital letter from A to Z
  random_letter = str(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

  # Create the postcode
  return f"LL77 {random_number}{random_letter}"

# Generate 100 dummy
with open('Teacher.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for i in range(20):
        forename = generate_welsh_forename()
        surname = generate_welsh_surname()
        row = [
            generate_username(forename, surname),
            generate_password(),
            forename,
            surname,
            generate_sex(),
            generate_title(),
            generate_birthdate(),
            generate_hire_date(),
            generate_town(),
            generate_county(),
            generate_postcode(),
            generate_phone_number(),
            forename.lower() + "." + surname.lower() + "@example.com"
        ]
        writer.writerow(row)