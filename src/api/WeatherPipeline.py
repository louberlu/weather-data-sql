import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
from sqlalchemy import select, create_engine
from sqlalchemy import text, URL, Table, Column
from sqlalchemy import Sequence, Integer, TIMESTAMP
from sqlalchemy import Float, String, MetaData, ForeignKey

class WeatherPipeline:
    """Pipeline pour collecter, transformer et déposer les données météorologiques dans une base de données PostgreSQL.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    cle_api = None
    host = None
    user = None
    password = None
    port = None
    base = None
    url_BDD = None
    engine = None
    locations = None
    weathers = None
    tb_loc = None
    tb_weath = None
    metadata_obj = None
    url_meteo = None
    url_geo = None
        
    def __init__(self, path_env):
        """Initialise le pipeline météo en chargeant les variables d'environnement et en configurant les connexions à la base de données.

        Args:
            path_env (str): Le fichier .env avec son chemin complet
        """
        self.url_geo = "http://api.openweathermap.org/geo/1.0/direct"
        self.url_meteo = "https://api.openweathermap.org/data/2.5/weather"
        
        load_dotenv(dotenv_path=path_env)
        # Récupérer les variables d'environnement
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT")
        self.base = os.getenv("DB_NAME")
        self.cle_api = os.getenv("API_KEY_OPENWEATHER")
        
        self.url_BDD = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.base}"
                
        self.init_nb_json_file()
        
        self.metadata_obj = MetaData()
        self.tb_loc = "locations"
        self.tb_weath = "weathers"
        
        self.locations = Table(
            self.tb_loc,
            self.metadata_obj,
            Column("location_id", Integer, Sequence("location_id_seq"), primary_key=True),
            Column("country_name", String(100), nullable=False),
            Column("city", String(100), nullable=False),
            Column("country_code", String(2), nullable=False),
            Column("timezone", Integer, nullable=False),
            Column("lat", Float, nullable=False),
            Column("lon", Float, nullable=False)
        )

        self.weathers = Table(
            self.tb_weath,
            self.metadata_obj,
            Column("weather_id", Integer, Sequence("weather_id_seq"), primary_key=True),
            Column("main", String(20), nullable=False),
            Column("description", String, nullable=False),
            Column("temp", Float, nullable=False),
            Column("feels_like", Float, nullable=False),
            Column("temp_min", Float, nullable=False),
            Column("temp_max", Float, nullable=False),
            Column("pressure", Float, nullable=False),
            Column("humidity", Float, nullable=False),
            Column("visibility", Float, nullable=False),
            Column("wind_speed", Float, nullable=False),
            Column("clouds", Float, nullable=False),
            Column("rain", Float),
            Column("snow", Float),
            Column("observation_time", TIMESTAMP, nullable=False),
            Column("sunrise", TIMESTAMP, nullable=False),
            Column("sunset", TIMESTAMP, nullable=False),
            Column("location_id", None, ForeignKey("locations.location_id"), nullable=False)
        )
        
        self.init_connexion()
    
    def init_connexion(self) :
        """Initialise la connexion à la base de données.
        """
        self.engine = create_engine(self.url_BDD)
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print(f"Connexion établie sur {self.host} avec l'utilisateur {self.user}.")
        except Exception as e:
            print(f"Échec de la connexion à la base de données : {e}")
    
    def init_table(self):
        """Initialise les tables dans la base de données.
        """
        try :
            self.metadata_obj.create_all(self.engine)
            print(f"Les tables {self.tb_loc} et {self.tb_weath} ont été créé dans la base de donnée {self.base}.")
        except Exception as e:
            print(f"Échec de la création des tables : {e}")
    
    def init_nb_json_file(self):
        """Initialise le compteur de fichiers JSON.
        """
        conf = {
                'nb_json_file' : 0
            }
            
        with open("conf.json", "w") as json_file:
            json.dump(conf, json_file, indent=4)
    
    def collecte(self, city, country_code):
        """Collecte les données météorologiques pour une ville donnée.

        Args:
            city (str): Nom de la ville pour laquelle collecter les données météorologiques
            country_code (str): Code du pays

        Returns:
            dict: Fichier JSON contenant les données météorologiques collectées
        """
        # Appel API pour les coordonnées de la ville
        params_city = {
            'q': city+','+country_code,
            'appid': self.cle_api
        }

        r_city = requests.get(self.url_geo, params=params_city)

        # Appel de l'API pour les informations météo d'une ville 
        p_weather_city = {
            'lat': r_city.json()[0]['lat'],
            'lon': r_city.json()[0]['lon'],
            'appid': self.cle_api
        }
        
        r_meteo_city = requests.get(self.url_meteo, params=p_weather_city)

        d_city = r_meteo_city.json()

        with open("conf.json", "r") as json_file :
            conf = json.load(json_file)

        filename = "api_data"
        if conf['nb_json_file'] == 0:
            filename = "api_data.json"
        else:
            filename = filename + str(conf['nb_json_file']) +".json"
            
        cpt = conf['nb_json_file'] + 1
        conf = {
                'nb_json_file' : cpt
            }
            
        with open("conf.json", "w") as json_file:
            json.dump(conf, json_file, indent=4)

        print(f"Le fichier {filename} va être créer")
        
        with open(filename, "x") as json_file:
            json.dump(d_city, json_file, indent=4)
            
        print(f"Le fichier {filename} a été créé")
        return d_city
    
    def transformer(self, f_json, city, country, df_updated : pd.DataFrame | None = None) :
        """Transforme les données météorologiques collectées.

        Args:
            f_json (dict): Fichier JSON contenant les données météorologiques collectées
            city (str): Nom de la ville pour laquelle transformer les données
            country (str): Nom du pays
            df_updated (pd.DataFrame | None, optional): DataFrame mis à jour. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame contenant les données météorologiques transformées
        """
        df_weather = pd.read_json(f_json, orient="columns", typ="series")
        rain = None
        snow = None
        
        if "rain" in df_weather.index:
            rain = df_weather["rain"]

        if "snow" in df_weather.index:
            snow = df_weather["snow"]
        
        dc_weather = {
            "main" : df_weather["weather"][0]['main'],
            "description" : df_weather["weather"][0]['description'],
            "temp" : df_weather["main"]['temp'],
            "feels_like" : df_weather["main"]['feels_like'],
            "temp_min" : df_weather["main"]['temp_min'],
            "temp_max" : df_weather["main"]['temp_max'],
            "pressure" : df_weather["main"]['pressure'],
            "humidity" : df_weather["main"]['humidity'],
            "visibility" : df_weather["visibility"],
            "wind_speed" : df_weather["wind"]['speed'],
            "clouds" : df_weather["clouds"]['all'],
            "rain" : rain,
            "snow" : snow,
            "date" : df_weather["dt"],
            "sunrise" : df_weather["sys"]['sunrise'],
            "sunset" : df_weather["sys"]['sunset'],
            "country_name" : country,
            "country_code" : df_weather["sys"]['country'],
            "city" : city,
            "timezone" : df_weather["timezone"],
            "lat" : df_weather["coord"]['lat'],
            "lon" : df_weather["coord"]['lon']
        }

        df = pd.DataFrame(dc_weather, index=[0])
        
        # Conversion des dates en format lisible
        df['date'] = pd.to_datetime(df['date'], unit='s')
        df['sunrise'] = pd.to_datetime(df['sunrise'], unit='s')
        df['sunset'] = pd.to_datetime(df['sunset'], unit='s')
        
        if df_updated is not None :
            df = pd.concat([df_updated, df], ignore_index=True)
        
        return df
    
    def ville_id(self, city):
        """Récupère l'identifiant d'une ville dans la base de données.

        Args:
            city (str): Le nom de la ville dont on recherche l'id dans la base de données

        Raises:
            Exception: _description_

        Returns:
            int: L'identifiant de la ville
        """
        try :
            with self.engine.connect() as connection:
                s = select(self.locations.c.location_id).where(self.locations.c.city == city)
                result = connection.execute(s)
            line = result.fetchone();
            if line is not None and len(line) > 0:
                return line[0]
            else:
                print(f"La ville de '{city}' n'est pas présente dans la base")
                raise Exception
        except Exception as e :
            print(f"Échec de la sélection : {e}")
    
    def ville_presente(self, city):
        """Vérifie si une ville est présente dans la base de données.

        Args:
            city (Str): Nom de la ville à vérifier dans la base de données

        Returns:
            bool: True si la ville est présente, False sinon
        """
        try :
            with self.engine.connect() as connection:
                s = select(self.locations.c.location_id).where(self.locations.c.city == city)
                result = connection.execute(s)
            line = result.fetchone();
            if line is not None :
                return True
            else:
                return False
        except Exception as e :
            print(f"Échec de la sélection : {e}")

    def depot_sql(self, df):
        """Cette méthode effectue les insertions dans les tables de la base de données.

        Args:
            df (DataFrame): Le dataFrame contenant les données météos devant être déposer 
            dans la base de données
        """
        # Insertion dans la table locations
        for i in range(len(df)):
            city = df.loc[i]['city']
            
            if not self.ville_presente(city):
                try :
                    ins = self.locations.insert().values(
                        country_name = df.loc[i]["country_name"],
                        country_code = df.loc[i]["country_code"],
                        city = df.loc[i]["city"],
                        timezone = df.loc[i]["timezone"],
                        lat = df.loc[i]["lat"],
                        lon = df.loc[i]["lon"])
                    
                    print(f"Insertion dans la base de donnée {self.base}...\n......\n") 
                    print(ins.compile().params,"\n")
                    
                    with self.engine.begin() as connection:
                        print("...Insertion en cours...")
                        print(str(ins),"\n")
                        connection.execute(ins)
                    print(f"... Les données ont été inséré dans la table 'locations' de la base de donnée {self.base}")
                except Exception as e :
                    print(f"Échec de l'insertion : {e}")

            loc_id = self.ville_id(city)

            # Insertion dans la table weathers  
            try:
                rain = df.loc[i]["rain"]
                snow = df.loc[i]["snow"]
                if rain != None:
                    rain = float(rain)

                if snow != None:
                    snow = float(snow)
                
                ins = self.weathers.insert().values(
                    main = df.loc[i]["main"],
                    description = df.loc[i]["description"],
                    temp = float(df.loc[i]["temp"]),
                    feels_like = float(df.loc[i]["feels_like"]),
                    temp_min = float(df.loc[i]["temp_min"]),
                    temp_max = float(df.loc[i]["temp_max"]),
                    pressure = float(df.loc[i]["pressure"]),
                    humidity = float(df.loc[i]["humidity"]),
                    visibility = float(df.loc[i]["visibility"]),
                    wind_speed = float(df.loc[i]["wind_speed"]),
                    clouds = float(df.loc[i]["clouds"]),
                    rain = rain,
                    snow = snow,
                    observation_time = df.loc[i]["date"],
                    sunrise = df.loc[i]["sunrise"],
                    sunset = df.loc[i]["sunset"],
                    location_id = loc_id)
                
                print(f"Insertion dans la base de donnée {self.base}...\n......\n") 
                print(ins.compile().params,"\n")
                
                with self.engine.begin() as connection:
                    print("...Insertion en cours...")
                    print("\n",str(ins),"\n")
                    connection.execute(ins)
                    
                print(f"... Les données ont été inséré dans la table 'weathers' de la base de donnée {self.base}")
            except Exception as e :
                print(f"Échec de l'insertion : {e}")

if __name__ == "__main__":
    pass