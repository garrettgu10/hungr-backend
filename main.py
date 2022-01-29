from ml import predict
from flask import Flask, request, jsonify
import json
import random

recipe_file = open('recipes.json', 'r')
recipe_arr = json.load(recipe_file)
recipes = {}
for recipe in recipe_arr:
    recipes[recipe['name']] = recipe

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def hello_world():
    req = request.json

    num_predictions = req['num_predictions']
    ratings = req['ratings']

    if num_predictions == None:
        return "Please specify the number of predictions you need"
    elif ratings == None:
        return "Please supply an array of ratings"

    if len(ratings) == 0:
        #predict a random list of recipes
        return jsonify({
            "recipes": random.sample(recipe_arr, num_predictions)
        })

    return jsonify({
        "recipes": predict(recipes, ratings, num_predictions)
    })