from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
DB_URI = "postgresql+psycopg2://digitalskola:D6GhCbaaiq8LlNy7@35.193.53.27:5432/api"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)

class Users(db.Model):
  __table_args__ = {"schema": "aji"}
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String)

  def __init__(self, name, address):
    self.name = name
    self.address = address


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == 'GET':
        users = Users.query.all()
        result = [
            {
                "name": user.name,
                "model": user.address
            } for user in users]
        return jsonify(result)
    
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_users = Users(name=data['name'], address=data['address'])
            db.session.add(new_users)
            db.session.commit()
            return {"message": f"User {new_users.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


if __name__ == "__main__":
    app.run(debug=True, port=8080)

