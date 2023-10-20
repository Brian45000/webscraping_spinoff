# Avec la syntaxe from ... import ... on import un seul  objet
from database_sqlite import DatabaseSQLITE
from database_postgresql import DatabasePOSTGRESQL
from moteur_csv import MoteurCSV
from retriever import Retriever
from processor import Processor
import pprint
import sys
import calendar
from datetime import datetime, timedelta
from main import main


date_actuelle = datetime.now()

# Obtenez l'année en cours
annee_en_cours = date_actuelle.year
mois = sys.argv[2]
print(mois)

# Construisez la date du premier jour du mois sélectionné
premier_jour_mois = datetime(annee_en_cours, int(mois), 1)

# Obtenez le dernier jour du mois en cours
dernier_jour_mois = premier_jour_mois.replace(day=calendar.monthrange(annee_en_cours, int(mois))[1])

# Formatez les dates
premier_jour_mois_formatte = premier_jour_mois.strftime("%d-%m-%Y")
dernier_jour_mois_formatte = dernier_jour_mois.strftime("%d-%m-%Y")

main(annee_en_cours, int(mois), premier_jour_mois_formatte, dernier_jour_mois_formatte)
