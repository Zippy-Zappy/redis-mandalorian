import redis
from enum import Enum

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
            return data
        except redis.RedisError as error:
            return f"Error during select operation: {error}"

    def delete_episode(self, number):
        try:
            client = self.get_instance()
            if (client.delete(f"Episode {number}") > 0):
                client.srem("episodes", number)
                return f"Episode {number} successfully deleted."
            return f"Error. Episode {number} not found."
        except redis.RedisError as error:
            return f"Error during delete operation: {error}"
