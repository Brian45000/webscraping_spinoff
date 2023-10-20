# Avec la syntaxe from ... import ... on import un seul  objet
from database_sqlite import DatabaseSQLITE
from database_postgresql import DatabasePOSTGRESQL
from moteur_csv import MoteurCSV
from retriever import Retriever
from processor import Processor
import pprint
from datetime import datetime, timedelta



def main(annee_en_cours='2023', mois='10', premier_jour_mois='01-10-2023', dernier_jour_mois='31-10-2023'):
    
    #Création des instances BD
    URL_DBK = "postgres://course_pyth_5215:XVDByby-rbC0qWQ0m1xO@course-pyth-5215.postgresql.a.osc-fr1.scalingo-dbs.com:33698/course_pyth_5215?sslmode=prefer"
    instance_bdd_ps = DatabasePOSTGRESQL(URL_DBK)
    instance_bdd_sl = DatabaseSQLITE("database.db")

    #Création d'une instance pour csv
    instance_csv = MoteurCSV("data/files/episodes.csv")


    # Récupération de la page (Scraping 1/2)
    url = f"https://www.spin-off.fr/calendrier_des_series.html?date={annee_en_cours}-{mois}"

    # Récupération du code source de la page
    retriever_instance = Retriever(url=url)
    ps = retriever_instance.get_page_source()

    # Création de l'instance processor
    processor_instance = Processor(text=ps)
    scraping_mois_en_cours = processor_instance.scraping_mois_en_cours()

    # Fichiers CSV : 
    instance_csv.write_episode(scraping_mois_en_cours)
    instance_csv.read_without_libraries()


    print('------------------------------------------------------------------------------------------------------')
    print('-------------------Création des tables dans les base de données en cours -------------------------')
    # SQL création des tables avec les bonnes colonnes dans nos deux bases de données
    episode_table_columns_sl = [
        "id INTEGER PRIMARY KEY",
        "nom_serie TEXT",
        "numero_episode INTEGER",
        "numero_saison INTEGER",
        "date_diffusion TEXT",
        "pays TEXT",
        "chaine_diffusion TEXT",
        "url TEXT"
    ]
    episode_table_columns_ps = [
        "id SERIAL PRIMARY KEY",
        "nom_serie TEXT",
        "numero_episode INTEGER",
        "numero_saison INTEGER",
        "date_diffusion TEXT",
        "pays TEXT",
        "chaine_diffusion TEXT",
        "url TEXT"
    ]

    instance_bdd_sl.create_table("episode", episode_table_columns_sl)
    instance_bdd_ps.create_table("episode", episode_table_columns_ps)

    duration_table_columns_sl = [
        "id INTEGER PRIMARY KEY",
        "duree INTEGER",
        "episode_id INTEGER",
        "FOREIGN KEY (episode_id) REFERENCES episode(id)"
    ]
    duration_table_columns_ps = [
        "id SERIAL PRIMARY KEY",
        "duree INTEGER",
        "episode_id INTEGER",
        "FOREIGN KEY (episode_id) REFERENCES episode(id)"
    ]
    instance_bdd_sl.create_table("duration", duration_table_columns_sl)
    instance_bdd_ps.create_table("duration", duration_table_columns_ps)


    # Insertion des episodes dans les bases de données 
    # Récupération des colonnes à utiliser pour l'insertion en base
    episode_table_columns = [column.split()[0] for column in episode_table_columns_ps if column.split()[0] != 'id']
    print('------------------------------------------------------------------------------------------------------')
    print('-------------------Insertions des épisodes dans les base de données en cours -------------------------')
    for episode in scraping_mois_en_cours:
        instance_bdd_sl.insert_data("episode", episode_table_columns, episode)
        instance_bdd_ps.insert_data("episode", episode_table_columns, episode)

    print('------------------------------------------------------------------------------------------------------')
    print('--------------------------- Statistiques des épisodes ( Algorithmie 1/2 ) ----------------------------')
    ## Algorithmie 
    count_by_chaine = instance_bdd_ps.count_episodes_by_field('chaine_diffusion', premier_jour_mois, dernier_jour_mois)
    pprint.pprint(count_by_chaine)
    count_by_pays = instance_bdd_ps.count_episodes_by_field('pays', premier_jour_mois, dernier_jour_mois)
    pprint.pprint(count_by_pays)
    count_10_words = instance_bdd_ps.count_10_words_name(premier_jour_mois, dernier_jour_mois)
    pprint.pprint(count_10_words)

    print('-----------------------------------------------------------------------------------------------------')
    print('--------------------------------Récupération des durées en cours ------------------------------------')
    #Scrapping 2/2 et SQL 2/2
    liste_episodes_AppleTV = instance_bdd_ps.fetch_data('episode', f"chaine_diffusion = 'Apple TV+' AND TO_DATE(date_diffusion, 'DD-MM-YYYY') BETWEEN TO_DATE('{premier_jour_mois}', 'DD-MM-YYYY') AND TO_DATE('{dernier_jour_mois}', 'DD-MM-YYYY')")
    liste_duration=[]
    for episode in liste_episodes_AppleTV: 
        id_episode = episode[0]
        retriever_instance = Retriever("https://www.spin-off.fr/"+episode[7])
        ps = retriever_instance.get_page_source()
        processor_instance = Processor(text=ps)
        duration = processor_instance.scraping_detail_episode()
        liste_duration.append([duration,id_episode])


    print('-----------------------------------------------------------------------------------------------------')
    print('-------------------Insertions des durées dans la base de données en cours ---------------------------')
    #On Ajoute en base les durées 
    for duration in liste_duration:
        duree =  str(duration[0]) if duration[0] != '' else '0'
        episode_id = str(duration[1])
        instance_bdd_ps.insert_data("duration", ['duree','episode_id'], [duree, episode_id])
        instance_bdd_sl.insert_data("duration", ['duree','episode_id'], [duree, episode_id])



    print('-----------------------------------------------------------------------------------------------------')
    print('------------------------------- Algorithmie 2/2 Nb jour consecutif ----------------------------------')
    #Algorithmie 2/2
    instance_bdd_ps.cursor.execute(f"SELECT distinct date_diffusion, chaine_diffusion FROM episode WHERE TO_DATE(date_diffusion, 'DD-MM-YYYY') BETWEEN TO_DATE('{premier_jour_mois}', 'DD-MM-YYYY') AND TO_DATE('{dernier_jour_mois}', 'DD-MM-YYYY') ORDER BY chaine_diffusion ASC, date_diffusion ASC")
    liste_date_episodes = instance_bdd_ps.cursor.fetchall()

    resultat = {}
    # Date tampon pour calcul 
    date_tmp= None
    for date, chaine in liste_date_episodes:
        # On format la date en format date D-M-Y
        dateFormat = datetime.strptime(date, "%d-%m-%Y")
        if chaine in resultat:
            if date_tmp + timedelta(days=1) == dateFormat:
                resultat[chaine] += 1
            else: 
                 resultat[chaine] = 1
        else:
            resultat[chaine] = 1
        date_tmp = dateFormat

    #On trie le dictionnaire
    sortedDict = sorted(resultat.items(), key=lambda x:x[1])
    
    #Résultat TF1 avec 5 jours consecutifs 
    print(f"La chaîne de TV qui diffuse des épisodes pendant le plus grand nombre de jours consécutifs sur le mois {mois} est ",sortedDict[-1])



if __name__ == "__main__":
    main()
