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


FACEBOOK_APP_ID = "438754742875401"
FACEBOOK_APP_SECRET = "978a9f480a199a29121ef6ff9726a5ef"

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

    def logon(self):
        args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=request.path_url)
        self.redirect(
            "https://graph.facebook.com/oauth/authorize?" +
            urllib.urlencode(args))

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
current = User()

FACEBOOK_APP_ID = "438754742875401"
FACEBOOK_APP_SECRET = "978a9f480a199a29121ef6ff9726a5ef"

@app.route('/')
def login():
    alreadylogged = False;
    if 'username' in session:
        alreadylogged = True;
        print "Already logged in as %s" % session['username']
    current.logon()
    print ("logging on")
    return render_template('login.html', islogged = alreadylogged)

@app.route('/home')
def home():
    if (session['logged_in']):
        print session['username']
        return render_template('index.html')
    else:
        print "NOT LOGGED IN!"
        return render_template('login.html')

@app.route('/make_ticket', methods=['GET', 'POST'])
def make_ticket():
    if (session['logged_in']):
        print session['username']
        return render_template('makeTix.html')
    else:
        print "NOT LOGGED IN!"
        return render_template('login.html', islogged=False)

@app.route('/profile')
def profile():
    if (session['logged_in']):
        print session['username']
        ticket_item = []
        ticket_list = []
        for item in connection.main.ticketCollection.find():
            if session['username'] == item['nameAndIDOfOwed'][0]:
                ticket_item.append(item['nameAndIDOfOwed'])
                ticket_item.append(item['ticketAmount'])
                ticket_list.append(ticket_item)
                ticket_item = []
        return render_template('profile.html', tickets=ticket_list)
    else:
        print "NOT LOGGED IN!"
        return render_template('login.html', islogged=False)

@app.route('/profile', methods=['POST'])
def save_entry():
    #new_entry = personCollection.User()
    new_entry = connection.main.personCollection.User()
    new_entry.name = request.form['user_name']
    new_entry.url = request.form['email']
    new_entry.phone_number = request.form['password']
    new_entry.save()

@app.route('/logout', methods=['POST'])
def logout():
    print"logging out"
    session.pop('username', None)
    session['logged_in'] = False
    return render_template('login.html')

@app.route('/loginattempt', methods=['GET', 'POST'])
def trylogin():
    print "here"
    error = None
    if request.method == 'POST':
            print('You were logged in')
            new_entry = connection.main.personCollection.User()
            new_entry.name = request.form['user_name']
            new_entry.url = request.form['email']
            new_entry.phone_number = request.form['password']
            new_entry.save()

            session['logged_in'] = True
            session['username'] = new_entry.name

    #for item in connection.main.personCollection.find():
        #print item['name']

    return redirect(url_for('home'))

def get_tickets():
    for item in connection.main.ticketCollection.Ticket():
        print item


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
