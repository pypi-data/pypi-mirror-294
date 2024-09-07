#! /usr/bin/env python3

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

lbl = ttk.Label(root, text="Select the terms which best describe you.")
lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

rb1 = tk.Checkbutton(root)
rb1.grid(row=1, column=0, padx=10, pady=10)
lbl1 = ttk.Label(root, text="Bandu Goji")
lbl1.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

rb2 = tk.Checkbutton(root)
rb2.grid(row=2, column=0, padx=10, pady=10)
lbl2 = ttk.Label(root, text="Computer Experts")
lbl2.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

rb3 = tk.Checkbutton(root)
rb3.grid(row=3, column=0, padx=10, pady=10)
lbl3 = ttk.Label(root, text="Troublemakers")
lbl3.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

lbl = ttk.Label(root, text="Only computer experts are allowed on Zoom.")
lbl.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

btn = tk.Button(root, text="Confirm", relief="solid")
btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.grid_columnconfigure(1, weight=1)
root.title("Pre-Zoom Survey")

root.tk.call('tk', 'scaling', 4.0)

root.mainloop()
