from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

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


@app.route('/api/v1/transactions', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Cart_table).filter(Cart_table.customer == customer).count() == 0:
            data = Cart_table(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
