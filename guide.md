### Strava Activity Summarizer 


How this works: 

1) A flask server listens for new activities 
2) When a new activity is detected, the server gets the ID and requests the activity data 
3) A couple of utility functions parse this information into a cleaned activity summary 
4) The server sends a put request to update the activity with the ID's description


**Important Notes**
*Getting API access*: 
Code for this can be found in `auth_guide.py`
1. Request code from Strava 
2. Use this code to generate an access token and a refresh token 

Code for this step can be found in `utilities.py`
3. Keep the refresh token so that when the access token expires you can fetch a new one 

*Subscribing to webhooks*
This step shows you how to set up your server url to handle incoming requests (like when an event is uploaded). 
Code for this step can be found in `push_guide.py`
1. Send a post request to Strava's push subscription website to initialize a subscription 
2. Configure your server to handle the challenge & respond 
3. Done! Now you've created a server that will receive webhooks for when activities are uploaded to this account :)
