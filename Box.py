from ConnexionBase import ConnexionBase

class Box:
    def __init__(self, IdBox, Longueur, Largeur, IdMarche, Personne, Couleur="grey"):
        self.IdBox = IdBox
        self.Longueur = Longueur
        self.Largeur = Largeur
        self.IdMarche = IdMarche
        self.Personne = Personne
        self.Couleur = Couleur

    def getAllBox(db):
        results = db.execute_query('SELECT * FROM Box')
        box = []
        if results:
            for row in results:
                IdBox, longueur, largeur, IdMarche, Personne = row
                boxes = Box(IdBox, longueur, largeur, IdMarche, Personne)
                box.append(boxes)
        return box
    
    def getLoyerAPayer(self, Mois, Annee, db):
        query = '''SELECT b.IdBox, b.Longueur, b.Largeur, a.Debut, a.Fin, a.Loyer
                   FROM (Box AS b
                   INNER JOIN Marche AS m ON b.IdMarche = m.IdMarche)
                   INNER JOIN Loyer AS a ON m.IdLoyer = a.IdLoyer
                   WHERE b.IdBox = ? 
                   AND a.Debut <= ? AND a.Fin >= ?;'''
        start_date = f'{Annee}-{Mois:02d}-01'
        end_date = f'{Annee}-{Mois:02d}-{self.get_last_day_of_month(Mois, Annee)}'
        results = db.execute_query(query, (self.IdBox, end_date, start_date))
        loyerApayer = 0
        if results:
            for row in results:
                IdBox, longueur, largeur, debut, fin, loyer = row
                surface = longueur * largeur    
                loyerApayer = surface * loyer
        return loyerApayer

    def get_last_day_of_month(self, Mois, Annee):
        if Mois in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif Mois in [4, 6, 9, 11]:
            return 30
        elif Mois == 2:
            if (Annee % 4 == 0 and Annee % 100 != 0) or (Annee % 400 == 0):
                return 29
            else:
                return 28
        return 30

    def getLoyerDejaPayer( self, Mois, Annee, db):
        query = '''SELECT mois, annee, sum(MontantPaye) as mpaye from Paiement where idBox = ? and mois = ? and annee = ? group by mois, annee;'''
        results = db.execute_query(query, (self.IdBox, Mois, Annee))
        loyerDejaPayer = 0
        if results:
            for row in results:
                mois, annee, mpaye = row
                loyerDejaPayer = mpaye
        return loyerDejaPayer

    def getResteLoyerAPayer(self, Mois, Annee, db):
        aPayer = self.getLoyerAPayer( Mois, Annee, db)
        dejaPayer = self.getLoyerDejaPayer( Mois, Annee, db)
        Reste = aPayer - dejaPayer
        return Reste

    def Filtre(self, Mois, Annee, db):
        aPayer = self.getLoyerAPayer(Mois, Annee, db)
        dejaPayer = self.getLoyerDejaPayer(Mois, Annee, db)
        Reste = aPayer - dejaPayer
        print(Reste)
        if aPayer > 0:
            pourcentage_reste = (Reste / aPayer) * 100
        else:
            pourcentage_reste = 0  

        return pourcentage_reste
    
    def getBoxById(IdBox, db):
        query = 'SELECT * FROM Box WHERE IdBox = ?'
        results = db.execute_query(query, (IdBox,))
        if results:
            row = results[0]
            IdBox, longueur, largeur, IdMarche, Personne = row
            return Box(IdBox, longueur, largeur, IdMarche, Personne)
        return None

    def __str__(self):
        return f"Box({self.IdBox}, {self.Longueur}, {self.Largeur}, {self.IdMarche}, {self.Personne})"