from flask import Flask, render_template, session, redirect, Blueprint 

from auth.login import login
from auth.signup import signUp
# from meeting.create_meeting import create_meeting
# from meeting.list_meeting import list_meeting
from flask_cors import CORS

# Global Flask app (SUBJECT TO CHANGE) static_folder="../frontend/assets,template_folder="../frontend/html""
app = Flask(__name__, static_folder="../frontend/css", template_folder="../frontend/html")
CORS(app, resources={r"*": {"origins": "*"}}) 

script_bp = Blueprint('script', __name__, static_folder='../frontend/script', static_url_path='/script')
app.register_blueprint(script_bp)
app.register_blueprint(login)
app.register_blueprint(signUp)
# app.register_blueprint(create_meeting)
# app.register_blueprint(list_meeting)

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug = True)