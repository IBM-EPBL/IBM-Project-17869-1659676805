from flask import Flask,render_template,request
from Static.utils.Geoloc import geolo
from Static.utils  import Home
from Static.utils import CropCloud
from Static.utils import RainCloud
import requests
import numpy as np
import pickle 

# Loading crop recommendation model
crop_recommedation_model_path='Model/crop_recommender.pkl'
crop_recommedation_model=pickle.load(open(crop_recommedation_model_path,'rb'))

# Loading rainfall prediction model
rainfall_model_path='Model/rainfall_prediction.pkl'
rainfall_model=pickle.load(open(rainfall_model_path,'rb'))


app=Flask(__name__)

def weather_fetch(city_name):
    api_key= "9d7cde1f6d07ec55650544be1631307e"
    base_url="http://api.openweathermap.org/data/2.5/weather?"

    complete_url=base_url+"appid="+api_key+"&q="+city_name
    response=requests.get(complete_url)
    x=response.json()
    
    if x["cod"]!="404":
        y=x["main"]
        temperature=round((y["temp"]-273.15),2)
        humidity=y["humidity"]
        return temperature,humidity
    else:
        return None

@app.route("/")
def login():
    return render_template("Login.html",wrong="")

@app.route("/signin")
def signin():
    return render_template("Signup.html")

@app.route("/rainfall")
def rainfall():
    return render_template("Rainfall.html",rainfall="")

@app.route("/crop")
def crop():
    return render_template("Crop.html",crops="")

@app.route('/login', methods=['POST','GET'])        
def welcome():
    email=""
    password=""
    if request.method=='POST':
        email=str(request.form['email'])
        password=str(request.form['password'])
    if(Home.logins(email,password)): 
        return render_template("Welcome.html")
    else:
        return render_template("login.html",wrong=['Invalid Creditails','wr'])

@app.route('/signins', methods=['POST','GET'])        
def signins():
    email=""
    password=""
    name=""
    mobile=""
    if request.method=='POST':
        name=str(request.form['name'])
        email=str(request.form['email'])
        mobile=str(request.form['mobile'])
        password=str(request.form['password'])
        print(name,email,mobile,password)
    Home.signups(email,password,name,mobile)
    return render_template("login.html",wrong="")
    

@app.route('/home', methods=['POST','GET'])        
def home():
    city=""
    if request.method=='POST':
        lat=float(request.form['lat'])
        lon=float(request.form['lon'])
        city=geolo(lat,lon)
        print(city)
    return render_template("Home.html",city=city)

@app.route('/crop-predict',methods=['POST','GET'])
def crop_prediction():
    if request.method=='POST':
        N=int(request.form['nitrogen'])
        P=int(request.form['phosphorous'])
        K=int(request.form['pottasium'])
        ph=float(request.form['ph'])
        rainfall=float(request.form['rainfall'])
        city=request.form.get("city")

        if weather_fetch(city) != None:
            temperature,humidity = weather_fetch(city)
            final_prediction=CropCloud.call_cloud(N,P,K,temperature,humidity,ph,rainfall)
            ws=["static/image/"+final_prediction+".jpg",final_prediction,'myfunc()']
            return render_template('crop.html',crops=ws)
        else:
            return render_template('crop.html',crops=[0,0,"error()"])
    else:
            return render_template('crop.html',crops=[0,0,"error()"])

@app.route('/rainfall-predict',methods=['POST','GET'])
def rainfall_prediction():
    if request.method=='POST':
        mintemp=float(request.form['mintemp'])
        meantemp=float(request.form['meantemp'])
        maxtemp=float(request.form['maxtemp'])
        pressure=float(request.form['pressure'])
        preceptions=float(request.form['preceptions'])
        windspeed=float(request.form['windspeed'])

        
        final_prediction=RainCloud.call_cloud("TAMIL NADU",2022,11,mintemp,meantemp,maxtemp,preceptions,pressure,windspeed)
        #ws=["static/image/"+final_prediction+".jpg",final_prediction,'myfunc()']
        return render_template('Rainfall.html',rainfall=[final_prediction,"pre()"])
    else:
            return render_template('Rainfall.html',error="Can't predicted Some Error. Try Again")

if __name__ == '__main__':
   app.run(debug = True)