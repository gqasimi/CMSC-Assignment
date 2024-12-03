from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
print("DB_USER:", os.getenv('HW5_USER'))
print("DB_PASSWORD:", os.getenv('HW5_PASSWORD'))
print("DB_HOST:", os.getenv('HW5_HOST'))
print("DB_NAME:", os.getenv('HW5_DB_NAME'))

# Initialize Flask app
app = Flask(__name__)

# Configure database connection using values from .env
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('HW5_USER')}:{os.getenv('HW5_PASSWORD')}@{os.getenv('HW5_HOST')}/{os.getenv('HW5_DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.username}>"

# Create database tables (only needed for the first run)
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return "Welcome to the ACMS Project!"

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

# Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'user_id': user.user_id, 'username': user.username, 'email': user.email, 'status': user.status} for user in users]
    return jsonify(users_list)

# Retrieve a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'user_id': user.user_id, 'username': user.username, 'email': user.email, 'status': user.status})

# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.status = data.get('status', user.status)
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
