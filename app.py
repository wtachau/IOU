from flask import Flask, render_template, request

app = Flask(__name__) 

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