# import redis

# redis_ip = "172.17.0.2"

# connection = redis.StrictRedis(
#     host="localhost",
#     port=6379,
#     db=0,
#     decode_responses = True
# )

# try:
#     if connection.ping():
#         print("conexion exitosa")
#     else:
#         print("conexion fallida")
    
#     #print(connection.lrange("mandalorians", 0, -1))
#     print(connection.get("jedi_1"))
# except redis.exceptions.ConnectionError as e:
#     print(f"Connection error: {e}")


from redis_database import RedisDatabase

redisrepo = RedisDatabase()
Status = RedisDatabase.Status

#print(redisrepo.insert_episode(69, "The Test", 1, 10))
print(redisrepo.select_all_episodes())
#print(redisrepo.select_episode(1))
#print(redisrepo.delete_episode(69))

# import redis

# r = redis.Redis(host='localhost', port=6379, db=0)

# try:
#     r.ping()
#     print("Connected to Redis!")
# except redis.exceptions.ConnectionError as e:
#     print(f"Error connecting to Redis: {e}")
