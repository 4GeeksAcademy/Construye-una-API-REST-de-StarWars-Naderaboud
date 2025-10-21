from flask import jsonify, Blueprint
from models import db, User, Planet, Character

api = Blueprint("api", __name__)

def get_current_user():
    return User.query.get(1)

# PEOPLE 
@api.route("/people", methods=["GET"])
def list_people():
    people = Character.query.all()
    return jsonify([p.serialize() for p in people])

@api.route("/people/<int:people_id>", methods=["GET"])
def get_people(people_id):
    person = Character.query.get_or_404(people_id)
    return jsonify(person.serialize())

# PLANETS
@api.route("/planets", methods=["GET"])
def list_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets])

@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify(planet.serialize())

# USERS
@api.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users])

@api.route("/users/favorites", methods=["GET"])
def list_user_favorites():
    user = get_current_user()
    return jsonify({
        "favorite_people": [p.serialize() for p in user.favorite_characters],
        "favorite_planets": [p.serialize() for p in user.favorite_planets]
    })

# FAVORITE PLANET
@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user = get_current_user()
    planet = Planet.query.get_or_404(planet_id)
    if planet not in user.favorite_planets:
        user.favorite_planets.apiend(planet)
        db.session.commit()
    return jsonify({"message": f"{planet.name} added to favorites"}), 200

@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def remove_favorite_planet(planet_id):
    user = get_current_user()
    planet = Planet.query.get_or_404(planet_id)
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
    return jsonify({"message": f"{planet.name} removed from favorites"}), 200

# FAVORITE PEOPLE
@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user = get_current_user()
    person = Character.query.get_or_404(people_id)
    if person not in user.favorite_characters:
        user.favorite_characters.apiend(person)
        db.session.commit()
    return jsonify({"message": f"{person.name} added to favorites"}), 200

@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def remove_favorite_people(people_id):
    user = get_current_user()
    person = Character.query.get_or_404(people_id)
    if person in user.favorite_characters:
        user.favorite_characters.remove(person)
        db.session.commit()
    return jsonify({"message": f"{person.name} removed from favorites"}), 200

if __name__ == "__main__":
    api.run(debug=True)