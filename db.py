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
names = ''


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


def new_entry(name, pin):
	new_entry=connection.main.entry.Entry()
	new_entry.nameAndIDOfOwed = (name, pin)
	#entries.add(new_entry)
	new_entry.save()


new_entry("Alana", 0)
new_entry("Jessie", 1)

@app.route('/')
def hello():
	names_before = ''
	i = 0
    	for item in connection.main.entry.find():
    		names_before += item['nameAndIDOfOwed'][0] + str(i) +"\n"
    		i+=1
    		connection.main.entry.remove()
    	return names_before


if __name__=="__main__":
	app.run(debug=True)
