import csv
import pprint

class MoteurCSV:
    def __init__(self, file_path):
        self.file_path = file_path

    # Fonction pour écrire dans un fichier avec un délimiter ; et en utf8
    def write(self, data):
        try:
            with open(self.file_path, 'a', encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(data)
            print("Données ajoutées avec succès au fichier CSV.")
        except Exception as e:
            print(f"Erreur lors de l'ajout des données au fichier CSV : {e}")

    # Fonction pour écrire tous les épisodes dans notre fichier en appelant la fonction write
    def write_episode(self,liste_episodes):
        for episode in liste_episodes:
            self.write(episode)

    # Fonction pour récuperer les lignes dans un fichier sans utiliser de librairie
    def read_without_libraries(self):
        resultats = []
        file = open(self.file_path,"r")
        lines = file.readlines()
        for line in lines:
            data = line.split(';')
            resultats.append((data[0],data[1],data[2],data[3],data[4],data[5],data[6])) 
        pprint.pprint(resultats)