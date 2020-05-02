from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/shopping_cart'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://etenqytsjeoypx:ebb1a5d71cc102c5e4ad94bf6734be94253db5b2499022e9a4d1fd5bddcdec60@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d2iqpd7aouh4hr'

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


@app.route('/')
def index():
    return render_template('APItest.html')



# Add product to cart
@app.route('/api/v1/transactions', methods=['POST'])
def add_transaction():
    
    data = request.get_json()
    
    user_id = data['user_id']
    product_id = data ['user_id']
    quantity = data['quantity']
    complete = False
    
    data = Cart_table(user_id,product_id,quantity,complete)
    db.session.add(data)
    db.session.commit()
    return "Item has been added to the cart"
    
        
#<---- todo ------>
        
# checkout  query all transaction of given user_id and change complete to TRUE
@app.route('/api/v1/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data['user_id']

    
def dict_factory(cursor, row): 
"""Converts rows that need to be retrieved into a dictionary object. This function replaces the existing row_factory attribute of the sqlite3 connection object.z"""
d = {}
for idx, col in enumerate(cursor.description):
d[col[0]] = row[idx]
return d
    
#show active transaction (send all transaction(complete = FALSE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/current_transaction', methods=['GET'])
def current_transaction(id):
    user_id = data['user_id']
    complete =  data['complete']
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    current_transaction = cur.execute('SELECT * FROM user_id WHERE complete = False;').fetchall()
    return jsonify(current_transaction)
        
#show active transaction (send all transaction(complete = TRUE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/history_transaction', methods=['GET'])
def history_transaction(id):
    user_id = data['user_id']
    complete =  data['complete']
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    current_transaction = cur.execute('SELECT * FROM user_id WHERE complete = True;').fetchall()
    return jsonify(current_transaction)


if __name__ == '__main__':
    app.run()
