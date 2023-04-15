import pandas as pd
import random
import time
import os
from googletrans import Translator
from plyer import notification

# Read in vocabulary CSV file and set up pandas DataFrame
vocabulary_file = 'vocabulary.csv'
if not os.path.exists(vocabulary_file):
    open(vocabulary_file, 'w').close() # Create empty file if it does not exist
vocabulary_df = pd.read_csv(vocabulary_file, index_col=0)

# Set up Google Translate API client
translator = Translator()

# Function to add a new word to the vocabulary
def add_word():
    while True:
        word = input("Enter the Italian word you want to learn: ")
        if word in vocabulary_df.index:
            print("That word already exists in the vocabulary!")
            continue
        break

    english_translation = translator.translate(word, dest='en').text
    russian_translation = translator.translate(word, dest='ru').text

    vocabulary_df.loc[word] = [english_translation, russian_translation, ""]

    vocabulary_df.to_csv(vocabulary_file)
    print(f"{word} has been added to the vocabulary.")

# Function to modify an existing word in the vocabulary
def modify_word():
    while True:
        word = input("Enter the Italian word you want to modify: ")
        if word not in vocabulary_df.index:
            print("That word does not exist in the vocabulary!")
            continue
        break

    print(f"{word}:")
    print(f"1. English translation: {vocabulary_df.loc[word]['english']}")
    print(f"2. Russian translation: {vocabulary_df.loc[word]['russian']}")
    print(f"3. Example usage: {vocabulary_df.loc[word]['example']}")
    print("Which field do you want to modify?")
    while True:
        field = input("Enter the field number (1-3): ")
        if field not in ['1', '2', '3']:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue
        break

    new_value = input("Enter the new value: ")
    if field == '1':
        vocabulary_df.at[word, 'english'] = new_value
    elif field == '2':
        vocabulary_df.at[word, 'russian'] = new_value
    else:
        vocabulary_df.at[word, 'example'] = new_value

    vocabulary_df.to_csv(vocabulary_file)
    print(f"{word} has been modified.")

# Function to generate a random word and send a notification with its translations
def generate_word_notification():
    if vocabulary_df.empty:
        print("The vocabulary is empty!")
        return

    word = random.choice(vocabulary_df.index)
    english_translation = vocabulary_df.loc[word]['english']
    russian_translation = vocabulary_df.loc[word]['russian']

    notification_title = "Italian Word to Learn"
    notification_message = f"{word}\n\nEnglish translation: {english_translation}\nRussian translation: {russian_translation}"

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=10
    )

# Function to set the notification period
def set_notification_period():
    while True:
        try:
            notification_period = int(input("Enter the notification period in hours: "))
            if notification_period <= 0:
                print("Invalid input. Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    return notification_period

# Main loop
while True:
    print("\nChoose an option:")
    print("1. Add a new word to the vocabulary")