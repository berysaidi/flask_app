''' Application initialization '''
from datetime import timedelta
from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager

# this will serve for caching mac addresses.
cache_cfg = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_HEADER_NAME"] = "x-authentication-token" #As Per requirement
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

# Init the JWT manager
jwt = JWTManager(app)


app.config.from_mapping(cache_cfg)
cache = Cache(app)

from app import routes, schema

