import re

from flask import Flask, render_template, request, redirect
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)


# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=False)

    only_letters_regex = "^[a-zA-Z\u00C0-\u017F\s]+$"
    phone_number_regex = "^[+]*[\d]{0,4}[\d]{3,4}[0-9]{7,9}$"
    email_regex = '^[-\w.]+@([-\w]+\.)+[-\w]{2,4}$'

    @validates("name")
    def validate_name(self, key, name):
        if re.match(self.only_letters_regex, name):
            return name
        raise ValueError("name only can contain letters")

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if re.match(self.only_letters_regex, last_name):
            return last_name
        raise ValueError("last name only can contain letters")

    @validates("email")
    def validate_email(self, key, email):
        friend = self.query.filter_by(email=email).first()

        if friend:
            if friend.id != self.id:
                raise ValueError("email must be unique")
        if re.match(self.email_regex, email):
            return email
        raise ValueError("email must be valid")

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        friend = self.query.filter_by(phone_number=phone_number).first()

        if friend:
            if friend.id != self.id:
                raise ValueError("phone number must be unique")
        if re.match(self.phone_number_regex, phone_number):
            return phone_number
        raise ValueError("phone number must be valid")

    # Create a function to return a string when we add
    def __repr__(self):
        return '<Name %r>' % self.id


subscribers = []


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a problem deleting that friend"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    print(request.method)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        friend_to_update.last_name = request.form['last_name']
        friend_to_update.company = request.form['company']
        friend_to_update.phone_number = request.form['phone_number']
        friend_to_update.email = request.form['email']
        try:
            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            return render_template('update.html', friend_to_update=friend_to_update, error=e)
    else:
        return render_template('update.html', friend_to_update=friend_to_update)


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    page = request.args.get('page', 1, type=int)
    title = "My Friend List"
    if request.method == "POST":
        friend = {}
        friend['name'] = request.form['name']
        friend['last_name'] = request.form['last_name']
        friend['company'] = request.form['company']
        friend['phone_number'] = request.form['phone_number']
        friend['email'] = request.form['email']
        try:
            new_friend = Friends(name=friend['name'], last_name=friend['last_name'], company=friend['company'], phone_number=friend['phone_number'], email=friend['email'])
        # Push to database

            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            friends = Friends.query.order_by(Friends.name).paginate(page=page, max_per_page=10, error_out=False)
            return render_template("friends.html", title=title, friends=friends, error=e, friend=friend)
    else:
        friend = {}
        friend['name'] = ''
        friend['last_name'] = ''
        friend['company'] = ''
        friend['phone_number'] = ''
        friend['email'] = ''
        friends = Friends.query.order_by(Friends.id).paginate(page=page, max_per_page=10, error_out=False)
        return render_template("friends.html", title=title, friends=friends, friend=friend)


@app.route('/')
def index():
    title = "Eduardo Ahumada's Portfolio"
    return render_template("index.html", title=title)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
