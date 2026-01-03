from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

API_KEY = "X9f#2aB7!dE4$kL1"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    basket = db.Column(db.JSON, default=list)  

def require_api_key(func):
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Forbidden"}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/users/", methods=["POST"])
@require_api_key
def register():
    data = request.json
    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        basket=[]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})


@app.route("/login/", methods=["POST"])
@require_api_key
def login():
    data = request.json
    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()
    if user:
        return jsonify({"true_or_false": True, "id": user.id})
    else:
        return jsonify({"true_or_false": False})


@app.route("/users/", methods=["GET"])
@require_api_key
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "password": u.password,
            "basket": u.basket
        } for u in users
    ])


@app.route("/users/<int:id>", methods=["GET"])
@require_api_key
def get_user(id):
    u = User.query.get(id)
    if u:
        return jsonify({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "password": u.password,
            "basket": u.basket
        })
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
