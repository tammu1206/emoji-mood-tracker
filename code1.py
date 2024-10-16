import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os

# List of moods with emoji representation
mood_options = {
    1: ("😊", "Happy"),
    2: ("😔", "Sad"),
    3: ("😡", "Angry"),
    4: ("😴", "Tired"),
    5: ("😇", "Grateful"),
    6: ("🤔", "Thoughtful")
}

def display_mood_menu():
    print("\nSelect your current mood by number:")
    for num, (emoji, mood) in mood_options.items():
        print(f"{num}. {emoji} - {mood}")

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

def read_mood_log():
    moods = []
    if os.path.exists("mood_log_advanced.csv"):
        with open("mood_log_advanced.csv", "r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                moods.append(row)
    return moods

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

def main():
    while True:
        print("\n--- Advanced Emoji Mood Tracker ---")
        print("1. Log Mood")
        print("2. View Mood Summary")
        print("3. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            log_mood()
        elif choice == "2":
            summarize_moods()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please select again.")

if __name__ == "__main__":
    main()
