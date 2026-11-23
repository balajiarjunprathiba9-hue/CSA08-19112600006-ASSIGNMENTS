
import re
import sqlite3
import random
import time
import os
from collections import Counter

# ==========================================
# TASK B4 - FINAL ENGINEERING DECISION
# ==========================================

POSITIVE = {
    "good", "great", "excellent", "clean", "prompt",
    "quick", "quickly", "helpful", "resolved",
    "happy", "polite", "safe", "efficient",
    "thanks", "thank", "satisfied", "beautiful",
    "wonderful", "smooth", "nice", "kind"
}

NEGATIVE = {
    "bad", "terrible", "dirty", "broken", "dangerous",
    "unsafe", "irregular", "blocked", "overflowing",
    "pollution", "smell", "pathetic", "slow",
    "poor", "delay", "unbearable", "rude",
    "waste", "sick", "failed", "dark", "contaminated"
}

NEGATORS = {"not", "no", "never", "cannot", "hardly"}

def score(text):
    words = re.findall(r"[a-z]+", text.lower())
    total = 0

    for i, word in enumerate(words):
        value = 0

        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1

        if value:
            previous = words[max(0, i-3):i]
            if sum(w in NEGATORS for w in previous) % 2:
                value = -value

            total += value

    return total


def label(text):
    s = score(text)

    if s > 0:
        return "positive"
    elif s < 0:
        return "negative"
    else:
        return "neutral"


# ==========================================
# COMPLAINT DATASET - 62 COMPLAINTS
# ==========================================

P = "positive"
N = "negative"
U = "neutral"

COMPLAINTS = [

("The garbage near Adyar bus stop has not been cleared for a week and the smell is terrible.", N),
("Street lights on Velachery main road are broken and the road is dark and unsafe at night.", N),
("Water supply is irregular and the tanker never arrives on time.", N),
("There is a huge pothole near Guindy signal and it is dangerous for two wheelers.", N),
("Sewage is overflowing on our street and mosquitoes are everywhere.", N),
("Nobody responded to my complaint about the noise from the factory.", N),
("The dust from construction work is making it hard to breathe.", N),
("Rude behaviour from the staff at the ward office and no action taken.", N),
("Drain is blocked and water is stagnant in front of my house.", N),
("The air pollution here is the worst I have ever seen.", N),
("Burning of waste near the lake every evening, the smoke is unbearable.", N),
("Complaint registered three times and still no one came. Pathetic service.", N),
("The bus shelter is damaged and crowded all the time.", N),
("Road repair was promised months ago but nothing has been done.", N),
("I am tired of calling the helpline, it is a waste of time.", N),
("Stray dogs are attacking people in our colony and the authorities are not bothered.", N),
("The stagnant water has become a breeding ground for mosquitoes.", N),
("Foul smell from the drain is making life difficult.", N),
("Oh great, another power cut during the exam week. Wonderful.", N),
("The complaint portal keeps crashing and I cannot submit my request.", N),
("Not happy with the delay in fixing the street light.", N),
("The park is dirty and the benches are broken.", N),
("Very slow response and poor follow up from the department.", N),
("Traffic signal is not working at the Guindy junction, causing long jams.", N),
("Contaminated drinking water was supplied to our apartment.", N),
("The road was repaired well but the drain is still blocked and smells bad.", N),
("Staff were polite but the delay is unacceptable.", N),

("Thank you for clearing the garbage so quickly, the street is clean now.", P),
("The water supply issue was resolved within a day. Excellent work.", P),
("Very polite and helpful staff at the ward office.", P),
("The new street lights on Adyar road are great and the area feels safe.", P),
("Pothole was fixed promptly, thanks to the quick action by the team.", P),
("Happy with the improved bus service, it is faster and cleaner.", P),
("The park has been well maintained and it is a pleasure to walk there.", P),
("No complaints about the water supply this month, it has been regular.", P),
("Appreciate the quick response from the pollution control board.", P),
("The new waste collection system is efficient and the street is spotless.", P),
("Good job by the sanitation workers, the drain is no longer blocked.", P),
("Excellent improvement in air quality near the school after the new rules.", P),
("I am satisfied with how the officer handled my request.", P),
("The road is smooth now and travel is comfortable.", P),
("Great initiative, the new complaint app is easy to use.", P),
("Thanks to the corporation for the clean drinking water.", P),
("Metro has made commuting fast and safe.", P),
("Not bad at all, the new bus stop is quite nice.", P),
("The helpline operator was kind and solved my problem within minutes.", P),
("Wonderful cleanup drive in our locality, the beach looks beautiful.", P),

("Please share the schedule for garbage collection in Velachery.", U),
("I would like to know the office hours of the zonal office.", U),
("Requesting a copy of the air quality report for January.", U),
("Can you tell me how to apply for a new water connection?", U),
("The meeting about the new drainage plan is on Monday at 10 am.", U),
("Where can I find the contact number of the ward officer?", U),
("Kindly update me on the status of application number 4521.", U),
("A new bus route has been introduced between Adyar and Guindy.", U),
("Please confirm if the pollution monitoring station at Adyar is working.", U),
("I want to know the process for changing my property tax address.", U),
("The survey team visited our street yesterday.", U),
("What documents are needed to register a complaint?", U),
("The water tank cleaning is scheduled for Saturday.", U),
("Requesting details about the tree plantation drive next month.", U),
("Is the Velachery station data available for download?", U)

]


