from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Import Blueprints
from routes.auth import auth_bp
from routes.content import content_bp
from routes.subscription import subscription_bp
from routes.webhooks import webhooks_bp  # Added Webhooks

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use PostgreSQL in production

# Initialize Database & Login Manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Register Blueprints (Modular Routing)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(subscription_bp, url_prefix='/subscribe')
app.register_blueprint(webhooks_bp, url_prefix='/webhooks')  # Added Webhooks

# Load User Model
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define Routes for Each Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/premium')
def premium():
    return render_template('premium.html')

if __name__ == '__main__':
    app.run(debug=True)
