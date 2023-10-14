#### Step 1: Generate authorization code 

# paste this into a browser & copy the code generated
url = "https://www.strava.com/oauth/authorize?client_id={your_client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read,activity:read,activity:write,activity:read_all"


#### Step 2: Generate bearer token 

# make a post request to this endpoint: https://www.strava.com/oauth/token
# with the following params: 

url = "https://www.strava.com/oauth/token"
params = {
    "client_id": "<client_id>", 
    "client_secret": "<client_secret>",
    "code": "<code>", 
    "grant_type": "authorization_code"
}

resp = requests.post(url, params=params)
json = resp.json()

access_token = json["access_token"]
refresh_token = json["refresh_token"]

os.environ["access_token"] = access_token
os.environ["refresh_token"] = refresh_token
