import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from Marche import Marche  
from Box import Box  
from FormulairePaiement import FormulairePaiement

class MaFenetre:
    def __init__(self, annee, mois, db):
        self.annee = annee
        self.mois = mois
        self.db = db

        self.fenetre = tk.Tk()
        self.fenetre.title("Antananarivo")
        self.fenetre.geometry("1200x800")
        self.fenetre.configure(bg="white")

        self.canvas = tk.Canvas(self.fenetre, bg="lightblue", width=1200, height=800)
        self.canvas.pack()

        self.bouton_payer = tk.Button(self.fenetre, text="Payer le loyer", command=self.ouvrir_formulaire_paiement)
        self.bouton_payer.place(x=1100, y=10)  

        self.dessiner_marches_et_box()

    def dessiner_marches_et_box(self):
        self.canvas.delete("all")  

        echelle = 50
        Marches = Marche.getAllMarche(self.db)
        marche_coords = {}
        x = 10
        y = 10
        for marche in Marches:
            Longueur = float(marche.getDimensionById(marche.IdMarche, self.db)[0][1]) * echelle
            Largeur = float(marche.getDimensionById(marche.IdMarche, self.db)[0][2]) * echelle
            # Largeur = Longueur
            self.dessiner_rectangle(x, y, Longueur, Largeur, "pink", f"")
            marche_coords[marche.IdMarche] = (x, y, Longueur, Largeur)
            y += Largeur + 20

        boxes = Box.getAllBox(self.db)
        for box in boxes:
            pourcentage_reste = box.Filtre(int(self.mois), int(self.annee), self.db)
            pourcentage_paye = 100 - pourcentage_reste
            
            Longueur = float(box.Longueur) * echelle
            Largeur = float(box.Largeur) * echelle
            marche_id = box.IdMarche
            if marche_id in marche_coords:
                mx, my, mLongueur, mLargeur = marche_coords[marche_id]
                x1 = mx + 10  
                y1 = my + 10
                longueur_paye = Longueur * (pourcentage_paye / 100)
                self.dessiner_rectangle(x1, y1, longueur_paye, Largeur, "green", f"")
                x2 = x1 + longueur_paye
                longueur_reste = Longueur * (pourcentage_reste / 100)
                self.dessiner_rectangle(x2, y1, longueur_reste, Largeur, "red", f"")
                x_centre = x1 + (Longueur / 2)
                y_centre = y1 + (Largeur / 2)
                self.ecrire_texte(x_centre, y_centre, f"{box.IdBox}")
                marche_coords[marche_id] = (mx + Longueur + 10, my , mLongueur, mLargeur)

    def dessiner_rectangle(self, x1, y1, x2, y2, couleur, label):
        self.canvas.create_rectangle(
            x1, y1,  
            x1 + x2, y1 + y2,  
            fill=couleur,  
            outline="black",  
            width=2
        )
        self.canvas.create_text(
            x1 + x2 / 2, y1 + y2 / 2,  
            text=label,  
            fill="black"
        )

    def ouvrir_formulaire_paiement(self):
        fenetre_paiement = tk.Toplevel(self.fenetre)
        FormulairePaiement(fenetre_paiement, self, self.db)
    
    def ecrire_texte(self, x, y, texte, couleur="black"):
        self.canvas.create_text(x, y, text=texte, fill=couleur, font=("Arial", 12, "bold"))


    def actualiser(self):
        self.dessiner_marches_et_box()

    def run(self):
        """Lance la boucle principale de l'interface."""
        self.fenetre.mainloop()
