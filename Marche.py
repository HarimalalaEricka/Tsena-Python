from ConnexionBase import ConnexionBase

class Marche:
    def __init__(self, IdMarche, Nom, IdLoyer):
        self.IdMarche = IdMarche
        self.Nom = Nom
        self.IdLoyer = IdLoyer

    def getAllMarche(db):
        results = db.execute_query('SELECT * FROM Marche')
        marches = []
        if results:
            for row in results:
                IdMarche, nom, id_loyer = row
                marche = Marche(IdMarche, nom, id_loyer)
                marches.append(marche)

        return marches

    def __str__(self):
        return f"Marche(Nom={self.Nom}, IdLoyer={self.IdLoyer})"

    def getDimensionById(self, IdBox, db):
        query = '''Select * from (SELECT IdMarche, SUM(Longueur+1) , MAX(Largeur+0.5)  FROM Box GROUP BY IdMarche) where IdMarche = ?;'''
        results = db.execute_query(query, (IdBox,))
        return results

# Point d'entrée du programme
if __name__ == "__main__":
    results = Marche.getDimensionById(1)
    print(results[0][0])
    # Récupérer tous les marchés depuis la base de données
    # marches = Marche.getAllMarche()

    # # Afficher les marchés
    # if marches:
    #     print("Liste des marchés :")
    #     for marche in marches:
    #         print(marche)
    # else:
    #     print("Aucun marché trouvé dans la base de données.")