# ==========================================
# SUMMARISATION
# ==========================================

def summarise(text, k=2):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    words = set(NEGATIVE) | set(POSITIVE)

    ranked = []

    for i, sentence in enumerate(sentences):
        tokens = re.findall(r"[a-z]+", sentence.lower())
        importance = sum(w in words for w in tokens)

        ranked.append((importance, i, sentence))

    selected = sorted(
        ranked,
        key=lambda x: (-x[0], x[1])
    )[:k]

    selected.sort(key=lambda x: x[1])

    return " ".join(x[2] for x in selected)


def first_k(text, k=2):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:k])


# ==========================================
# B4.1 SENTIMENT ANALYSIS
# ==========================================

print("\n========== B4.1 SENTIMENT ANALYSIS ==========")

labels = ["positive", "negative", "neutral"]

conf = Counter(
    (actual, label(text))
    for text, actual in COMPLAINTS
)

correct = sum(conf[(x, x)] for x in labels)

accuracy = correct / len(COMPLAINTS)

print("Total complaints:", len(COMPLAINTS))
print("Agreement:", correct, "/", len(COMPLAINTS))
print("Accuracy: {:.2f}%".format(accuracy * 100))

print("\nCONFUSION MATRIX")
print(f"{'':12s}" + "".join(f"{x:>12s}" for x in labels))

for actual in labels:
    print(
        f"{actual:12s}"
        + "".join(f"{conf[(actual, predicted)]:12d}"
                  for predicted in labels)
    )

print("\nCLASS RECALL")

for x in labels:
    total = sum(conf[(x, p)] for p in labels)
    recall = conf[(x, x)] / total if total else 0

    print(x, ":", "{:.2f}%".format(recall * 100))


print("\nWRONGLY CLASSIFIED COMPLAINTS")

for text, actual in COMPLAINTS:
    predicted = label(text)

    if predicted != actual:
        print("Actual:", actual, "| Predicted:", predicted)
        print(text)


# ==========================================
# SUMMARISER COMPARISON
# ==========================================

print("\n========== SUMMARISER COMPARISON ==========")

LONG = [

(
"I am writing about the road near Velachery signal. "
"I have lived here for ten years and the area is generally quiet. "
"Last month a huge pothole formed in front of the bank and two bikers fell down. "
"The pothole has not been repaired even after three reminders. "
"Please repair the pothole urgently before someone gets seriously hurt.",
"pothole"
),

(
"Hello, I am a resident of Guindy. Thank you for taking my complaint. "
"The drinking water in our street has been dirty and smelly for ten days. "
"Many children have fallen sick after drinking this water. "
"We request the board to test the water and clean the pipeline.",
"water"
),

(
"Good morning. I want to bring something to your kind attention. "
"The garbage bins at Adyar market have been overflowing since Diwali. "
"Rats and flies are spreading in the area. "
"Kindly arrange daily garbage collection.",
"garbage"
),

(
"To the Pollution Control Board. A small factory near our colony burns plastic every night. "
"The black smoke enters our houses and the smell is unbearable. "
"Several elders have breathing problems. "
"Kindly inspect the factory and stop the burning.",
"plastic"
)

]

hit_ex = 0
hit_fk = 0

for text, key in LONG:

    extractive = summarise(text, 2)
    first = first_k(text, 2)

    ex = key in extractive.lower()
    fk = key in first.lower()

    hit_ex += ex
    hit_fk += fk

    print("\nKeyword:", key)
    print("Extractive summary:", extractive)
    print("First two sentences:", first)
    print("Extractive contains keyword:", ex)
    print("First-k contains keyword:", fk)

print("\nExtractive coverage:", hit_ex, "/", len(LONG))
print("First-k coverage:", hit_fk, "/", len(LONG))


# ==========================================
# 50,000 COMPLAINTS PERFORMANCE TEST
# ==========================================

print("\n========== 50,000 COMPLAINTS TEST ==========")

random.seed(3)

month = [
    random.choice(COMPLAINTS)[0]
    for _ in range(50000)
]

start = time.perf_counter()

results = [label(x) for x in month]

elapsed = time.perf_counter() - start

print("Total complaints:", len(month))
print("Processing time:", round(elapsed, 3), "seconds")
print("Processing speed:",
      round(50000 / max(elapsed, 0.000001)), "complaints/second")

print("Label counts:", dict(Counter(results)))


# ==========================================
# B4.2 SQLITE INDEX EXPERIMENT
# ==========================================

print("\n========== B4.2 DATABASE INDEX ==========")

conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE readings (
    station_id TEXT,
    day TEXT,
    pm25 REAL
)
""")

random.seed(5)

rows = []

# Online compiler friendly test:
# 120 stations x 30 days x 24 hours

for s in range(120):

    for d in range(30):

        day = "2025-01-" + str(d + 1).zfill(2)

        for h in range(24):

            pm = round(
                max(5, 40 + 3 * (s % 10) +
                    random.gauss(0, 12)),
                1
            )

            rows.append(
                ("Station" + str(s + 1), day, pm)
            )

conn.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    rows
)

conn.commit()

nrows = len(rows)

print("Total database rows:", nrows)


probe = [
    (
        "Station" + str(random.randint(1, 120)),
        "2025-01-" + str(random.randint(1, 30)).zfill(2)
    )
    for _ in range(300)
]


queries = {

    "A - Station-day lookup": lambda: [
        conn.execute(
            "SELECT AVG(pm25) FROM readings "
            "WHERE station_id=? AND day=?",
            p
        ).fetchone()
        for p in probe
    ],

    "B - Daily mean": lambda: conn.execute(
        "SELECT station_id, day, AVG(pm25) "
        "FROM readings GROUP BY station_id, day"
    ).fetchall(),

    "C - Readings above 60": lambda: conn.execute(
        "SELECT station_id, COUNT(*) "
        "FROM readings WHERE pm25 > 60 "
        "GROUP BY station_id"
    ).fetchall()

}


def timeit(function):

    best = float("inf")

    for _ in range(3):

        start = time.perf_counter()
        function()
        elapsed = time.perf_counter() - start

        best = min(best, elapsed)

    return best


before = {
    name: timeit(function)
    for name, function in queries.items()
}

plan_before = conn.execute("""
EXPLAIN QUERY PLAN
SELECT AVG(pm25) FROM readings
WHERE station_id='Station1'
AND day='2025-01-01'
""").fetchall()

print("\nQuery plan before index:", plan_before)


start = time.perf_counter()

conn.execute("""
CREATE INDEX idx_station_day
ON readings(station_id, day)
""")

conn.commit()

index_time = time.perf_counter() - start


plan_after = conn.execute("""
EXPLAIN QUERY PLAN
SELECT AVG(pm25) FROM readings
WHERE station_id='Station1'
AND day='2025-01-01'
""").fetchall()

print("Query plan after index:", plan_after)

after = {
    name: timeit(function)
    for name, function in queries.items()
}


print("\nQUERY PERFORMANCE COMPARISON")

print(f"{'Query':28s}{'Before':>12s}{'After':>12s}")

for name in queries:

    print(
        f"{name:28s}"
        f"{before[name]*1000:10.2f}ms"
        f"{after[name]*1000:10.2f}ms"
    )

    speedup = before[name] / max(after[name], 0.000001)

    print("Speed-up:", round(speedup, 2), "x")

print("\nIndex creation time:",
      round(index_time, 4), "seconds")


# ==========================================
# B4.3 PRODUCTION SCALE ESTIMATION
# ==========================================

print("\n========== B4.3 PRODUCTION DECISION ==========")

# Measure insertion speed

start = time.perf_counter()

test_conn = sqlite3.connect(":memory:")

test_conn.execute("""
CREATE TABLE test_readings (
    station_id TEXT,
    day TEXT,
    pm25 REAL
)
""")

test_conn.executemany(
    "INSERT INTO test_readings VALUES (?, ?, ?)",
    rows[:20000]
)

insert_time = time.perf_counter() - start

insert_speed = 20000 / max(insert_time, 0.000001)

print("Insertion speed:",
      round(insert_speed), "rows/second")


# Production estimation

new_rows_year = (
    100 * 96 * 365 +
    12 * 24 * 365
)

daily_rows = 100 * 96 + 12 * 24

bytes_per_row = 106

database_size = new_rows_year * bytes_per_row

print("\nNEW PRODUCTION SCENARIO")

print("New stations: 100")
print("Old stations: 12")
print("New station readings per day: 96")
print("Old station readings per day: 24")

print("Total rows per day:", daily_rows)

print("Total rows per year:", new_rows_year)

print("Estimated database size:",
      round(database_size / 1000000), "MB")

print("Estimated daily insertion time:",
      round(daily_rows / max(insert_speed, 1), 3),
      "seconds")

print("50,000 complaints per month can be processed using",
      round(50000 / max(elapsed, 0.000001)),
      "complaints per second (measured above)")


# ==========================================
# FINAL DECISION
# ==========================================

print("\n========== FINAL ENGINEERING DECISION ==========")

print("""
1. SQLite is suitable for structured environmental data.

2. An index on station_id and day improves station-day
   search performance.

3. Python lexicon-based sentiment analysis is fast,
   but it may fail to understand sarcasm and context.

4. Extractive summarisation helps identify important
   complaint information.

5. At larger scales, database indexing, batch processing
   and regular data cleaning are recommended.

6. For better sentiment accuracy, a trained machine
   learning model should be considered.

FINAL CONCLUSION:
A combination of SQLite, Python data processing and
improved machine learning techniques is suitable for
the proposed environmental monitoring system.
""")

conn.close()
test_conn.close()
