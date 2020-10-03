from flask import Flask, render_template, redirect, flash, logging, url_for, session, request
import requests
from json import dump, load

app = Flask(__name__)

with open("config.json",'r') as file:
    configuration = load(file)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about_corona.html")

@app.route('/form',methods = ['GET','POST'])
def form():
    return render_template("corona_form.html")

@app.route('/medical-centers')
def routes():
    pass

if __name__ == '__main__':
   app.run(debug=True)