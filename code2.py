import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
import os
import random

# List of moods with emoji representation
mood_options = {
    1: ("😊", "Happy"),
    2: ("😔", "Sad"),
    3: ("😡", "Angry"),
    4: ("😴", "Tired"),
    5: ("😇", "Grateful"),
    6: ("🤔", "Thoughtful")
}

# List of motivational quotes for negative moods
motivational_quotes = [
    "Keep going, you're doing great!",
    "Believe in yourself, and all that you are.",
    "Challenges are what make life interesting.",
    "When it rains, look for rainbows!",
    "Success is not final, failure is not fatal: it is the courage to continue that counts."
]

# Check if today is logged
def check_streak():
    moods = read_mood_log()
    if not moods:
        return 0
    
    last_entry = datetime.strptime(moods[-1]["Timestamp"], "%Y-%m-%d %H:%M:%S")
    today = datetime.now()
    
    if (today - last_entry).days == 1:
        return 1
    return 0

# Mood tracker menu
def display_mood_menu():
    print("\nSelect your current mood by number:")
    for num, (emoji, mood) in mood_options.items():
        print(f"{num}. {emoji} - {mood}")

# Log mood entry
def log_mood():
    display_mood_menu()

    try:
        mood_choice = int(input("\nEnter the number corresponding to your mood: "))
        if mood_choice not in mood_options:
            print("Invalid choice! Try again.")
            return
    except ValueError:
        print("Please enter a valid number!")
        return

    comment = input("Optional: Add a short comment (or press Enter to skip): ")

    emoji, mood = mood_options[mood_choice]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mood_data = [emoji, mood, timestamp, comment]

    # Save the mood to a CSV file with UTF-8 encoding
    file_exists = os.path.isfile("mood_log_advanced.csv")
    with open("mood_log_advanced.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Emoji", "Mood", "Timestamp", "Comment"])
        writer.writerow(mood_data)

    print(f"\nMood logged: {mood} at {timestamp}!")

    # Provide motivational quotes for negative moods
    if mood in ["Sad", "Angry", "Tired"]:
        print("\nHere's something to lift your spirits:")
        print(random.choice(motivational_quotes))

# Read mood log from CSV
def read_mood_log():
    moods = []
    if os.path.exists("mood_log_advanced.csv"):
        with open("mood_log_advanced.csv", "r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                moods.append(row)
    return moods

# View complete mood history
def view_mood_history():
    moods = read_mood_log()
    if not moods:
        print("No mood history available yet.")
        return

    print("\nMood History:")
    for entry in moods:
        print(f"Emoji: {entry['Emoji']}, Mood: {entry['Mood']}, Time: {entry['Timestamp']}, Comment: {entry['Comment']}")

# Mood trend analysis
def summarize_moods():
    moods = read_mood_log()

    if not moods:
        print("No moods logged yet.")
        return

    mood_count = {mood: 0 for emoji, mood in mood_options.values()}
    for entry in moods:
        mood_count[entry["Mood"]] += 1

    print("\nMood Summary:")
    for mood, count in mood_count.items():
        print(f"{mood}: {count} times")

    # Visualize the mood data
    plt.bar(mood_count.keys(), mood_count.values(), color='skyblue')
    plt.title("Mood Distribution")
    plt.xlabel("Moods")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Analyze mood by time of day
def analyze_mood_by_time():
    moods = read_mood_log()

    if not moods:
        print("No moods logged yet.")
        return

    time_periods = {
        "Morning": 0,
        "Afternoon": 0,
        "Evening": 0
    }

    for entry in moods:
        time = datetime.strptime(entry["Timestamp"], "%Y-%m-%d %H:%M:%S").time()
        if time < datetime.strptime("12:00", "%H:%M").time():
            time_periods["Morning"] += 1
        elif time < datetime.strptime("17:00", "%H:%M").time():
            time_periods["Afternoon"] += 1
        else:
            time_periods["Evening"] += 1

    print("\nMood Logs Based on Time of Day:")
    for period, count in time_periods.items():
        print(f"{period}: {count} times")

    # Pie chart for time of day analysis
    plt.pie(time_periods.values(), labels=time_periods.keys(), autopct='%1.1f%%', startangle=90)
    plt.title("Mood Logs by Time of Day")
    plt.show()

def main():
    streak = check_streak()

    while True:
        print("\n--- Advanced Emoji Mood Tracker ---")
        if streak:
            print(f"🔥 You've logged your mood for {streak} consecutive days!")
        print("1. Log Mood")
        print("2. View Mood Summary")
        print("3. View Complete Mood History")
        print("4. Analyze Mood by Time of Day")
        print("5. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            log_mood()
        elif choice == "2":
            summarize_moods()
        elif choice == "3":
            view_mood_history()
        elif choice == "4":
            analyze_mood_by_time()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please select again.")

if __name__ == "__main__":
    main()
