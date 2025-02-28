import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from Paiement import Paiement
from Box import Box

class FormulairePaiement:
    def __init__(self, master, parent, db):
        self.master = master
        self.parent = parent
        self.db = db
        self.master.title("Formulaire de Paiement")
        self.master.geometry("400x300")
        
        tk.Label(self.master, text="Id:").grid(row=0, column=0, padx=10, pady=10)
        self.id = tk.Entry(self.master)
        self.id.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Mois:").grid(row=1, column=0, padx=10, pady=10)
        self.mois = tk.StringVar()
        self.combobox_mois = ttk.Combobox(self.master, textvariable=self.mois)
        self.combobox_mois['values'] = [str(month) for month in range(1, 13)]
        self.combobox_mois.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Année:").grid(row=2, column=0, padx=10, pady=10)
        self.annee = tk.StringVar()
        self.combobox_annee = ttk.Combobox(self.master, textvariable=self.annee)
        self.combobox_annee['values'] = [str(year) for year in range(2025, 2040)]
        self.combobox_annee.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Date de paiement:").grid(row=3, column=0, padx=10, pady=10)
        self.date_paiement = DateEntry(self.master, date_pattern='yyyy-mm-dd')
        self.date_paiement.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.master, text="Montant:").grid(row=4, column=0, padx=10, pady=10)
        self.montant = tk.Entry(self.master)
        self.montant.grid(row=4, column=1, padx=10, pady=10)

        self.bouton_valider_paiement = tk.Button(self.master, text="Valider", command=self.valider_paiement)
        self.bouton_valider_paiement.grid(row=5, columnspan=2, pady=10)

    def valider_paiement(self):
        id_value = self.id.get()
        mois = self.mois.get()
        annee = self.annee.get()
        date_paiement = self.date_paiement.get()
        montant = int(self.montant.get())

        print(f"Id: {id_value}, Mois: {mois}, Année: {annee}, Date de paiement: {date_paiement}, Montant: {montant}")

        box = Box.getBoxById(id_value, self.db)
        Paiement.InsertPaiement(box, montant, self.db)

        self.master.destroy()

        self.parent.actualiser()