from ConnexionBase import ConnexionBase
from Box import Box
from datetime import datetime

class Paiement:
    def __init__(self, IdBox, mois, Annee, DatePaie):
        self.IdBox = IdBox
        self.mois = mois
        self.Annee = Annee
        self.DatePaie = DatePaie

    def InsertPaiement(box, Montant, db):
        mois = 0
        annee = 0
        query = '''SELECT mois, annee FROM Paiement WHERE idBox = ?;'''
        query1 = '''INSERT INTO Paiement(IdBox, Mois, Annee, DatePaie, MontantPaye) VALUES(?, ?, ?, ?, ?);'''
        current_datetime = datetime.now().strftime("%d/%m/%Y")
        results = db.execute_query(query, (box.IdBox,))
        if results:
            derniere_ligne = results[-1]  
            mois = derniere_ligne[0] 
            annee = derniere_ligne[1]
            if box.getResteLoyerAPayer(mois, annee, db) == 0:
                if mois == 12:
                    mois = 1
                    annee += 1
                else:
                    mois += 1
                    annee = derniere_ligne[1] 

                loyer_a_payer = box.getLoyerAPayer(mois, annee, db)
                if loyer_a_payer >= Montant:
                    db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, Montant))
                else:
                    db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, loyer_a_payer))
                reste = Montant - loyer_a_payer
                if reste > 0:
                    if reste  != Montant:
                        Paiement.InsertPaiement(box, reste, db)
                else:
                    return
            elif box.getResteLoyerAPayer(mois, annee, db) > 0:
                loyer_restant = box.getResteLoyerAPayer(mois, annee, db)
                if loyer_restant >= Montant:
                    db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, Montant))
                else:
                    db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, loyer_restant))
                reste = Montant - loyer_restant
                if reste > 0:
                    if reste  != Montant:
                        Paiement.InsertPaiement(box, reste, db)
                else:
                    return
        else:
            # If no previous payments, start with the current month and year
            mois = 1
            annee = 2024
            loyer_a_payer = box.getLoyerAPayer(mois, annee, db)
            if loyer_a_payer >= Montant:
                db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, Montant))
            else:
                db.execute_query(query1, (box.IdBox, mois, annee, current_datetime, loyer_a_payer))
            reste = Montant - loyer_a_payer
            if reste > 0:
                if reste  != Montant:
                    Paiement.InsertPaiement(box, reste, db)
            else:
                return

        db.commit()

if __name__ == "__main__":
    box = Box(4, 10, 10, 1, "Alice") 
    Paiement.InsertPaiement(box, 200000)