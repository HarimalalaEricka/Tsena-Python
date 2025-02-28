from Box import Box  
from MaFenetre import MaFenetre
from Filtre import Filtre
import tkinter as tk
from ConnexionBase import ConnexionBase

class Main:
    def __init__(self):
        self.app = None
        self.db = ConnexionBase(r'C:\Users\Nam\Documents\S4\Programmation\Python\Tsena\tsena.accdb')
        self.db.connect()

    def lancer_application(self):
        root = tk.Tk()
        formulaire = Filtre(root)
        root.mainloop()
        
        selection = formulaire.get_selection()
        if selection:
            annee, mois = selection
            self.filtre(annee, mois)
            self.app = MaFenetre(annee, mois, self.db)
            self.app.run()

    def filtre(self, annee, mois):
        print(f"Filtrage pour l'année: {annee}, mois: {mois}")

if __name__ == "__main__":
    programme = Main()
    try:
        programme.lancer_application()
    finally:
        programme.db.close()