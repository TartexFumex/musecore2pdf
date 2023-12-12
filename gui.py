import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os, sys

from extraction import Extraction

from threading import Thread

class Gui():
    def __init__(self) -> None:
        # Initialize the GUI
        self.root = tk.Tk()

        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = (screen_width/2) - (530/2)
        y = (screen_height/2) - (300/2)

        self.root.title("Musecore2PDF")
        self.root.geometry(f"530x300+{int(x)}+{int(y)}")
        self.root.resizable(False, False)

        # Labels and entry widgets for Musecore URL and PDF file destination
        tk.Label(self.root, text="Musecore2PDF", font=("Arial", 20)).grid(row=0, column=0, columnspan=3, pady=10)
        tk.Label(self.root, text="Musecore url : ", font=("Arial", 10)).grid(row=1, column=0, pady=10)
        self.entry_url = tk.Entry(self.root, width=50)
        self.entry_url.grid(row=1, column=1, pady=10)
        tk.Label(self.root, text="PDF file destination : ", font=("Arial", 10)).grid(row=2, column=0, pady=10)
        self.entry_path = tk.Entry(self.root, width=50)
        self.entry_path.grid(row=2, column=1, pady=10)

        # Browse button to select PDF file destination
        self.button_browse = tk.Button(self.root, text="Browse", command=self.browse)
        self.button_browse.grid(row=2, column=2, pady=10)

        # Convert button to initiate the conversion process
        self.button_convert = tk.Button(self.root, text="Convert", command=self.convert)
        self.button_convert.grid(row=3, column=1, pady=10)

        # Progress bar and label for status information
        progress_frame = tk.Frame(self.root)
        progress_frame.grid(row=4, column=0, pady=10, columnspan=3)
        self.progress_bar_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=350, mode="determinate", variable=self.progress_bar_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, pady=10)
        self.label_status_var = tk.StringVar()
        self.label_status_var.set("Status")
        self.label_status = tk.Label(progress_frame, textvariable=self.label_status_var, font=("Arial", 10))
        self.label_status.grid(row=0, column=1, pady=10, columnspan=2)

        self.root.mainloop()

    def browse(self):
        # Open a file dialog to select PDF file destination
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")] )
        self.entry_path.delete(0, tk.END)
        self.entry_path.insert(0, file_path)

    def convert(self):
        # Perform validation and initiate the conversion process
        if self.entry_url.get() == "":
            messagebox.showerror("Error", "Please enter a URL")
        elif self.entry_path.get() == "":
            messagebox.showerror("Error", "Please select a destination file")
        else:
            url = self.entry_url.get()
            render_path = self.entry_path.get()

            # Initialize progress bar and disable UI elements during conversion
            self.progress_bar_var.set(0)
            self.button_browse.config(state="disabled")
            self.button_convert.config(state="disabled")
            self.entry_path.config(state="disabled")
            self.entry_url.config(state="disabled")

            # Initialize Extraction class and start extraction in a separate thread
            self.extraction = Extraction(self.root, self.label_status_var, self.progress_bar_var)
            self.thread = Thread(target=self.extraction.extract, args=(url, render_path))
            self.thread.start()

            # Wait for the thread to finish and update the UI
            while self.thread.is_alive():
                self.root.update()

            # Enable UI elements after conversion is complete
            self.button_browse.config(state="normal")
            self.button_convert.config(state="normal")
            self.entry_path.config(state="normal")
            self.entry_url.config(state="normal")

            # Reset progress bar and status label, and open the rendered PDF
            self.progress_bar_var.set(0)
            self.label_status_var.set("Status")
            os.startfile(render_path)

if __name__ == "__main__":
    gui = Gui()
