import pyodbc

class ConnexionBase:
    def __init__(self, db_path):
        """
        Initialise la connexion à la base de données Access.
        
        :param db_path: Chemin vers le fichier de base de données Access (.accdb ou .mdb)
        """
        self.db_path = db_path
        self.conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_path + ';'
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Établit la connexion à la base de données.
        """
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
            print("Connexion à la base de données réussie.")
        except pyodbc.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            print(f"Code d'erreur : {e.args[0]}")
            print(f"Message d'erreur : {e.args[1]}")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Erreur : Aucune connexion à la base de données.")
            return None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Vérifie si la requête est une requête de type SELECT
            if query.strip().upper().startswith("SELECT"):
                # print("Requête SELECT exécutée avec succès.")
                return self.cursor.fetchall()
            else:
                # Pour les requêtes INSERT, UPDATE, DELETE, on commit les changements
                self.connection.commit()
                # print("Requête exécutée avec succès (pas de résultats à retourner).")
                return None

        except pyodbc.Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return None

    def commit(self):
        """
        Valide les modifications dans la base de données.
        """
        try:
            self.connection.commit()
            # print("Modifications validées avec succès.")
        except pyodbc.Error as e:
            print(f"Erreur lors de la validation des modifications : {e}")
            print(f"Code d'erreur : {e.args[0]}")
            print(f"Message d'erreur : {e.args[1]}")

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            # print("Connexion à la base de données fermée.")
        except pyodbc.Error as e:
            print(f"Erreur lors de la fermeture de la connexion : {e}")
            print(f"Code d'erreur : {e.args[0]}")
            print(f"Message d'erreur : {e.args[1]}")

# # Exemple d'utilisation de la classe
# if __name__ == "__main__":
#     # Chemin vers la base de données Access
#     db_path = r'C:\Users\Nam\Documents\S4\Programmation\Python\Tsena\tsena.accdb'

#     # Création d'une instance de la classe AccessDatabase
#     db = ConnexionBase(db_path)

#     # Connexion à la base de données
#     db.connect()

#     # Exécution d'une requête SELECT
#     results = db.execute_query('SELECT * FROM Etudiant')
#     if results:
#         for row in results:
#             print(row)

#     # Exécution d'une requête INSERT avec paramètres
#     insert_query = "INSERT INTO Etudiant (Etudiant, Semestre) VALUES (?, ?)"
#     db.execute_query(insert_query, ('Carène', 'S6'))
#     db.commit()  # Valider les modifications

#     # Fermeture de la connexion
#     db.close()