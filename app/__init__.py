from flask import Flask
from dotenv import load_dotenv
import os
from .auth import auth
from .routes import routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.register_blueprint(auth)
app.register_blueprint(routes)
