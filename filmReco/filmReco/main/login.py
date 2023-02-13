from flask import Blueprint, url_for, request, render_template, redirect,session
import requests
import json

from filmReco.extensions import mongo
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=["POST","GET"])
def register():
    # Si la méthode est POST (soumission du formulaire)
    if request.method=="POST":
        # On récupère les infos du formulaire
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        
        
        user_found = mongo.db.users.find_one({"name": user})
        email_found = mongo.db.users.find_one({"email": email})

        if user_found:
            return render_template('registration.html', message="Username already taken")
        if email_found:
            return render_template('registration.html', message="This email already exists in the database")
        if password1 != password2:
            return render_template('registration.html', message="Passwords should match")
        
        mongo.db.users.insert_one({'name': user, 'email': email, 'password': password1})
    
    
    return render_template('registration.html')

@auth.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":

        email = request.form.get("email")
        password = request.form.get("password")

        emailFound = mongo.db.users.find_one({"email":email})

        if not emailFound:
            return render_template('login.html', message="Email not found")
        else:
            passwordFound = emailFound["password"]
            if passwordFound != password:
                return render_template('login.html', message="Password does not match")
        
    return render_template('login.html', message="Logged in")
        


