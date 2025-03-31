from flask import Blueprint, request, session, redirect, url_for
from flask_pymongo import PyMongo
from config import Config

boards_bp = Blueprint('boards', __name__)

# MongoDB setup
mongo = PyMongo()

@boards_bp.route('/boards', methods=['GET', 'POST'])
def create_board():
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        
        board_name = request.form.get('board_name')
        if board_name:
            mongo.db.users.update_one(
                {"email": session['user']},
                {"$push": {"boards": {"name": board_name}}}
            )
        return redirect(url_for('index'))
    
    # Render a simple form for creating a new board
    return '''
        <form method="POST">
            <label for="board_name">Board Name:</label>
            <input type="text" id="board_name" name="board_name" required>
            <button type="submit">Create Board</button>
        </form>
    '''
