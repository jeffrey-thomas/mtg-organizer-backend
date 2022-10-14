from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Deck, Card, deck_schema, decks_schema, card_schema, cards_schema, user_schema

api = Blueprint('api',__name__,url_prefix='/api')

###############################################################
# Users
###############################################################

# Create
@api.route('/user',methods=['POST'])
@token_required 
def create_user(uid):

    username = request.json['username']
    email = request.json['email']

    user = User(uid, username, email)

    db.session.add(user)
    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

###############################################################
# Decks
###############################################################

# Create
@api.route('/decks',methods=['POST'])
@token_required 
def create_deck(uid):

    name = request.json['name']

    deck = Deck(uid, name)

    db.session.add(deck)
    db.session.commit()

    response = deck_schema.dump(deck)
    return jsonify(response)

#Read
@api.route('/decks',methods=['GET'])
@token_required
def get_decks(uid):
    decks = Deck.query.filter_by(user_id = uid).all()
    response = decks_schema.dump(decks)
    return jsonify(response)

@api.route('/decks/<id>',methods=['GET'])
@token_required
def get_single_deck(uid,id):
    deck = Deck.query.get(id)
    if(deck.user_id != uid):
        deck = None
    response = deck_schema.dump(deck)
    return jsonify(response)

#Update
@api.route('/decks/<id>',methods=["POST", "PUT"])
@token_required
def update_book(uid, id):
    deck = Deck.query.get(id)
    if(deck.user_id != uid):
        return jsonify(None)

    deck.name = request.json['name']
   
    db.session.commit()
    response = deck_schema.dump(deck)
    return jsonify(response)

#Delete
@api.route('/decks/<id>',methods=["DELETE"])
@token_required
def delete_deck(uid, id):
    deck = Deck.query.get(id)

    if(deck.user_id != uid):
        return jsonify(None)
        
    db.session.delete(deck)
    db.session.commit()

    response = deck_schema.dump(deck)
    return jsonify(response)

###############################################################
# Cards
###############################################################

# Create
@api.route('/cards',methods=['POST'])
@token_required 
def create_card(uid):

    id = request.json['id']
    qty = request.json['qty']

    card = Card(id,uid, qty)

    db.session.add(card)
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)

#Read
@api.route('/cards',methods=['GET'])
@token_required
def get_all_cards(uid):
    cards = db.session.query(Card, Deck).join(Deck).filter(Deck.user_id == uid).all()
    response = cards_schema.dump(cards)
    return jsonify(response)

@api.route('/cards/<deck_id>',methods=['GET'])
@token_required
def get_deck_cards(uid,deck_id):
    cards = db.session.query(Card,Deck).join(Deck).filter(Deck.user_id == uid, Deck.id == deck_id).first()
    response = cards_schema.dump(cards)
    return jsonify(response)

#Update
@api.route('/cards/<deck_id>/<id>',methods=["POST", "PUT"])
@token_required
def update_card(uid, deck_id, id):
    deck = Deck.query.get(deck_id)
    if(deck.user_id != uid):
        return jsonify(None)

    card = Card.query.get((id,deck_id))

    card.qty = request.json['qty']
   
    db.session.commit()
    response = card_schema.dump(card)
    return jsonify(response)

#Delete
@api.route('/cards/<deck_id>/<id>',methods=["DELETE"])
@token_required
def delete_card(uid, deck_id, id):
    deck = Deck.query.get(deck_id)

    if(deck.user_id != uid):
        return jsonify(None)

    card = Card.query.get((id,deck_id))    
    db.session.delete(card)
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)