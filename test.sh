#!/bin/bash
#first install httpie, then
http POST http://127.0.0.1:5000/predict num_predictions:=5 ratings:='[{"name": "Antipasto Salad", "rating": 1}, {"name": "Italian Orzo Salad", "rating": 0}]'