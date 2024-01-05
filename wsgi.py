# wsgi.py

from app import flask_server, app

# Ensure the app is callable
application = app.server

if __name__ == "__main__":
    application.run(debug=True)
