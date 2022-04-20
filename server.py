# Server app, should contain the database

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import csv, socket, os, requests

app = Flask(__name__)
api = Api(app)

# Gets csv data and puts it in a list (still uses csv parser)
def getTracksData():
    results = []
    with open('tracks.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            results.append(line)
    return (results)

def search(searchType, searchTerm):
    # fetch csv data
    results = getTracksData()

    # filter/search based on the searchType and searchTerm
    if searchType.upper() == "ID":
        results = [d for d in results if searchTerm.lower() in d['id'].lower()]
    elif searchType.upper() == "NAME":
        results = [d for d in results if searchTerm.lower() in d['name'].lower()]
    elif searchType.upper() == "POPULARITY":
        results = [d for d in results if searchTerm.lower() in d['popularity'].lower()]
    elif searchType.upper() == "DURATION_MS":
        results = [d for d in results if searchTerm.lower() in d['duration_ms'].lower()]
    elif searchType.upper() == "EXPLICIT":
        results = [d for d in results if searchTerm.lower() in d['explicit'].lower()]
    elif searchType.upper() == "ARTISTS":
        results = [d for d in results if searchTerm.lower() in d['artists'].lower()]
    elif searchType.upper() == "ID_ARTISTS":
        results = [d for d in results if searchTerm.lower() in d['id_artists'].lower()]
    elif searchType.upper() == "RELEASE_DATE":
        results = [d for d in results if searchTerm.lower() in d['release_date'].lower()]
    elif searchType.upper() == "DANCEABILITY":
        results = [d for d in results if searchTerm.lower() in d['danceability'].lower()]
    elif searchType.upper() == "ENERGY":
        results = [d for d in results if searchTerm.lower() in d['energy'].lower()]
    elif searchType.upper() == "KEY":
        results = [d for d in results if searchTerm.lower() in d['key'].lower()]
    elif searchType.upper() == "LOUDNESS":
        results = [d for d in results if searchTerm.lower() in d['loudness'].lower()]
    elif searchType.upper() == "MODE":
        results = [d for d in results if searchTerm.lower() in d['mode'].lower()]
    elif searchType.upper() == "SPEECHINESS":
        results = [d for d in results if searchTerm.lower() in d['speechiness'].lower()]
    elif searchType.upper() == "ACOUSTICNESS":
        results = [d for d in results if searchTerm.lower() in d['acousticness'].lower()]
    elif searchType.upper() == "INSTRUMENTALNESS":
        results = [d for d in results if searchTerm.lower() in d['instrumentalness'].lower()]
    elif searchType.upper() == "LIVENESS":
        results = [d for d in results if searchTerm.lower() in d['liveness'].lower()]
    elif searchType.upper() == "VALENCE":
        results = [d for d in results if searchTerm.lower() in d['valence'].lower()]
    elif searchType.upper() == "TEMPO":
        results = [d for d in results if searchTerm.lower() in d['tempo'].lower()]
    elif searchType.upper() == "TIME_SIGNATURE":
        results = [d for d in results if searchTerm.lower() in d['time_signature'].lower()]


    # get total count of records, and set the number returned
    #totalCount = len(results)

    # limit, slice the return data
    #try:
        # converts searchCount to integer
       # searchCount = int(searchCount)
    #except:
        # default count value
      #  searchCount = 20

    # if count is not negative 1, then slice. if count is -1, return entire list 
    #if searchCount != -1:
        #results = results[0:searchCount]

    # how many tracks will actually be returned
    #count = len(results)

    # build and return the json response
    #response = {
        #'tracksFound': totalCount,
        #'tracksDisplayed': count,
        #'tracks': results,
    #}
    return jsonify(results)

# Creates a resource called SearchTracks which searches and filters tracks
class Search(Resource):
    def get(self):
        args = request.args

        searchType = args.get("type")
        searchTerm = args.get("term")

        return search(searchType, searchTerm)

def export():
    test_file = open("tracks.csv", "rb")
    test_url = "http://127.0.0.1/tracks"
    test_response = requests.post(test_url, files = {"form_field_name": test_file})
    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print("Something went wrong!")
    return 1

class Export(Resource):
    def get(self):
        return export()

# Returns the resource SearchTracks when resolving the url */api/searchTracks
api.add_resource(Search, "/api/search")
api.add_resource(Export, "/export")

# Creates a resource called DefaultDatabase which returns the full database
class DefaultDatabase(Resource):
    def get(self):
        return jsonify(getTracksData())

# Returns the resource DefaultDatabase when resolving the url */default
api.add_resource(DefaultDatabase, "/default")

# Server runs on port 4995
if __name__ == "__main__":
    app.run(port=4995, debug=True)