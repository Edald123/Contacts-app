"""This module contains the Friends app
"""
import re
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)


# Create db model
class Friends(db.Model):
    """This class contains the Friends model with its validators
    Args:
        db.Model (db): db instance
    Raises:
        ValueError: Some field is invalid
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=False)

    only_letters_regex = r"^[a-zA-Z\u00C0-\u017F\s]+$"
    phone_number_regex = r"^[+]*[\d]{0,4}[\d]{3,4}[0-9]{7,9}$"
    email_regex = r"^[-\w.]+@([-\w]+\.)+[-\w]{2,4}$"

    @validates("name")
    def validate_name(self, key, name):
        """Validates name
        Args:
            name (string): name to update
        Raises:
            ValueError: name is invalid
        Returns:
            name: if name is valid returns the name
        """
        if re.match(self.only_letters_regex, name):
            return name
        raise ValueError("name only can contain letters")

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        """Validates last_name
        Args:
            last_name (string): last name to update
        Raises:
            ValueError: last name is invalid
        Returns:
            last_name: if last name is valid returns the last_name
        """
        if re.match(self.only_letters_regex, last_name):
            return last_name
        raise ValueError("last name only can contain letters")

    @validates("email")
    def validate_email(self, key, email):
        """Validates email
        Args:
            email (string): email to update
        Raises:
            ValueError: email is invalid
        Returns:
            email: if email is valid returns the email
        """
        friend = self.query.filter_by(email=email).first()

        if friend:
            if friend.id != self.id:
                raise ValueError("email must be unique")
        if re.match(self.email_regex, email):
            return email
        raise ValueError("email must be valid")

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        """Validates phone_number
        Args:
            phone_number (string): phone number to update
        Raises:
            ValueError: phone number is invalid
        Returns:
            phone_number: if phone number is valid returns the phone_number
            "": if phone number is void return a void string
        """
        if phone_number:

            friend = self.query.filter_by(phone_number=phone_number).first()

            if friend:
                if friend.id != self.id:
                    raise ValueError("phone number must be unique")
            if re.match(self.phone_number_regex, phone_number):
                return phone_number
            raise ValueError("phone number must be valid")
        return ""

    # Create a function to return a string when we add
    def __repr__(self):
        return '<Name %r>' % self.id


subscribers = []


@app.route('/')
def index():
    """Index of the friends page
    Returns:
        render_template: renders the index of the friends page
    """
    title = "Welcome"
    return render_template("index.html", title=title)


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    """List and create friends
    Returns:
        render_template: render the list and the create form of friends
    """
    page = request.args.get('page', 1, type=int)
    title = "Friends"
    if request.method == "POST":
        friend = {'name': request.form['name'], 'last_name': request.form['last_name'],
                  'company': request.form['company'], 'phone_number': request.form['phone_number'],
                  'email': request.form['email']}
        try:
            new_friend = Friends(name=friend['name'], last_name=friend['last_name'], company=friend['company'],
                                 phone_number=friend['phone_number'], email=friend['email'])
            # Push to database

            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            list_of_friends = Friends.query.order_by(Friends.name).paginate(page=page, max_per_page=10, error_out=False)
            return render_template("friends.html", title=title, friends=list_of_friends, error=e, friend=friend)
    else:
        friend = {'name': '', 'last_name': '', 'company': '', 'phone_number': '', 'email': ''}
        list_of_friends = Friends.query.order_by(Friends.name).paginate(page=page, max_per_page=10, error_out=False)
        return render_template("friends.html", title=title, friends=list_of_friends, friend=friend)


@app.route('/update/<id_friend>', methods=['POST', 'GET'])
def update(id_friend):
    """Update one friend by id
    Args:
        id_friend (integer): id of the friend to update
    Returns:
        redirect: redirects to friends page
        render_template: if error renders the form to update with the errors
    """
    friend_to_update = Friends.query.get_or_404(id_friend)

    if request.method == "POST":
        friend = {'id': id_friend, 'name': request.form['name'], 'last_name': request.form['last_name'],
                  'company': request.form['company'], 'phone_number': request.form['phone_number'],
                  'email': request.form['email']}
        try:
            friend_to_update.name = friend['name']
            friend_to_update.last_name = friend['last_name']
            friend_to_update.company = friend['company']
            friend_to_update.phone_number = friend['phone_number']
            friend_to_update.email = friend['email']

            db.session.commit()
            return redirect('/friends')
        except Exception as e:
            print("hello")
            return render_template('update.html', friend_to_update=friend, error=e)
    else:
        return render_template('update.html', friend_to_update=friend_to_update)


@app.route('/delete/<id_friend>')
def delete(id_friend):
    """Delete a friend by id
    Args:
        id_friend (integer): id of the friend to delete
    Returns:
        redirect: redirects to friends page
    """
    friend_to_delete = Friends.query.get_or_404(id_friend)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a problem deleting that friend"


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
