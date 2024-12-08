import subprocess
from flask import Flask, request, render_template, jsonify, session, redirect, Blueprint 

from auth.login import login
from auth.signup import signUp
from meeting.create_meeting import create_meeting
from meeting.list_meeting import list_meeting
from flask_cors import CORS

# Global Flask app (SUBJECT TO CHANGE) static_folder="../frontend/assets,template_folder="../frontend/html""
app = Flask(__name__, static_folder="../frontend/css", template_folder="../frontend/html")
CORS(app, resources={r"*": {"origins": "*"}}) 

script_bp = Blueprint('script', __name__, static_folder='../frontend/script', static_url_path='/script')
app.register_blueprint(script_bp)
app.register_blueprint(login)
app.register_blueprint(signUp)
app.register_blueprint(create_meeting)
app.register_blueprint(list_meeting)

@app.route('/register')
def register():
    return render_template('register.html')

# @app.route('/start-client', methods=['POST'])
# def start_client():
#     try:
#         # 可選：檢查傳入的帳號或其他必要參數
#         data = request.get_json()
#         account = data.get('account')

#         # 使用 subprocess 啟動 client.py
#         subprocess.Popen(['python', 'client.py'])

#         return jsonify({"status": "success", "message": "Client started successfully!"})
#     except Exception as e:
#         return jsonify({"status": "error", "message": f"Error starting client: {e}"})
    

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

@app.route('/list_meeting', methods=['GET'])
def list_meeting():
    return render_template('list_meeting.html')



if __name__ == '__main__':
    app.run(debug = True)