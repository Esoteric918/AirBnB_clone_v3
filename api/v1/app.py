#!/usr/bin/python3
"""sets up Flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
# Start Flask app
app = Flask()


@app.teardown_appcontext
def teardown(context):
    """reloads storage after each request"""
    storage.close()


if __name__ == "__main__":
    # run the app host
    # defaults:
    #   host 0.0.0.0
    #   port 5000
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)
