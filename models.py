from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from flask_marshmallow import Marshmallow

ma=Marshmallow()
db=SQLAlchemy()

#######
# User
#######
class User(db.Model):
    g_auth_uid = db.Column(db.String(128), primary_key = True)
    username = db.Column(db.String(32), nullable=True, default='')
    email = db.Column(db.String(128), nullable=False)

    def __init__(self, uid, username, email):
        self.g_auth_uid = uid
        self.username = username
        self.email = email

    def __repr__(self):
        return f'User({self.id},{self.email},{self.username})'

class UserSchema(ma.Schema):
    class Meta:
        fields = ['g_auth_id', 'username', 'email']

user_schema = UserSchema()

#######
# Deck
#######
class Deck(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String, db.ForeignKey('user.g_auth_uid'), nullable=False)
    name = db.Column(db.String(32))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f'Deck({self.id}, {self.user_id},{self.name})'

class DeckSchema(ma.Schema):
    class Meta:
        fields = ['id', 'user_id', 'name']

deck_schema = DeckSchema()
decks_schema = DeckSchema(many=True)

#######
# Card
#######
class Card(db.Model):
    id = db.Column(db.String(40),primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'),primary_key=True)
    qty = db.Column(db.Integer)

    def __init__(self, card_id, deck_id, qty):
        self.id = card_id
        self.deck_id = deck_id
        self.qty = qty

    def __repr__(self):
        return f'Card({self.deck_id}, {self.id}, {self.qty})'

class CardSchema(ma.Schema):
    class Meta:
        fields = ['id', 'deck_id', 'qty']

card_schema = CardSchema()
cards_schema = CardSchema(many=True)

