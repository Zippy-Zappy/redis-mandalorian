from redis_database import RedisDatabase
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
redisrepo = RedisDatabase()
#Status = RedisDatabase.Status

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json()
    result = redisrepo.insert_episode(
        data["number"],
        data["name"],
        data["season"],
        data["price"]
    )
    return jsonify({"message": result})

@app.route("/episodes", methods=["GET"])
def get_episodes():
    result = redisrepo.select_all_episodes()
    return jsonify(result)

@app.route("/delete/<number>", methods=["DELETE"])
def delete(number):
    result = redisrepo.delete_episode(number)
    return jsonify({"message": result})

@app.route("/update/<number>", methods=["PUT"])
def update_episode(number):
    try:
        data = request.get_json()  # Get data as JSON
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Update every field
        name = data.get("name")
        season = data.get("season")
        price = data.get("price")

        if not all([name, season, price]):  # Verify all fields are present
            return jsonify({"message": "Missing fields (name, season, or price)"}), 400

        # Call update_episode method from redis.
        result = redisrepo.update_episode(number, name=name, season=season, price=price)
        return jsonify({"message": result})
    
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route("/rent/<number>", methods=["PUT"])
def rent_episode(number):
    result = redisrepo.rent_episode(number)
    return jsonify({"message": result})

@app.route("/verify/<number>", methods=["PUT"])
def verify_payment(number):
    result = redisrepo.verify_payment(number)
    return jsonify({"message": result})

if __name__ == "__main__":
    app.run(debug=True)
# print(redisrepo.select_all_episodes())
# print(redisrepo.select_episode(1))
# print(redisrepo.rent_episode(69))
# print(redisrepo.verify_payment(69))