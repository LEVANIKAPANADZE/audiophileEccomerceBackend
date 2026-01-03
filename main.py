from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    basket = db.Column(db.JSON, default=list)  


@app.route("/users/", methods=["POST"])
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
