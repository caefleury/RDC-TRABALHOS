from database import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, timezone

chat_room_members = db.Table('chat_room_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('chat_room_id', db.Integer, db.ForeignKey('chatrooms.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    messages = db.relationship("Message", back_populates="user")
    chatrooms = db.relationship("ChatRoom", foreign_keys="[ChatRoom.user_id]", back_populates="user")
    joined_rooms = db.relationship('ChatRoom', secondary=chat_room_members, back_populates='members')

class ChatRoom(db.Model, SerializerMixin):
    __tablename__ = 'chatrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    members = db.relationship('User', secondary=chat_room_members, back_populates='joined_rooms')

    messages = db.relationship('Message', cascade='all, delete-orphan', back_populates='chatroom')
    user = db.relationship("User", foreign_keys=[user_id], back_populates="chatrooms")
    participant = db.relationship("User", foreign_keys=[participant_id])
   
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_type = db.Column(db.String(50))  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatrooms.id'), nullable=False)
    file_url = db.Column(db.String(255), nullable=True)  
    file_type = db.Column(db.String(50), nullable=True) 

    user = db.relationship("User", back_populates="messages")
    chatroom = db.relationship("ChatRoom", back_populates="messages")
