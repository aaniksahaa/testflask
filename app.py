import flask
from flask import request
import requests
import json

url = "https://famous-quotes4.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "683351e6d6msh5280d130f8100c4p1b86d2jsn83e8d30556e0",
	"X-RapidAPI-Host": "famous-quotes4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

text = response.text

quoteCats = json.loads(text)

# Util functions Start


def getLyricsFromID(id):

    url = "https://genius-song-lyrics1.p.rapidapi.com/songs/"+ str(id) +"/lyrics"

    headers = {
        "X-RapidAPI-Key": "683351e6d6msh5280d130f8100c4p1b86d2jsn83e8d30556e0",
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    t = response.text
    tt = json.loads(t)

    if(tt['meta']['status'] != 200):
        return "No Lyrics Found"

    r = tt['response']
    #print(r)
    lyrics = tt['response']['lyrics']['lyrics']['body']['plain']


    return lyrics


# Util functions End

app = flask.Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/quotes', methods=['GET'])
def getQuote():
    print("Yes hereee")
    cat = (request.args['category'])
    cnt = (request.args['count'])
    ress = []
    if(cat in quoteCats):

        url = "https://famous-quotes4.p.rapidapi.com/random"

        querystring = {"category":cat,"count":cnt}

        headers = {
            "X-RapidAPI-Key": "683351e6d6msh5280d130f8100c4p1b86d2jsn83e8d30556e0",
            "X-RapidAPI-Host": "famous-quotes4.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        t = response.text

        tt = json.loads(t)

        return tt
    else:
        return ress

@app.route('/music', methods=['GET'])
def getMusic():
    print("Yes hereee")
    query = (request.args['query'])
    count = (request.args['count']) # Count Sensitive
    cnt =  int(count)
    ress = []

    url = "https://genius-song-lyrics1.p.rapidapi.com/search"

    querystring = {"q":query,"per_page":"10","page":"1"}

    headers = {
        "X-RapidAPI-Key": "683351e6d6msh5280d130f8100c4p1b86d2jsn83e8d30556e0",
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    t = response.text

    tt = json.loads(t)

    #print(tt)

    hits = tt['response']['hits']

    #if(len(hits)==0):
        #return []

    i = 0
    n = len(hits)
    while(i<n and i<cnt):

        result = hits[i]['result']

        title = result['title']
        full_title = result['full_title']
        artist = result['artist_names']
        id = result['id']

        lyrics = getLyricsFromID(id)

        #print(lyrics)

        print(title)

        dict = {}
        dict['full_title'] = full_title
        dict['title'] = title
        dict['artist'] = artist
        dict['lyrics'] = lyrics
        dict['geniusId'] = id

        ress.append(dict)

        i = i+1

    return ress

@app.route('/', methods=['GET'])
def home():
    return "Hello"


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
