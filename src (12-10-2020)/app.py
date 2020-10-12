from flask import Flask, render_template, redirect, flash, logging, url_for, session, request
from flask_mysqldb import MySQL
from api_corona import api_country,api_states
from json import dump, load, loads
from datetime import datetime
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from sklearn.tree import DecisionTreeClassifier
import pickle
import requests
import numpy as np

app = Flask(__name__)

with open("ML Model/corona.pkl",'rb') as file:
    model = pickle.load(file)

with open("DATABASE And API Configuration/config.json",'r') as file:
    configuration = load(file)

local_db = False
if(local_db):
    app.config['MYSQL_HOST'] = configuration["DATABASE"]["LOCAL"]['HOST']
    app.config['MYSQL_USER'] = configuration["DATABASE"]["LOCAL"]['USER']
    app.config['MYSQL_PORT'] = configuration["DATABASE"]["LOCAL"]['PORT']
    app.config['MYSQL_DB'] = configuration["DATABASE"]["LOCAL"]['DATABASE']
    app.config['MYSQL_PASSWORD'] = configuration["DATABASE"]["LOCAL"]['PASSWORD']
    app.config['MYSQL_CURSORCLASS'] = configuration["DATABASE"]["LOCAL"]['CURSOR']
else:
    app.config['MYSQL_HOST'] = configuration["DATABASE"]["REMOTE"]['HOST']
    app.config['MYSQL_USER'] = configuration["DATABASE"]["REMOTE"]['USER']
    app.config['MYSQL_PORT'] = configuration["DATABASE"]["REMOTE"]['PORT']
    app.config['MYSQL_DB'] = configuration["DATABASE"]["REMOTE"]['DATABASE']
    app.config['MYSQL_PASSWORD'] = configuration["DATABASE"]["REMOTE"]['PASSWORD']
    app.config['MYSQL_CURSORCLASS'] = configuration["DATABASE"]["REMOTE"]['CURSOR']

mysql = MySQL(app)

@app.route('/')
def home():
    country = api_country()
    states = api_states()

    return render_template("index.html",header_data=country,table_data=states)

@app.route('/about')
def about():
    return render_template("about_corona.html")

@app.route('/predict',methods = ['GET','POST'])
def prediction():

    if request.method =='POST':    
        age = request.form['age']
        temperature = request.form['temperature']
        breathing_problem = request.form['breath']
        cough_or_cold = request.form['cold']
        body_ache = request.form['body']
        now = datetime.now()
        data_registered_date = now.strftime("%Y-%m-%d %H:%M:%S")
    
        # print(age,temperature,breathing_problem,cough_or_cold,body_ache)
        # print(type(age))
        # print(type(temperature))
        # print(type(breathing_problem))
        # print(type(cough_or_cold))
        # print(type(body_ache))

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO corona_data(age,temperature,breathing_problem,cough_or_cold,body_ache,data_registered_date) VALUES(%s,%s,%s,%s,%s,%s)",(age,temperature,breathing_problem,cough_or_cold,body_ache,data_registered_date))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
 
        #columns  -- Age,	Fever,	BodyPains,	RunnyNose,	Difficulty_in_Breath
        data = [[age,temperature,body_ache,cough_or_cold,breathing_problem]]
        predict = model.predict(data)[0]
        proba_score = model.predict_proba([[60,100,0,1,0]])[0][0]
        
        if predict==1:
            prediction='Positive'
        else:
            prediction = 'Negative'
        
        return render_template("corona_form.html",prediction=prediction,proba_score=round(proba_score*100,2))
    else: 
        return render_template("corona_form.html")

@app.route('/medical-centers')
def routes():
    pass

@app.route('/feedback-form',methods=["GET","POST"])
def feedback():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        comments = request.form['comments']
        overall_experience = request.form['experience']
        now = datetime.now()
        feedback_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO feedback(overall_experience,name,email,comments,feedback_date) VALUES(%s,%s,%s,%s,%s)",(overall_experience,name,email,comments,feedback_date))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Your Feedback has been Registered.You Are Redirected to HomePage','success')
        return redirect(url_for("home"))

    else:
        return render_template("feedback_form.html")

@app.route('/contact-form',methods=["GET","POST"])
def contact():
    if request.method =='POST':    
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        now = datetime.now()
        contact_date = now.strftime("%Y-%m-%d %H:%M:%S")

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO contact(name,email,message,contact_date) VALUES(%s,%s,%s,%s)",(name,email,message,contact_date))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Your Contact Details has been Registered.You Are Redirected to HomePage','success')
        return redirect(url_for("home"))

    return render_template("contact_form.html")

if __name__ == '__main__':
    app.secret_key = "\xb6\xa9\xba\xd6y\xd6\x10\xd4,Fh\x1e"
    app.run(debug=True)