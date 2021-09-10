''' Application initialization '''
from datetime import timedelta
from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

TIMEOUT = 15
# this will serve for caching mac addresses.
CACHE_CFG = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
# name of your database; add path if necessary
DB_NAME = ':memory'




app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_HEADER_NAME"] = "x-authentication-token" #As Per requirement
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=TIMEOUT)

# Init the JWT manager
jwt = JWTManager(app)

# Init the cache
app.config.from_mapping(CACHE_CFG)
cache = Cache(app)

# Init the Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

from app import routes, schema, models

# setup the db
db.create_all()


