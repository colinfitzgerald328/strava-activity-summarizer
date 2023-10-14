import requests

# Send this request to the server where you will receive incoming webhooks 
url = "https://www.strava.com/api/v3/push_subscriptions"
data = {
    "client_id": "<client_id>",
    "client_secret": "<client_secret>",
    "callback_url": "<your_server_url>",
    "verify_token": "STRAVA"
}

response = requests.post(url, data=data)

# Check the response
if response.status_code == 200:
    print("Subscription created successfully.")
else:
    print(f"Failed to create subscription. Status code: {response.status_code}")
    print(response.text)


# This is an example of how your server should handle the request to properly respond to the challenge: 
from flask import Flask, request, jsonify

app = Flask(__name)

@app.route('/<your_server_url>', methods=['GET'])
def validate_subscription():
    hub_challenge = request.args.get('hub.challenge')
    hub_verify_token = request.args.get('hub.verify_token')

    # Check if the hub_verify_token matches your expected value
    if hub_verify_token == 'STRAVA':
        return jsonify({"hub.challenge": hub_challenge}), 200
    else:
        return "Invalid verify token", 403

if __name__ == '__main__':
    app.run(debug=True)
