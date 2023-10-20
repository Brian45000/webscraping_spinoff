import psycopg2
from collections import Counter
import pprint

class DatabasePOSTGRESQL:
    def __init__(self, url):
        self.conn = psycopg2.connect(url)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        try:
            columns_str = ', '.join(columns)
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)

    def insert_data(self, table_name, value_names, data):
        try:
            placeholders = ', '.join(['%s'] * len(data))
            value_names = ', '.join(value_names)
            self.cursor.execute(f"INSERT INTO {table_name} ({value_names}) VALUES ({placeholders})", data)
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)

    def count_episodes_by_field(self, field_name , premier_jour_mois, dernier_jour_mois):
        try:
            query = f"SELECT {field_name}, COUNT(*) AS episode_count FROM episode WHERE TO_DATE(date_diffusion, 'DD-MM-YYYY') BETWEEN TO_DATE('{premier_jour_mois}', 'DD-MM-YYYY') AND TO_DATE('{dernier_jour_mois}', 'DD-MM-YYYY') GROUP BY {field_name} ORDER BY episode_count DESC;"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return []

    def count_10_words_name(self, premier_jour_mois, dernier_jour_mois):
        try:
            query = f"SELECT DISTINCT nom_serie from episode WHERE TO_DATE(date_diffusion, 'DD-MM-YYYY') BETWEEN TO_DATE('{premier_jour_mois}', 'DD-MM-YYYY') AND TO_DATE('{dernier_jour_mois}', 'DD-MM-YYYY');"
            self.cursor.execute(query)
            list_name = self.cursor.fetchall()
            
            # On concatène tout les noms de série pour utiliser la fonction counter par la suite, 
            # et ensuite most_common qui permet de récupérer les mots les plus communs
            all_name = ' '.join([name[0].lower() for name in list_name ])
            word_counter = Counter(all_name.split()).most_common(10)

            return word_counter
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return []


    def fetch_data(self, table_name, condition=None):
        try:
            if condition:
                self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
            else:
                self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(e)


    def close(self):
        self.cursor.close()
        self.conn.close()
