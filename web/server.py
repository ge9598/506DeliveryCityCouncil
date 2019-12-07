from flask import Flask, render_template, jsonify, abort
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient()
db = client.cs504

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    ward_data = db.ward_data.find({})
    result = {}

    for data in ward_data:
        result[data["Ward"]] = data

    for wid in result.keys():
        del result[wid]['_id']

    return jsonify(result)


@app.route("/api/v0.1/Ward/<int:wid>")
def getWard(wid):
    if wid < 1 or wid > 22:
        abort(404)

    ward_data = db.ward_data.find({'Ward': wid})
    result = {}
    for data in ward_data:
        result = data
    del result['_id']

    return jsonify(result)


@app.route("/api/v0.1/Election/<int:wid>/")
def getElection(wid):
    if wid < 1 or wid > 22:
        abort(404)

    ward_data = db.ward_data.find({'Ward': wid})
    result = {}
    for data in ward_data:
        result = data
    del result['_id']

    return jsonify(result["Election"])


@app.route("/api/v0.1/Voter/<int:wid>/")
def getVoter(wid):
    if wid < 1 or wid > 22:
        abort(404)

    ward_data = db.ward_data.find({'Ward': wid})
    result = {}
    for data in ward_data:
        result = data
    del result['_id']

    return jsonify(result["Voter"])



if __name__ == "__main__":
    app.run(debug=True)
