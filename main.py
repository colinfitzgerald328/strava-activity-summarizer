from flask import Flask, request, jsonify 
from utilities import update_activity
app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'


@app.route('/process', methods=["GET", "POST"])
def process_activity():
  # Parse the JSON data sent by Strava
  strava_data = request.json
  activity_id = strava_data["object_id"]
  update_activity(activity_id)
  return '', 200





app.run(host='0.0.0.0', port=8080)
