from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Models
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes

@app.route('/')
def home():
    return {"message": "Chatterbox API running ✅"}

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([
        {
            "id": msg.id,
            "body": msg.body,
            "username": msg.username,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ])

# POST new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    new_msg = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "id": new_msg.id,
        "body": new_msg.body,
        "username": new_msg.username,
        "created_at": new_msg.created_at.isoformat()
    }), 201

# PATCH update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        msg.body = data['body']

    db.session.commit()

    return jsonify({
        "id": msg.id,
        "body": msg.body,
        "username": msg.username,
        "created_at": msg.created_at.isoformat()
    })

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get_or_404(id)

    db.session.delete(msg)
    db.session.commit()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
