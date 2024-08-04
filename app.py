from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from database import db
from flask_socketio import SocketIO, emit, join_room
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
import subprocess
import cryptography
from models.user import User ,ChatRoom, Message
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import datetime, timezone
import logging
from werkzeug.utils import secure_filename
from flask import url_for

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'

socketio = SocketIO(app,cors_allowed_origins="*")

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
jwt = JWTManager(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                login_user(user)
                return jsonify({"message": "Usuario logado com sucesso!"}), 200
        return jsonify({"message": "Credenciais invalidas"}), 400
    return render_template('login.html')

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Usuário deslogado com sucesso"}), 200


@app.route("/register", methods=["GET","POST"])
def create_user():
    if request.method == 'POST':
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if username and password and email:
            find_user_by_username = User.query.filter_by(username=username).first()
            find_user_by_email = User.query.filter_by(email=email).first()
            if find_user_by_username:
                return jsonify({"message": "Esse nome de usuário já existe"}), 400
            elif find_user_by_email:
                return jsonify({"message": "Esse email já está sendo utilizado por outro usuário"}), 409
            
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuário criado com sucesso"}), 200

        return jsonify({"message", "Dados inválidos"}), 400
    return render_template('register.html')




class CreateChatRoom(Resource):
    @login_required
    def post(self):
        user_id = current_user.id
        participant_id = request.json.get('participant_id')
        group_name = request.json.get('name')

        chat_room = ChatRoom(user_id=user_id, participant_id=participant_id, name=group_name)
        db.session.add(chat_room)
        db.session.commit()
        return {"chat_room_id": chat_room.id}, 201
class MessagesByChatRoomId(Resource):
    @login_required
    def get(self, chat_room_id):
        chat_room = ChatRoom.query.filter_by(id=chat_room_id).first()

        if not chat_room:
            return {"message": "Chat room not found"}, 404

        messages = Message.query.filter_by(chatroom_id=chat_room_id).all()

        messages_data = [
            {
                'id': message.id,
                'content': message.content,
                'user_id': message.user_id,
                'sender_type': message.sender_type,
                'timestamp': message.timestamp.isoformat(),
                'username': message.user.username
            } for message in messages
        ]
        return messages_data


api.add_resource(CreateChatRoom, '/chat_room')
api.add_resource(MessagesByChatRoomId, '/chat_room/<int:chat_room_id>/messages')

@socketio.on('send_message')
def handle_send_message(data):

    user_id = current_user.id
    chat_room_id = data['chat_room_id']
    message_content = data['message']
    sender_type = data['sender_type']

    chat_room = ChatRoom.query.get(chat_room_id)
    if chat_room:
        new_message = Message(content=message_content, user_id=user_id, sender_type=sender_type, chatroom_id=chat_room_id, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()
        
        print(new_message)
        new_message_id = new_message.id
        emit('new_message', {
            'id': new_message.id,
            'content': message_content,
            'user_id': user_id,
            'sender_type': sender_type,
            'username': current_user.username
        }, room=data(chat_room_id))
        print(message_content)

@app.route('/users', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    users_data = [{'username': user.username, 'email': user.email} for user in users]
    return render_template('users.html', users=users_data)
     
@app.route('/profile')
@login_required
def profile():
    user = current_user
    user_data = {
        'username': user.username,
        'email': user.email
    }
    return render_template('profile.html', user=user_data)


@socketio.on('join')
def on_join(data):
    room = data['chat_room_id']
    join_room(room)
    emit('join_response', f"{current_user.username} has joined the room.", room=room)

@app.route('/get_groups', methods=['GET'])
@login_required
def get_user_groups():
    groups = ChatRoom.query.all()
    groups_data = [
        {
            'id': group.id,
            'name': group.name,
            'owner': {
                'id': group.user_id,
                'username': User.query.get(group.user_id).username
            }
        } for group in groups
    ]
    return jsonify(groups_data), 200

@app.route('/groups', methods=['GET'])
@login_required
def groups_page():
    return render_template('groups.html')

@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    user_id = current_user.id
    data = request.json
    group_name = data.get('name')

    if not group_name:
        return jsonify({"message": "Invalid data"}), 400

    chat_room = ChatRoom(user_id=user_id, participant_id=user_id, name=group_name)
    db.session.add(chat_room)
    db.session.commit()
    return jsonify({"message": "Group created successfully", "chat_room_id": chat_room.id}), 201


@app.route('/group/<int:chat_room_id>', methods=['GET'])
@login_required
def group_page(chat_room_id):
    chat_room = ChatRoom.query.get_or_404(chat_room_id)
    return render_template('group.html', chat_room_id=chat_room_id)


# @app.route('/join_group/<int:chat_room_id>', methods=['POST'])
# @login_required
# def join_group(chat_room_id):
#     chat_room = ChatRoom.query.get_or_404(chat_room_id)
#     if current_user not in chat_room.members:
#         chat_room.members.append(current_user)
#         db.session.commit()
#         socketio.emit('user_joined', {'user_id': current_user.id, 'username': current_user.username}, room=str(chat_room_id))
#     return jsonify({"message": "Joined group successfully"}), 200

if __name__ == "__main__":
     socketio.run(app,debug=True)
