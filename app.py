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

class Entry(Document):
    use_dot_notation = True
    __collection__='entry'
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
    
    

connection.register([Entry])
connection.main.entry.Entry()


# def new_entry(name, pin):
#     new_entry=connection.main.entry.Entry()
#     new_entry.nameAndIDOfOwed = (name, pin)
#     new_entry.save()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/results', methods=['POST'])
def results():
    search_term = request.form['term']
    location = request.form['location']
    numbers = 1
    #numbers = range(100,200)
    return render_template('results.html', 
        search_term=search_term,
        location=location,
        integers=numbers)

if __name__ == '__main__':
    app.run(debug=True)