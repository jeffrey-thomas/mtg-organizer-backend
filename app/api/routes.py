from flask import Blueprint, request, jsonify
from flask_cors import CORS
from helpers import token_required
from models import db, Deck, Card, deck_schema, decks_schema, card_schema, cards_schema

api = Blueprint('api',__name__,url_prefix='/api')
CORS(api)
###############################################################
# Decks
###############################################################

# Create
@api.route('/decks',methods=['POST'])
@token_required 
def create_deck(uid):

    name = request.json['name']

    deck = Deck(user_id=uid, name=name)

    db.session.add(deck)
    db.session.commit()

    response = deck_schema.dump(deck)
    return jsonify(response)

#Read
@api.route('/decks',methods=['GET'])
@token_required
def get_decks(uid):
    decks = db.session.query(Deck.id,Deck.name).filter_by(user_id = uid).all()
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
def update_deck(uid, id):
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
    
    #move cards out of deck
    library = db.session.query(Deck).filter_by(user_id=uid, name='').first()
    cards = db.session.query(Card).filter_by(deck_id=id)
    for card in cards:
        #check if card is also already in library
        existingCard = db.session.query(Card).filter_by(deck_id=library.id, id=card.id).first()
        if(existingCard == None):
            card.deck_id = library.id    
        else:
            existingCard.qty += card.qty
            db.session.delete(card)

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
def add_card(uid):

    deck_id = request.json['deck_id']
    id = request.json['id']
    qty = request.json['qty']

    #check if card already exists
    card = db.session.query(Card).filter_by(deck_id=deck_id, id=id).first()
    if(card == None):
        card = Card(id=id,deck_id=deck_id, qty=qty)
        db.session.add(card)
    else:
        card.qty += qty
    
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)

#Read
@api.route('/cards',methods=['GET'])
@token_required
def get_cards_by_deck_id(uid):
    deck_ids = request.args.getlist('deck')
    cards = db.session.query(Card).filter(Card.deck_id.in_(deck_ids))
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
