import requests
import tkinter as tk
from tkinter import filedialog
import os

# 1. Setup the File Picker
root = tk.Tk()
root.withdraw()  # Hides the messy background window
root.attributes('-topmost', True)  # Forces the popup to the front

print("Opening file dialog... Please select a PDF from your computer.")

# 2. Open the File Dialog
file_path = filedialog.askopenfilename(
    title="Select your Study Notes (PDF)",
    filetypes=[("PDF Files", "*.pdf")]
)

# 3. Process the Selected File
if not file_path:
    print("No file was selected. Canceling test.")
else:
    # Extract just the file name to display it nicely
    file_name = os.path.basename(file_path)
    print(f"\nSuccessfully selected: {file_name}")

    # Let you ask a custom question in the terminal!
    user_query = input("What question do you want to ask the AI about these notes? \n> ")

    url = 'http://127.0.0.1:5000/process-document'

    try:
        with open(file_path, 'rb') as f:
            # Package the dynamic file and dynamic query
            files = {'file': f}
            data = {'query': user_query}

            print("\nSending document to your Flask backend...")
            response = requests.post(url, files=files, data=data)

            # Print the server's response
            print("\n--- AI Server Response ---")
            print(response.json())

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is app.py still running?")
