from .jsonService import JsonService
import datetime
import random
import math

class LocationService():
    
    ocean_locations = {
    "Atlantic Ocean": {
        "lat_range": (-60.0, 80.0),  
        "lon_range": (-80.0, 20.0)   
    },
    "Pacific Ocean": {
        "lat_range": (-60.0, 60.0),  
        "lon_range": (-180.0, -60.0)
    },
    "Indian Ocean": {
        "lat_range": (-60.0, 10.0),  
        "lon_range": (20.0, 150.0)   
    },
    "Southern Ocean": {
        "lat_range": (-90.0, -60.0),  
        "lon_range": (-180.0, 180.0)  
    },
    "Arctic Ocean": {
        "lat_range": (60.0, 90.0),   
        "lon_range": (-180.0, 180.0) 
    },
    "Southern Ocean (Antarctic)": {
        "lat_range": (-90.0, -60.0),  
        "lon_range": (-180.0, 180.0)  
    },
    "Antarctic Ocean": {
        "lat_range": (-90.0, -60.0),  
        "lon_range": (-180.0, 180.0)  
    }
}

    @staticmethod
    def _get_last_agent(filename: str, identifier: str):
      """
      Busca o último agente no log JSON com o identificador fornecido e
      retorna o agente com o timestamp mais recente.
      """    
      try:
        agents = JsonService.load_json(filename)
        agent_load = [agent for agent in agents if agent['identifier'] == identifier]
        if not agent_load:
            return {
                "success": False,
                "data": {},
                "error": "Agente não encontrado."
            }
        #Ordena os agentes encontrados pelo timestamp
        agent_load.sort(key=lambda agent: 
                        datetime.datetime.strptime(agent['metadata']['timestamp'],
                                                    "%Y-%m-%d %H:%M:%S"), reverse=True)
        return {
              "success": True,
              "data": agent_load[0], 
              "error": "" 
        }
        
      except Exception as e:
          return {
              "success": False,
              "data": e,
              "error": "Agente não encontrado."
          }
    
    @staticmethod
    def _calculate_new_coordinate(latitude: float, longitude: float, 
                                  speed: float, time: float):
      """
      Calcula as novas coordenadas baseadas na velocidade do agente e no tempo decorrido.
      """ 
      distance = speed * time  # Distância em km
      print(f"Debug: A ultima coleta aconteceu faz {time} horas")
      
      delta_latitude = distance / 111.0  # 1 grau ~= 111km
      delta_longitude = distance / (111.0 * math.cos(math.radians(latitude)))

      # Define uma direção aleatória entre -180 e 180 graus
      direction = random.uniform(-180, 180)

      # Calcula as novas coordenadas
      new_latitude = latitude + delta_latitude * math.cos(math.radians(direction))
      new_longitude = longitude + delta_longitude * math.sin(math.radians(direction))

      return new_latitude, new_longitude

    @staticmethod
    def _get_location_coordinates(agent: dict, time: str, ocean_locations: dict):
      """
      Se o agente não tiver uma localização no metadata,
      sorteia uma localização aleatória e retorna o nome do oceano.
      Caso contrário, retorna a localização do agente. 
      """
      if agent:        
        agent_type = agent.get("agent_type")
        ocean_name = agent.get("location")
        geolocation = agent.get("geolocation", {})
    
        latitude = geolocation.get("latitude")
        longitude = geolocation.get("longitude")

        if latitude is not None and longitude is not None:
                  
          if agent_type == "Ship":
            speed = 30  # Velocidade média de um navio em km/h
          elif agent_type == "Drone":
            speed = 80  # Velocidade média de um drone em km/h
          
          
          new_latitude, new_longitude = LocationService._calculate_new_coordinate(
              latitude, longitude, speed, float(time)
          )

        return new_latitude, new_longitude, ocean_name
      else:
        #Escolhendo um oceano aleatóriamente do dicionário
        ocean_name = random.choice(list(ocean_locations.keys()))
        
        lat_min, lat_max = ocean_locations[ocean_name]["lat_range"]
        lon_min, lon_max = ocean_locations[ocean_name]["lon_range"]

        latitude = random.uniform(lat_min, lat_max)  
        longitude = random.uniform(lon_min, lon_max)  

      return latitude, longitude, ocean_name
    
    @staticmethod
    def locationService(identifier: str):
        """
        Recupera a localização do agente com o identificador fornecido e
        monta o metadata.
        """
        try:
            # Recupera o último agente
            agent = LocationService._get_last_agent(
                'app/database/storage.json', identifier
            )
            
            if not agent['success']:
                return {
                    "success": False,
                    "error": agent['error']
                }
            
            ocean_locations = LocationService.ocean_locations
            agent_type = agent.get('data', {}).get('metadata', {}).get('agent_type')
            last_timestamp = agent.get('data', {}).get('metadata', {}).get('timestamp')
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            # Calcula a diferença de tempo em horas (usando o timestamp atual)
            if last_timestamp:
                time_diff = (datetime.datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S") - 
                            datetime.datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600
            else:
                time_diff = 0  # Se não houver timestamp, não calcula a diferença de tempo
            
            latitude, longitude, ocean_name = LocationService._get_location_coordinates(
                agent['data']['metadata'], time_diff, ocean_locations
            )
            
            # Montando o novo metadata
            metadata = {
                "agent_type": agent_type,
                "timestamp": current_timestamp,
                "location": ocean_name,
                "geolocation": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
             
            return {
                "success": True,
                "data": metadata,
                "error": ""
            }
      
        except Exception as e:
            return {
                "success": False,
                "data": {},
                "error": f"Erro ao processar a localização: {str(e)}"
            }