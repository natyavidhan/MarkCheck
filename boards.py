from flask import Blueprint, request, session, redirect, url_for
from flask_pymongo import PyMongo
from config import Config
import random

boards_bp = Blueprint('boards', __name__)

@boards_bp.route('/boards', methods=['GET', 'POST'])
def create_board():
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        
        board_name = request.form.get('board_name')
        if board_name:
            # Use the mongo object from the blueprint
            boards_bp.mongo.db.users.update_one(
                {"email": session['user']},
                {"$push": {"boards": {"id": str(random.randint(100000, 999999)), "name": board_name, "content": ""}}}
            )
        return redirect(url_for('index'))
