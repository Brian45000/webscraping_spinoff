from bs4 import BeautifulSoup

class Processor:
    def __init__(self, text):
        self.text = text

    def scraping_mois_en_cours(self):
        list_episodes = []

        soup = BeautifulSoup(
            self.text, "html.parser"
        )

        tds_jours = soup.find('div',id='calendrier').find_all('table')[1].find_all('td',class_='td_jour')
        for td_jour in tds_jours:
            # On test si le td est vide ou non
            if td_jour.text.strip() != '':
                # Récupération de la date de diffusion en découpant l'identifiant de la div
                div_date_diffusion = td_jour.find('div').get('id')
                date_diffusion = div_date_diffusion.split('_')[1]

                # Récupération des episodes du jour
                episodes = td_jour.find_all('span',class_='calendrier_episodes')
                for episode in episodes:
                    # On récupère l'attribut alt des deux images
                    images = episode.find_previous_siblings('img')
                    pays = images[1].get('alt')
                    chaine = images[0].get('alt')
                    
                    # On récupère les balises A 
                    details_episode = episode.find_all('a')
                    nom_serie = details_episode[0].text
                    numero_saison = details_episode[1].text.split('.')[0]
                    numero_episode = details_episode[1].text.split('.')[1]
                    url = details_episode[1].get('href')

                    # On rajoute nos résultats dans la liste des épisodes
                    list_episodes.append([nom_serie,numero_episode,numero_saison,date_diffusion,pays,chaine,url])

        return list_episodes
    
    #Fonction pour récupérer seulement la durée en minutes sur la page d'un épisode
    def scraping_detail_episode(self):
        soup = BeautifulSoup(
            self.text, "html.parser"
        )       
        return soup.find("div", class_="episode_infos_episode_format").text.split('m')[0].strip()
                        
            