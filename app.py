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

personCollection = connection['personEntry'].entries
ticketCollection = connection['ticketEntry'].entries

class User(Document):
    use_dot_notation = True
    __collection='user'
    __database__='main'

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

class Ticket(Document):
    use_dot_notation = True
    __collection='ticket'
    __database__='main'


    structure = {
        'nameAndIDOfOwed': (basestring, int),
        'ticketAmount' : int,
        'ticketType' : basestring,
        'ticketDate' : datetime.datetime,
        'ticketMessage' : basestring,
        'ticketActive' : bool,
        'nameAndIDOfOwers' : [(basestring, int)],
    }

    default_values= {'ticketDate' : datetime.datetime.utcnow}

    def id(self):
        return self._id


connection.register([Ticket])
connection.register([User])
connection.main.entry.Ticket()
connection.main.entry.User()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/make_ticket', methods=['POST'])
def save_ticket():
    return redirect(url_for('index'))


@app.route('/loginattempt', methods=['GET', 'POST'])
def trylogin():
    print "here"
    error = None
    if request.method == 'POST':
            session['logged_in'] = True
            print('You were logged in')
            new_entry = connection.main.personCollection.User()
            new_entry.name = request.form['user_name']
            new_entry.url = request.form['email']
            new_entry.phone_number = request.form['password']
            new_entry.save()

    #for item in connection.main.personCollection.find():
        #print item['name']

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
