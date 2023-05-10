import csv
import random
import datetime

# Generate a list of 10 room names in the format "Room X"
rooms = ["Room " + str(i) for i in range(1, 11)]
frequency = ["Weekly", "Fortnightly", "Monthly"]

# Generate a list of 3 random counties on Anglesey
counties = ["Isle of Anglesey", "Gwynedd", "Conwy"]

#Method to return random date in format DD/MM/YYYY
generateDate = lambda: datetime.date(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28)).strftime("%d/%m/%Y")


# Generate dummy data for 100 records
data = []
for i in range(200):
    student_id = random.randint(1, 120)
    teacher_id = random.randint(1, 20)
    location = random.choice(rooms)
    lesson_frequency = random.choice(frequency)
    lesson_day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    lesson_time = datetime.time(random.randint(8, 16), random.randint(0, 59)).strftime("%H:%M")
    lesson_length = random.choice([30, 45, 60])
    lesson_cost = random.choice([20.00, 25.00, 30.00, 35.00, 40.00])
    booking_date = generateDate()
    booking_update = generateDate()
    cancelled = random.randint(0, 1)
    
    data.append((student_id, teacher_id, location, lesson_frequency, lesson_day, lesson_time, lesson_length, lesson_cost, booking_date, booking_update, cancelled))

# Write the data to a CSV file
with open("StudentBookings.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["StudentID", "TeacherID", "location", "lesson_frequency", "lesson_day", "lesson_time", "lesson_length", "lesson_cost", "booking_date", "last_update", "cancelled"])
    writer.writerows(data)
