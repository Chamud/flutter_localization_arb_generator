import csv
import os
import tkinter as tk
from tkinter import messagebox
import json
import sys

# Define the input CSV file name
csv_file = 'localization_data.csv'

# Create a dictionary to store the data
data = {}

# Delete all .arb and .json files in the same directory
for file in os.listdir():
  if file.endswith(".arb") or file.endswith(".json"):
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
  tk.Tk().withdraw()  # Hide the root window
  messagebox.showerror("Error", f"An error occurred while reading the CSV file: {str(e)}")
  sys.exit(1)

# Create the main window
root = tk.Tk()
root.title("File Format Selection")

# Define variables for radio buttons
file_format_var = tk.StringVar()

# Create radio buttons
arb_button = tk.Radiobutton(root, text="ARB", variable=file_format_var, value="arb")
json_button = tk.Radiobutton(root, text="JSON", variable=file_format_var, value="json")

# Select ARB by default
file_format_var.set("arb")

# Layout the radio buttons
arb_button.pack()
json_button.pack()


def generate_files():
  # Get the selected file format
  file_format = file_format_var.get()

  if file_format not in ['arb', 'json']:
    messagebox.showerror("Error", "Invalid file format selected. Please select either 'arb' or 'json'.")
    return

  # Rest of the code for generating files based on the selected format...
  # (same as the original code with `file_format` variable)
  else:

    # Define the output file names for each language
    output_files_arb = {lang: f'app_{lang}.{file_format}' for lang in languages}
    output_files_json = {lang: f'{lang}.{file_format}' for lang in languages}

    # Generate the files for each language
    try:
        if file_format == 'arb':
            for locale, output_file in output_files_arb.items():
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
                    
        elif file_format == 'json':
                for locale, output_file in output_files_json.items():
                    with open(output_file, 'w', encoding='utf-8') as out_file:
                        json_data = {}
                        for key, translations in data.items():
                            json_data[key] = translations[locale]
                        json.dump(json_data, out_file, ensure_ascii=False, indent=4)
                
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating files: {str(e)}")

  root.destroy()  # Close the window after success

# Button to trigger file generation
generate_button = tk.Button(root, text="Generate Files", command=generate_files)
generate_button.pack()

# Run the main event loop
root.mainloop()