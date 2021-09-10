## General Info
This an app squeleton which implements the basic assignement requirements.
It's written in Python 3 and uses Flask as its web framework


## How to Run
You can run it on your machine by creating a virtual env based on the app requirements.txt
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=entry.py
flask run
```
You can also build it with Docker for easier deployment and CI integration
```
docker build -t flask-app -f- . < Dockerfile
docker run -it -p 5000:5000 flask-app
```

# Manual Testing
```
export CLIENT=client
```
* Register a user
```
 curl -X POST 127.0.0.1:5000/register -H "Content-Type: application/json" -H "x-client-id: $CLIENT"
 "The client <client> has been registered."
```

* Get the Token for the user
```
curl -X POST 127.0.0.1:5000/login -H "Content-Type: application/json" -H "x-client-id: $CLIENT"

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMTI0OTE3NiwianRpIjoiYjA4YzMwNzktOWNkMC00N2FjLWFhNDMtMDY4YTgyYmE5NTQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImNsaWVudCIsIm5iZiI6MTYzMTI0OTE3NiwiZXhwIjoxNjMxMjUwMDc2fQ.yllmNZhV8HADQNUClee0r2uj7OUvgNm4uA-W89dX3xo"
}
```

* export it to be easily accessible 

```
export TOKEN="access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzMTI0OTE3NiwianRpIjoiYjA4YzMwNzktOWNkMC00N2FjLWFhNDMtMDY4YTgyYmE5NTQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImNsaWVudCIsIm5iZiI6MTYzMTI0OTE3NiwiZXhwIjoxNjMxMjUwMDc2fQ.yllmNZhV8HADQNUClee0r2uj7OUvgNm4uA-W89dX3xo"

```
* Post your good profile
```
curl -X POST 127.0.0.1:5000/profiles/clientId:9c:eb:e8:8e:3b:00 -H "Content-Type: application/json" -H "x-authentication-token: Bearer $TOKEN" -H "x-client-id: $CLIENT" -d @profile.json
{
  "profile": {
    "applications": [
      {
        "applicationId": "music_app",
        "version": "v1.4.10"
      },
      {
        "applicationId": "diagnostic_app",
        "version": "v1.2.6"
      },
      {
        "applicationId": "settings_app",
        "version": "v1.1.5"
      }
    ]
  }
}

```

* Post your bad profile
```
curl -X POST 127.0.0.1:5000/profiles/clientId:9c:eb:e8:8e:3b:00 -H "Content-Type: application/json" -H "x-authentication-token: Bearer $TOKEN" -H "x-client-id: $CLIENT" -d @profile_wrong.json
{
  "error": "Conflict",
  "message": "data error",
  "statusCode": 409
}

```

Tokens must be refreshed every 15 minutes
```
$ curl -X POST 127.0.0.1:5000/profiles/clientId:9c:eb:e8:8e:3b:00 -H "Content-Type: application/json" -H "x-authentication-token: Bearer $TOKEN" -H "x-client-id: $CLIENT" -d @profile.json
{
	  "msg": "Token has expired"
}
```

* If you want to test it with the running image, and docker fails to map ports you can run the few greps inside the app's running container
```
docker exec -it $(docker ps | grep flask-app | awk '{print $1}') bash
```

# Unit Testing
We rely on Python's standard library integrated with Flask in testing
our routes. Run them with the following :
```
python app/test_routes.py
......
----------------------------------------------------------------------
Ran 6 tests in 0.021s

OK

```
