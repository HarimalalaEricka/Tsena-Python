import tkinter as tk
from tkinter import ttk

class Filtre:
    def __init__(self, master):
        self.master = master
        self.master.title("Sélection de l'année et du mois")
        self.master.geometry("300x150")  
        
        self.label_annee = tk.Label(master, text="Année:")
        self.label_annee.grid(row=0, column=0, padx=10, pady=10)
        
        self.annee = tk.StringVar()
        self.combobox_annee = ttk.Combobox(master, textvariable=self.annee)
        self.combobox_annee['values'] = [str(year) for year in range(2024, 2040)]  
        self.combobox_annee.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_mois = tk.Label(master, text="Mois:")
        self.label_mois.grid(row=1, column=0, padx=10, pady=10)
        
        self.mois = tk.StringVar()
        self.combobox_mois = ttk.Combobox(master, textvariable=self.mois)
        self.combobox_mois['values'] = [str(month) for month in range(1, 13)]  
        self.combobox_mois.grid(row=1, column=1, padx=10, pady=10)
        
        self.bouton_valider = tk.Button(master, text="Valider", command=self.valider)
        self.bouton_valider.grid(row=2, columnspan=2, pady=10)

        self.selection = None

    def valider(self):
        self.selection = (self.annee.get(), self.mois.get())
        self.master.quit()

    def get_selection(self):
        return self.selection