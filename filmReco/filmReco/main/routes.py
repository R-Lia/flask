from flask import Blueprint, url_for, request, render_template, redirect
import requests
import json

from filmReco.extensions import mongo
main = Blueprint('main', __name__)

def get_info(movieTitle):
    url = "https://1mdb-data-searching.p.rapidapi.com/om"

    querystring = {"t":movieTitle}

    headers = {
	    "X-RapidAPI-Key": "0f85766d4cmsh5fabae171ecf09bp124df3jsn763272aa8fa2",
	    "X-RapidAPI-Host": "1mdb-data-searching.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonR = json.loads(response.text)
    return jsonR

def updateDatabase():
    moviesCo = mongo.db.movies
    allMovies = moviesCo.find()
    
    for m in allMovies :
        info = get_info(m["Film"])
        if info["Response"]=="True":
            moviesCo.update_one({"_id":m["_id"]}, {"$set": {
                "Date" : info["Year"],
                "Runtime" : info["Runtime"],
                "Genre" : info["Genre"],
                "Réalisateur": info["Director"],
                "Actors" : info["Actors"],
                "Country" : info["Country"],
                "Poster" : info["Poster"],
                "Plot" : info["Plot"]
            }})

"""
@main.route('/', methods=["POST","GET"])
def login():
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
            return render_template('registration.html', "Username already taken")
        if email_found:
            return render_template('registration.html', "This email already exists in the database")
        if password1 != password2:
            return render_template('registration.html', "Passwords should match")
        
        mongo.db.users.insert_one({'name': user, 'email': email, 'password': password1})
    
    
    return render_template('registration.html')
"""

@main.route('/', methods=["POST","GET"])
def index():
    #moviesCo = mongo.db.movies
    #return render_template('index.html')
    #updateDatabase()
    return render_template('base.html')

# To display a recommandation
@main.route('/display')
def display():
    rMovie = mongo.db.movies.aggregate([{"$sample": { "size": 1 } }])
    randomMovie = list(rMovie)
    #randomMovie = mongo.db.movies.find({"Film":"Gran Torino"})
    #randomMovie=list(randomMovie)
    #print(randomMovie)

    return render_template('display_movie.html', m=randomMovie[0])


@main.route('/add_movie', methods=['POST'])
def add_movie():
    moviesCo = mongo.db.movies
    movieName = request.form.get('fname')
    movieReal = request.form.get('rname')
    movieDate = request.form.get('date')
    movieAvis = request.form.get('avis')
    moviesCo.insert_one({'Film':movieName, 'Réalisateur': movieReal, 'Date': movieDate, 'Avis':movieAvis})
    return redirect(url_for('main.index'))
