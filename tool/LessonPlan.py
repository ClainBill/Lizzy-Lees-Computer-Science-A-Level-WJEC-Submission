import random
import csv

lesson_titles = [
    "Introduction to Piano Playing",
    "Guitar Chords and Techniques",
    "Music Theory for Beginners",
    "Singing Techniques and Performance",
    "Advanced Drums and Percussion",
    "Songwriting and Composition"
]

lesson_objectives = [
    "Developing proper hand and finger technique on the piano",
    "Learning basic chords and strumming patterns on the guitar",
    "Understanding music notation and basic theory concepts",
    "Improving vocal range and control for better singing performance",
    "Mastering complex drum patterns and rhythms",
    "Exploring different songwriting techniques and approaches"
]

materials = [
    "Piano keyboard, sheet music, metronome",
    "Guitar, pick, music stand",
    "Textbook, music notation software, staff paper",
    "Microphone, backing tracks, vocal exercises",
    "Drum kit, drumsticks, practice pad",
    "Instrument of choice, songwriting software"
]

procedures = [
    "Begin by reviewing basic finger and hand position on the keyboard, then practice playing simple melodies and scales. Move on to more complex pieces as proficiency increases.",
    "Start by learning basic chords and strumming patterns, then progress to more advanced techniques such as fingerpicking and alternate tunings.",
    "Review the basics of music notation and theory, including staff notation, key signatures, and time signatures. Practice identifying notes and chords, and analyze simple pieces.",
    "Begin by warming up the voice with breathing exercises and vocal warm-ups. Then practice singing simple songs, focusing on tone, pitch, and expression. Move on to more complex pieces as proficiency increases.",
    "Start by practicing basic rhythms and stick control on a practice pad, then progress to more complex patterns on the drum kit. Focus on technique and timing.",
    "Explore different approaches to songwriting, such as melody-first, lyrics-first, and chord progressions. Experiment with different instruments and styles."
]

# Generate 20 random lesson plans
lesson_plans = []
for i in range(20):
    lesson_plan = [
        lesson_titles[random.randint(0, len(lesson_titles)-1)],
        lesson_objectives[random.randint(0, len(lesson_objectives)-1)],
        materials[random.randint(0, len(materials)-1)],
        procedures[random.randint(0, len(procedures)-1)]
    ]
    lesson_plans.append(lesson_plan)

# Write the lesson plans to a CSV file
with open("LessonPlan.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["lesson_title", "lesson_objective", "materials", "procedure"])
    writer.writerows(lesson_plans)
