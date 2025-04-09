import redis
from enum import Enum
import time

class RedisDatabase:
    _instance = None

    class Status(Enum):
        AVAILABLE = 1
        RESERVED = 2
        RENTED = 3

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.StrictRedis(
            host="localhost",
            port=6379,
            db=1,
            decode_responses = True
            )
        return cls._instance
    
    def insert_episode(self, number, name, season, price):

        episode_data = {
            "name": name,
            "price": price,
            "season": season,
            "status": str(self.Status.AVAILABLE)
        }
        try:
            client = self.get_instance()
            #Sets episode data as a hash. Uses "episode number" as key.
            #It is commonly used in Redis when there is an object with
            #multiple attributes.
            client.hset(f"Episode {number}", mapping=episode_data)
            #adds episode number to episodes set.
            client.sadd("episodes", number)

            return f"Episode {number} successfully inserted."
        except redis.RedisError as error:
            return f"Error during insert operation: {error}"

    def select_all_episodes(self):
        episode_list = []
        try:
            client = self.get_instance()
            episodes = client.smembers("episodes")
            
            for episode in episodes:
                data = self.select_episode(episode)
                episode_list.append(f"Episode {episode} - {data["name"]}")
            return episode_list
        except redis.RedisError as error:
            return f"Error during select operation: {error}"
    
    def select_episode(self, number):
        try:
            client = self.get_instance()
            data = client.hgetall(f"Episode {number}")
            if len(data) == 0:
                return f"Error. Episode {number} does not exist."
            return data
        except redis.RedisError as error:
            return f"Error during select operation: {error}"

    def update_episode(self, number, **kwargs):
        try:
            if kwargs:
                client = self.get_instance()
                client.hset(f"Episode {number}", mapping=kwargs)
                return f"Episode {number} succesfully updated with {kwargs}"
            else:
                return f"No fields have been modified."
        except redis.RedisError as error:
            return f"Error during update operation: {error}"
                
    
    def delete_episode(self, number):
        try:
            client = self.get_instance()
            if (client.delete(f"Episode {number}") > 0):
                client.srem("episodes", number)
                return f"Episode {number} successfully deleted."
            return f"Error. Episode {number} not found."
        except redis.RedisError as error:
            return f"Error during delete operation: {error}"

    def rent_episode(self, number):
        try:
            client = self.get_instance()
            client.setex(f"Episode {number}:expiry", 10, "True")
            return f"Episode {number} rented successfully. You have 4 (four) minutes to confirm transaction."
        except redis.RedisError as error:
            return f"Error during rent operation: {error}"
    
    def verify_payment(self, episode_number):
        try:
            client = self.get_instance()
            if not client.exists(f"Episode {episode_number}:expiry"):
                return f"Episode {episode_number} has not been rented."
            self.update_episode(episode_number, status=str(self.Status.RENTED))
            print("Payment confirmed! The episode is yours for 24 hours.")
            time.sleep(20)
            self.update_episode(episode_number, status=str(self.Status.AVAILABLE))
            return("24 hours have passed (in Mercury, probably). The episode is now available for rent.")
        except redis.RedisError as error:
            return f"Error during confirm payment operation: {error}"

    #reservar:
    #creamos una key temporal
    #r.setex(f'chapter:{capitulo_id}:expiry', 240, 'true')
    
    #despues tenemos una funcion de verificar payment:
    #if not .exists(key):
    #la clave expira, se puede volver al estado "disponible" (en mi caso creo que no es necesario)
    #else: avisar que sigue reservado