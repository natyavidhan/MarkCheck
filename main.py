from flask import Flask, render_template, session
from flask_pymongo import PyMongo
from config import Config
import os

from auth import auth_bp  # Import the blueprint and init function
from boards import boards_bp  # Import the boards blueprint

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB setup
mongo = PyMongo(app)

auth_bp.mongo = mongo
app.register_blueprint(auth_bp)

boards_bp.mongo = mongo
app.register_blueprint(boards_bp)

@app.route('/')
def index():
    if 'user' in session:
        user = mongo.db.users.find_one({"email": session['user']})
        return render_template('dashboard.html', user=user)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    
    # Allow insecure transport for development purposes
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    app.run(debug=True)
