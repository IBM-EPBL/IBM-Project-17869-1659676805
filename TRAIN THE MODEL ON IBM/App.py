from flask import Flask,render_template,request
from Static.utils.Geoloc import geolo
from Static.utils  import Home
app=Flask(__name__)

@app.route("/")
def login():
    return render_template("Login.html")

@app.route("/signin")
def signin():
    return render_template("Signup.html")

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
        return render_template("login.html",wrong="myFunction()")

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
    return render_template("login.html")
    

@app.route('/home', methods=['POST','GET'])        
def home():
    city=""
    if request.method=='POST':
        lat=float(request.form['lat'])
        lon=float(request.form['lon'])
        city=geolo(lat,lon)
        print(city)
    return render_template("Home.html",city=city)


if __name__ == '__main__':
   app.run(debug = True)