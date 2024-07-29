from flask import Flask, request, jsonify, render_template
from database import db
from dotenv import load_dotenv
import os
import bcrypt
from flask_socketio import SocketIO
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), str.encode(user.password)):
            login_user(user)
            return jsonify({"message": "Usuario logado com sucesso!"}), 200
    return jsonify({"message": "Credenciais invalidas"}), 400


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Usuário deslogado com sucesso"}), 200


@app.route('/')
def index():
    return render_template('index.html')
