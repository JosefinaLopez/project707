import os, json
from click import password_option
from flask import Flask, render_template, redirect, url_for, request, session, flash,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
app=Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

    #configurar la session
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
    # base de datos
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login" ,methods= ["GET" , "POST"])
def login():
    #el usuario es pedido mediante el metodo post
    if request.method == "POST":
        #declaracion de variables
        username = request.form.get("username")
        password = request.form.get("password")
        #errores
        if not username:
            flash("Ingrese un usuario")
            return render_template("login.html")
        elif not password:
            flash("Ingrese una contraseña")
            return render_template("login.html")
        
        data = db.execute("SELECT *FROM usuario WHERE username = :username", {"username" :username}).fetchall()
        if len(data)!=1 or not check_password_hash(data[0]["password"], password):
            flash("Contraseña o Usuario No Valido") 
            return render_template("loging.html")
        print (data)
        session["id_user"]= data
        session["username"] = username
            # reedireccion al index
        flash("Sesión iniciada")
        return redirect(url_for("index"))       
     
@app.route("/register")
def register():
    if request.method == "POST": 
        #declaracion de variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        #errores
        if not username:
            flash("Ingrese un usuario")
            return render_template("register.html")
        elif not password:
            flash("Ingrese una contraseña")
            return render_template("register.html")
        elif password != confirmation:
            flash("Las contraseñas no coinciden")
            return render_template("index.html")
        data = db.execute("SELECT *FROM usuario WHERE username = :username", {"username" :username}).fetchall()
        #encriptar contraseña
        if len(data) !=0:
            return "error"
        password = generate_password_hash(password)
        #inserta los datos en la base
        database =db.execute("INSERT INTO usuario (username, password, admin) VALUES(:username, :password , False)" ,{"username" :username, "password" :password})
        #lo envia
        db.commit()
        session["id_user"]=database
        flash("Usuario registrado con exito")
        return render_template("index.html") 
    else:
        return render_template("register.html")  
           
@app.route("/salir")
def salir():
    session.clear()
    return render_template("login.html")    


if __name__ == "__main__":
        app.run(port=3300,debug=True)

