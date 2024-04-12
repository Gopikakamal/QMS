# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~
    This script is used to run the Flask application defined in the
    'app' module. It starts the development server with debugging enabled.

    :copyright: (c) 2024 by Petrus Technologies
"""

from app import connexion_app

if __name__ == '__main__':
    connexion_app.run(debug=True)
