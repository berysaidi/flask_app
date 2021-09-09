from flask import Flask
from flask_json import FlaskJSON
from flask_caching import Cache

# 
cache_cfg = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

json = FlaskJSON(app)
json.init_app(app)

app.config.from_mapping(cache_cfg)
cache = Cache(app)


from app import routes, schema
