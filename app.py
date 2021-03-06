from flask import Flask, render_template, request, jsonify, json
from flask.json import JSONEncoder
import jwt, os
from boto.s3.connection import S3Connection
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DB_KEY')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cart_table(db.Model):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    complete = db.Column(db.Boolean())

    def __init__(self, user_id, product_id, quantity, complete):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.complete = complete
        
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #token = request.args.get('Authorization')
        
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            splited = token.split(' ')
            
        
    
        if not token:
            return jsonify({'message' : 'Token is missing!'})

        
        try:
            data = jwt.decode(splited[1], app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : "Token is invalid"})
        
        return f(*args,**kwargs)
    return decorated
    

    
@app.route('/')
def index():
    return render_template('APItest.html')



# Add product to cart
@app.route('/api/v1/add_transaction', methods=['POST'])
@token_required
def add_transaction():
    
    data = request.get_json()
    
    user_id = data['user_id']
    product_id = data ['product_id']
    quantity = data['quantity']
    complete = False
    print(os.environ.get('DEV_DB_KEY'))
    current_transaction = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.product_id == product_id, Cart_table.complete == False)
    
    if current_transaction.count() == 0:
        data = Cart_table(user_id,product_id,quantity,complete)
        db.session.add(data)
        db.session.commit()
        return jsonify({"message":"Item has been added to the cart"})
    
    quantity = current_transaction[0].quantity + quantity
    
    current_transaction.update({'quantity' : quantity})
    db.session.commit()

    return jsonify({"message":"quantity is updated"})

# Change quantity of given user_id and product_id
@app.route('/api/v1/change_quantity' , methods=['POST'])
@token_required
def change_quantity():

    data = request.get_json()

    user_id = data['user_id']
    product_id = data ['product_id']
    quantity = data['quantity']
    current_transaction = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.product_id == product_id, Cart_table.complete == False)
    
    if current_transaction.count() == 0:
        return jsonify({"message":"There is no active transaction of given user_id and product_id"})
        
    current_transaction.update({'quantity' : quantity})
    db.session.commit()
    return jsonify({"message":"quantity is changed"})
    
    
# delete active transaction of given user_id and product_id
@app.route('/api/v1/delete_transaction', methods=['DELETE'])
@token_required
def delete_transaction():
    data = request.get_json()

    user_id = data['user_id']
    product_id = data ['product_id']
    
    current_transaction = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.product_id == product_id, Cart_table.complete == False)
    
    if current_transaction.count() == 0:
        return jsonify({"message":"There is no active transaction of given user_id and product_id"})
    
    current_transaction.delete()
    db.session.commit()
    return jsonify({"message":"transaction is deleted"})
    
    
    
    
                
# checkout  query all transaction of given user_id and change complete to TRUE
@app.route('/api/v1/checkout', methods=['POST'])
@token_required
def checkout():
    data = request.get_json()
    user_id = data['user_id']
    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(False))
    
    if current_transactions.count() == 0:
        return jsonify({"message":"There is no active transaction for this user"})
        
    transaction = db.session.query(Cart_table).filter(Cart_table.user_id == user_id).update({'complete' : True})
    
    db.session.commit()
    return jsonify({"message":"Checkout success"})

    
#show active transaction (send all transaction(complete = FALSE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/current_transaction', methods=['GET'])
@token_required
def current_transaction(id):
    data = request.get_json()
    user_id = id
    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(False))
    if current_transactions.count() == 0:
        return jsonify({"message":"There is no active transaction for this user"})
    
    data = []
    for i in current_transactions:
        data_set = {"product_id": i.product_id, "quantity": i.quantity}
        data.append(data_set)
    json_format = json.dumps(data)
    print(json_format)
    
    return json_format

        
#show active transaction (send all transaction(complete = TRUE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/history_transaction', methods=['GET'])
@token_required
def history_transaction(id):
    data = request.get_json()
    user_id = id
    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(True))
    if current_transactions.count() == 0:
        return jsonify({"message" : "There is no past transaction for this user"})
    
    data = []
    for i in current_transactions:
        data_set = {"product_id": i.product_id, "quantity": i.quantity}
        data.append(data_set)
    json_format = json.dumps(data)
    print(json_format)

    return json_format
    
if __name__ == '__main__':
    app.run()
