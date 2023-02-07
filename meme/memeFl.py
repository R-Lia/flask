#!/usr/bin/python3

from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def get_meme():
    url = "https://meme-api.com/gimme"
    r = requests.get(url)
    jsonR = json.loads(r.text)
    #preview = jsonR["preview"][-1]
    #author = 
    return jsonR

@app.route('/')
def index():
    jsonR = get_meme()
    data = {"author":jsonR["author"]}
    return render_template("index_meme.html",data=jsonR)


if __name__ == "__main__":    
    app.run(host="0.0.0.0", port=5000)
