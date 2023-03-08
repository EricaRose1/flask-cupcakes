"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def index_page():
    ''' cupakes index '''
    return render_template('base.html')

############################################

@app.route('/api/cupcakes')
def all_cupcakes():
    ''' returns JSON w/ all cupcakes '''
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonfy(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def cupcake_info(id):
    '''Returns JSON for one cupcake in particular'''
    cupcake = Cupcake.query.get_or_404(id)
    return jsonfy(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''create a cupcake form data and return it'''
    new_cupcake = Cupcake(id = request.json["id"],
                    flavor = request.json["flavor"],
                    size = request.json["size"],
                    rating = request.json["rating"],
                    image = request.json["image"] or None)

    db.session.add(new_cupcake)
    bd.session.commit()
    resp_json = jsonify(cupcake = new_cupcake.serialize())
    return (resp_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    '''update exisitng cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.image = request.json.get('image', cupcake.image)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def remove_cupcake(id):
    '''remove cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
    
