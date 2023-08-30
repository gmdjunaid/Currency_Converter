import requests
import tkinter as tk
from tkinter import ttk


from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

api_key = os.getenv("api_key")
BASE_URL = "https://free.currconv.com/"

# Define the main application class
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Lists to store currency labels and entry boxes for later use
        self.currency_labels = []
        self.currency_entry_boxes = []

        # Initialize the user interface
        self.setup_ui()

    def setup_ui(self):
        # Create and display a welcome label
        label = tk.Label(self.root, text="Welcome to the currency converter!", font=('Arial', 20, 'bold'), fg="#5e32a8")
        label.pack()

        # Create a button to list currencies and display it
        list_button = tk.Button(self.root, text="List Currencies", command=self.list_currencies, font=('Arial', 15),
                                fg="#5e32a8", bg="#3260a8", activeforeground="#5e32a8", activebackground="#3260a8")
        list_button.pack()

        # Create a button to perform currency conversion and display it
        convert_button = tk.Button(self.root, text="Convert", command=self.convert_currencies, font=('Arial', 15),
                                   fg="#5e32a8", bg="#3260a8", activeforeground="#5e32a8", activebackground="#3260a8")
        convert_button.pack()

        # Create an entry box for entering the amount to convert and display it
        self.amount_var = tk.StringVar()
        amount_entry = tk.Entry(self.root, textvariable=self.amount_var)
        amount_entry.pack()

        # Create a label to display the conversion result and display it
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def list_currencies(self):
        # Define the API endpoint to fetch a list of currencies
        endpoint = f"api/v7/currencies?apiKey={api_key}"
        url = BASE_URL + endpoint

        # Fetch currency data from the API and convert to a list
        data = requests.get(url).json()
        currency_list = list(data.keys())
        currency_list.sort()

        # Clear any previous currency labels and entry boxes
        self.currency_labels = []
        self.currency_entry_boxes = []

        # Create labels and entry boxes for currency selection and display them
        for i in range(2):
            label = tk.Label(self.root, text="Currency " + str(i + 1))
            label.pack()
            self.currency_labels.append(label)

            entry_box = tk.Entry(self.root)
            entry_box.pack()
            self.currency_entry_boxes.append(entry_box)

    def convert_currencies(self):
        # Retrieve currency choices and amount from the user input
        currency1 = self.currency_entry_boxes[0].get()
        currency2 = self.currency_entry_boxes[1].get()
        amount = self.amount_var.get()

        # Define the API endpoint for currency conversion
        endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={api_key}"
        url = BASE_URL + endpoint

        # Fetch currency conversion rate from the API
        data = requests.get(url).json()

        # Handle cases of invalid or unsupported currencies
        if not data:
            self.result_label.config(text="Invalid currencies.")
            return

        rate = data.get(f"{currency1}_{currency2}")
        if rate is None:
            self.result_label.config(text="Invalid currencies.")
            return

        # Calculate the converted amount and display the result
        converted_amount = float(amount) * rate
        self.result_label.config(text=f"{amount} {currency1} is equal to {converted_amount:.2f} {currency2}")

# Define the main function
def main():
    # Create the main application window
    root = tk.Tk()

    # Initialize and run the CurrencyConverterApp
    app = CurrencyConverterApp(root)
    root.mainloop()

# Run the main function when the script is executed directly
if __name__ == "__main__":
    main()