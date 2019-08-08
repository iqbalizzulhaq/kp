import sys
from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/coba")
def coba():
	return render_template("coba.html")

@app.route("/bandwidth-monitoring")
def bandwidth():
	text = open('data.txt', 'r+')
	content = text.read()
	text.close()
	return content
    
@app.route("/home")
def content():
	text = open('data.txt', 'r+')
	content = text.read()
	text.close()
	return render_template('home.html', text=content)

if __name__ == "__main__":
    app.run(debug=True)

