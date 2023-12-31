# strava-activity-summarizer
A quick app to summarize strava activities as they are uploaded

![Screenshot 2023-10-14 at 10 17 37 AM](https://github.com/colinfitzgerald328/strava-activity-summarizer/assets/64982557/0df80a9b-3cb3-444e-b8b1-9128726ccda6)

How this works: 

1) A flask server, subscribed to webhooks, receives a request when a new activity is uploaded
2) When a new activity is detected, the server gets the ID and requests the activity data 
3) A couple of utility functions parse this information into a cleaned activity summary 
4) The server sends a put request to update the activity with the ID's description


**Important Notes**

*Getting API access*: 
Code for this can be found in `auth_guide.py`
1. Request code from Strava 
2. Use this code to generate an access token and a refresh token 

*Refreshing a token*: Code for this step can be found in `utilities.py`

3. Keep the refresh token so that when the access token expires you can fetch a new one 

*Subscribing to webhooks*: This step shows you how to set up your server url to handle incoming requests (like when an event is uploaded). 

Code for this step can be found in `push_guide.py`
1. Send a post request to Strava's push subscription website to initialize a subscription 
2. Configure your server to handle the challenge & respond 
3. Done! Now you've created a server that will receive webhooks for when activities are uploaded to this account :)
