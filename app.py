from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for
)
from mongokit import Connection, Document, ObjectId
import datetime
from oauth import sign_url
import json
import requests
import urllib

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__) 
app.config.from_object(__name__)
connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

FACEBOOK_APP_ID = "438754742875401"
FACEBOOK_APP_SECRET = "978a9f480a199a29121ef6ff9726a5ef"

class Entry(Document):
    use_dot_notation = True

    structure = {
        'name': basestring,
        'created_at': datetime.datetime,
        'email': basestring,
        'password': basestring,
    }

    default_values = {'created_at': datetime.datetime.utcnow}

    def id(self):
        return self._id

    def __repr__(self):
        return '<Entry %s>' % self['name']

connection.register([Entry])
collection = connection['IOU'].entries

# VIEWS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile', methods=['POST'])
def save_entry():
    new_entry = collection.Entry()
    new_entry.name = request.form['user_name']
    new_entry.url = request.form['email']
    new_entry.phone_number = request.form['password']
    new_entry.save()

    return redirect(url_for('index'))


"""# We'll need a user class, but how?
class User(db.Model):
    User Model Class
    id = db.StringProperty(required=True) #facebook user-id
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)  #fb OAUTH access token"""

if __name__ == '__main__':
    app.run(debug=True)

"""@app.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        content='Profile Page',
        facebook_conn=social.facebook.get_connection())"""


"""
@app.route('/results', methods=['POST'])
def results():
    search_term = request.form['term']
    location = request.form['location']
    numbers = 1
    #numbers = range(100,200)
    return render_template('results.html', 
        search_term=search_term,
        location=location,
        integers=numbers)"""