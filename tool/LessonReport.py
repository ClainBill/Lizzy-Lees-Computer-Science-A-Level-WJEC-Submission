import csv
import random
import string

# Define the headers for the CSV file
headers = ['LessonPlansID', 'StudentID', 'TeacherID', 'attended', 'student_behaviour', 'notes', 'Date']

# Define some helper functions for generating random data
def generate_id(min, max):
    return random.randint(min, max)

def generate_attended():
    return random.choice([0, 1])

def generate_student_behaviour():
    return random.randint(0, 4)

def generate_notes():
    return ''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(60))

def generate_date():
    year = random.randint(2010, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{day:02d}/{month:02d}/{year}'

# Generate 100 dummy records
with open('lessonReport.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for i in range(1, 1000):
        row = [
            # generate_id(),
            generate_id(1, 20),
            generate_id(1,120),
            generate_id(1, 20),
            generate_attended(),
            generate_student_behaviour(),
            generate_notes(),
            generate_date(),
        ]
        writer.writerow(row)
