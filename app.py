from flask import Flask, render_template, jsonify, request
from model import db, User
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify([u.to_dict() for u in users]),200

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not User:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user.to_dict()), 200

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    age = int(data["age"])
    new_user = User(name=data["name"].strip(), age = age)
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
    return jsonify(new_user.to_dict()), 201

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": "deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)