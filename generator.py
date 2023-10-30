import csv
import os
import tkinter as tk
from tkinter import messagebox
import sys

# Define the input CSV file name
csv_file = 'localization_data.csv'

# Create a dictionary to store the data
data = {}

# Delete all .arb files in the same directory
for file in os.listdir():
    if file.endswith(".arb"):
        os.remove(file)

# Read the CSV file and populate the dictionary
try:
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        languages = headers[1:]  # Extract all languages except 'en'
        for row in reader:
            key, *translations = row
            translations_dict = {languages[i]: translations[i] for i in range(len(translations))}
            data[key] = {
                **translations_dict  # Add translations for other languages
            }
except Exception as e:
    messagebox.showerror("Error", f"An error occurred while reading the CSV file: {str(e)}")
    sys.exit(1)

# Define the output file names for each language
output_files = {lang: f'app_{lang}.arb' for lang in languages}

# Generate the .arb files for each language
try:
    for locale, output_file in output_files.items():
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write('{\n')
            if locale != 'en':
                out_file.write(f'    "@@locale": "{locale}",\n\n')
            for key, translations in data.items():
                out_file.write(f'    "{key}": "{translations[locale]}"')
                if key != list(data.keys())[-1]:
                    out_file.write(',')
                out_file.write('\n')
            out_file.write('}\n')
    messagebox.showinfo("Success", "Files generated successfully.")

except Exception as e:
    messagebox.showerror("Error", f"An error occurred while generating .arb files: {str(e)}")

# Exit the program after clicking OK
sys.exit()
