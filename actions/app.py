from flask import Flask, render_template, session, redirect, Blueprint, 

from auth.login import login
from auth.signup import signUp
from flask_cors import CORS

# Global Flask app (SUBJECT TO CHANGE) static_folder="../frontend/assets,template_folder="../frontend/html""
app = Flask(__name__, template_folder="../frontend/html", static_folder="../frontend/css")
CORS(app, resources={r"*": {"origins": "*"}}) 

script_bp = Blueprint('script_bp', __name__, static_folder='../frontend/script')
app.register_blueprint(script_bp)
app.register_blueprint(login)
app.register_blueprint(signUp)


@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)