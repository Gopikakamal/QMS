# -*- coding: utf-8 -*-
"""
    app
    ~~~~
    This script initializes a Flask web application using Connexion with
    an OpenAPI specification. It configures MongoDB integration,
    enables Cross-Origin Resource Sharing (CORS), and sets up the necessary
    components for building a RESTful web service.

    :copyright: (c) 2024 by Petrus Technologies
"""

from os import getenv
from connexion import FlaskApp
from flask_cors import CORS
from pymongo import MongoClient


# Configure DataBase
db_connection = MongoClient(getenv("MONGO_URI"))

# Initialize Connexion app with the OpenAPI specification
connexion_app = FlaskApp(__name__, specification_dir='./openapi')
app = connexion_app.app

connexion_app.add_api('api.yaml')

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)
