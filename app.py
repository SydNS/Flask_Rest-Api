from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Records Class/Model
class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    # worth = db.Column(db.Float)
    likes = db.Column(db.Integer)

    def __init__(self, name, description, worth, likes):
        self.name = name
        self.description = description
        self.worth = worth
        self.likes = likes


# Records Schema
class RecordsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'worth', 'likes')


# Init schema
Records_schema = RecordsSchema()
Recordss_schema = RecordsSchema(many=True)


# Create a Records
@app.route('/saverecord', methods=['POST'])
def add_Records():
    data = request.get_json(force=True)

    name = data["name"]
    description = data['description']
    worth = data['worth']
    likes = data['likes']

    new_Records = Records(name, description, worth, likes)

    db.session.add(new_Records)
    db.session.commit()

    return Records_schema.jsonify(data)


# Get All Records
@app.route('/home', methods=['GET'])
def get_Recordss():
    all_Recordss = Records.query.all()
    result = Recordss_schema.dump(all_Recordss)
    return jsonify(result)


# Get Single Records
@app.route('/records/<id>', methods=['GET'])
def get_Records(id):
    Records = Records.query.get(id)
    return Records_schema.jsonify(Records)


# Update a Record
@app.route('/record/<id>', methods=['PUT'])
def update_Records(id):
    Records = Records.query.get(id)

    name = request.json['name']
    description = request.json['description']
    worth = request.json['worth']
    likes = request.json['likes']

    Records.name = name
    Records.description = description
    Records.worth = worth
    Records.likes = likes

    db.session.commit()

    return Records_schema.jsonify(Records)


# Delete Record
@app.route('/record/<id>', methods=['DELETE'])
def delete_Records(id):
    Records = Records.query.get(id)
    db.session.delete(Records)
    db.session.commit()

    return Records_schema.jsonify(Records)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
