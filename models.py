from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from flask_marshmallow import Marshmallow

ma=Marshmallow()
db=SQLAlchemy()

#######
# Deck
#######
class Deck(db.Model):
    id=db.Column(UUID(as_uuid=True) , primary_key = True, default=uuid.uuid4)
    user_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(32))

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
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey('deck.id'),primary_key=True)
    qty = db.Column(db.Integer)

    def __repr__(self):
        return f'Card({self.deck_id}, {self.id}, {self.qty})'

class CardSchema(ma.Schema):
    class Meta:
        fields = ['id', 'deck_id', 'qty']

card_schema = CardSchema()
cards_schema = CardSchema(many=True)

